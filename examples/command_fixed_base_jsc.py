"""Native SuperDex JSC command path; source-reviewed, syntax-checked, NOT run.

Caller owns the Scene, Bot and configured BASIC_JSC_PD controller. This example
supports a HARD root and scalar moving joints only. The controller must belong to
actor, and this function must be the sole external-force writer for that actor.
No scene creation, imports at validation time, stepping or experiments are performed.
"""

from __future__ import annotations

from collections.abc import Sequence
import math

import superdex.physics as physics
import superdex.robotics as robotics


def command_fixed_base_jsc(
    actor: physics.Actor,
    controller: robotics.ControllerBasicJscPd,
    target_pose: Sequence[float],
    control_period_s: float,
    effort_limits: Sequence[float],
) -> list[float]:
    """Compute, cap and write one actor-space command; return copied commands.

    Limits must already be mapped to actor DoF order: negative means unbounded,
    zero disables driving, positive means a finite magnitude. Returned values
    are input commands in N or N*m, not measured contact or total constraint force.
    Call controller.reset() alongside the application's episode reset.
    """
    if not math.isfinite(control_period_s) or control_period_s <= 0:
        raise ValueError("control_period_s must be finite and positive")
    layout = actor.get_articulated_shape_info().dof_info
    if not len(layout) or layout[0].get_size() != 0:
        raise ValueError("this teaching example requires a HARD root")
    if any(info.get_size() > 1 for info in layout):
        raise ValueError("this teaching example supports scalar moving joints only")
    count = actor.get_num_dofs()
    if len(target_pose) != count or len(effort_limits) != count:
        raise ValueError("targets and limits must match actor DoF count")
    if not all(math.isfinite(x) for x in (*target_pose, *effort_limits)):
        raise ValueError("targets and limits must be finite")

    observations = controller.get_current_observations_from_mochi()
    observations.dt = control_period_s
    target = robotics.ControllerBasicJscPdTarget(target_pose=target_pose)
    # Copy the controller-owned output immediately: subsequent calls may reuse it.
    commands = [float(x) for x in controller.compute_output(observations, target)]
    if len(commands) != count or not all(math.isfinite(x) for x in commands):
        raise ValueError("controller returned invalid efforts")
    for i, limit in enumerate(effort_limits):
        if limit >= 0:
            commands[i] = max(-limit, min(limit, commands[i]))

    # Replaces the actor's entire external-force set; does not add to earlier calls.
    actor.set_external_forces_on_dofs(list(range(count)), commands)
    return commands
