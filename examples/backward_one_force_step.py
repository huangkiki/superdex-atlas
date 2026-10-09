"""One native adjoint step; source/syntax checked, NEVER executed.

Preconditions: a differentiable scene containing supported actors, a dynamic
standalone rigid actor, and a converged constant-h forward step. The caller set
external DoF forces, captured state_old, stepped, captured state_new, and computed
the COM output gradient (translation + quaternion XYZW). Indices match that
forward setter. Snapshots belong to scene and remain owned by the caller.

Calling this function performs numerical work and mutates scene/adjoint state.
It is a one-step example: resetting inside a multi-step backward loop is wrong.
It does not restore the final forward state or promise transactional recovery.
"""

from __future__ import annotations

import math
from typing import TYPE_CHECKING, Sequence

if TYPE_CHECKING:
    from superdex.physics import Actor, Scene, StateHandle


def backward_one_force_step(
    scene: Scene,
    actor: Actor,
    state_old: StateHandle,
    state_new: StateHandle,
    *,
    dof_indices: Sequence[int],
    grad_com_output: Sequence[float],
) -> dict[str, object]:
    """Return input-force gradients and diagnostic values, not a proof of accuracy."""
    if len(grad_com_output) != 7 or not all(map(math.isfinite, grad_com_output)):
        raise ValueError("COM output gradient requires seven finite components")
    indices = list(dof_indices)
    if not indices or len(set(indices)) != len(indices):
        raise ValueError("forward DoF indices must be nonempty and unique")

    import superdex.physics as physics
    from superdex.physics import diffsim

    diffsim.reset_back_propagation(scene)
    diffsim.prepare_back_propagate(scene, state_new, state_old)
    diffsim.get_center_of_mass_transform_backward(actor, list(grad_com_output))
    diffsim.back_propagate(scene)
    output = physics.DynamicArrayReal(len(indices))
    diffsim.set_external_forces_on_dofs_backward(actor, indices, output)
    params = diffsim.get_back_propagation_solver_params(scene)
    stats = diffsim.get_back_propagation_scene_stats(scene)
    return {
        "dof_indices": indices,
        "gradient_wrt_force_values": list(output),
        "outer_iterations": stats.max_outer_iters,
        "residual_norm": stats.residual_norm,
        "finite_diff_check_enabled": params.validate_finite_diff,
        "finite_diff_valid": (
            stats.finite_diff_valid if params.validate_finite_diff else None
        ),
    }
