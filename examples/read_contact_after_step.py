"""Copy native contact observations; source-reviewed, syntax-checked, NOT run.

The caller owns the initialized Scene and a dynamic rigid actor (or rigid link)
belonging to that Scene. It must not mutate either concurrently with this reader.
Before the application's next positive-time step, it must check query support and
register actor.register_query(physics.QueryType.CONTACT_POINTS) and
actor.register_query(physics.QueryType.TOTAL_CONTACT_FORCE), retaining both handles.
Call this function after that step, before another step or state/model mutation.
Cancel each query with actor.cancel_query(handle) when finished. Registration,
stepping, and cancellation belong to that caller; this file executes none of them.
"""

from __future__ import annotations

import math

import superdex.physics as physics


def read_contact_after_step(scene: physics.Scene, actor: physics.Actor) -> dict[str, object]:
    """Return copied world-frame data, preserving B-to-A force direction.

    This teaching reader rejects NONE/DIVERGED but reports STOPPED explicitly.
    Status checks do not prove the caller registered queries before the step.
    Handles are only identifiers within this live scene, not persistent asset IDs.
    """
    if actor.get_type() != physics.ActorType.RIGID or actor.is_static():
        raise ValueError("this example requires a dynamic rigid actor or rigid link")
    step_s = scene.get_last_time_step()
    if not math.isfinite(step_s) or step_s <= 0:
        raise ValueError("this reader requires a finite positive physical step")
    stats = scene.get_solver_stats()
    actor_status = actor.get_convergence_status()
    invalid = (physics.ConvergenceStatus.NONE, physics.ConvergenceStatus.DIVERGED)
    if stats.convergence_status in invalid or actor_status in invalid:
        raise ValueError("no accepted positive-step contact observation is available")
    for query in (physics.QueryType.CONTACT_POINTS, physics.QueryType.TOTAL_CONTACT_FORCE):
        if not actor.is_query_supported(query):
            raise ValueError(f"actor does not support {query.name}")

    params = scene.get_solver_params()
    return {
        "actor_handle": actor.get_handle().value,
        "simulation_time_s": scene.get_total_simulation_time(),
        "last_step_s": step_s,
        "scene_status": stats.convergence_status.name,
        "actor_status": actor_status.name,
        "scene_raw_residual_norm": stats.residual_norm,
        "configured_integration": params.integration_method.name,
        "configured_nonlinear_solver": params.non_linear_solver.solver_type.name,
        "configured_linear_solver": params.linear_solver.solver_type.name,
        "convergence_mode": params.non_linear_solver.convergence_mode.name,
        "nonlinear_abs_tolerance": params.non_linear_solver.abs_tol,
        "nonlinear_rel_tolerance": params.non_linear_solver.rel_tol,
        "linear_norm": params.linear_solver.norm_type.name,
        "linear_tolerance_strategy": params.non_linear_solver.linear_tolerance_strategy.name,
        "force_world_N": actor.get_contact_force_world().tolist(),
        "torque_about_com_world_Nm": actor.get_contact_torque_world().tolist(),
        "contacts": [
            {
                "actor_a": point.actor_a.value,
                "actor_b": point.actor_b.value,
                "distance_m": float(point.distance),
                "pos_a_world_m": point.pos_a.tolist(),
                "force_on_a_from_b_world_N": point.force.tolist(),
                "spatial_integration_weight": float(point.int_weight),
            }
            for point in actor.get_contact_points_world()
        ],
    }
