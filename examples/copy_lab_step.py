"""Copy a completed native Lab step; source/syntax checked, never executed.

Call on the environment's owning thread, after step() and before any other
mutation. This reads cached Lab data, not the shared Scene's current contents.
The caller supplies a logical ID, retains the previous observation separately,
and owns the native contexts. No native imports or simulation occur here.
"""

from __future__ import annotations

from copy import deepcopy
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from superdex.lab.gym.envs import MochiEnv


def copy_lab_step(env: MochiEnv, *, logical_env_id: int) -> dict[str, object]:
    """Copy Python/NumPy data and label nominal control time explicitly.

    Custom info must contain deepcopy-compatible data, not native resources.
    This is not an atomic snapshot, an on-disk schema or a complete transition.
    """
    if env.is_closed():
        raise ValueError("cannot read a closed environment")
    last = env.get_last_step()
    if last.action is None or last.reward is None:
        raise ValueError("reset output is not a completed action transition")
    last = deepcopy(last)
    control_step = env.get_step_count()
    control_dt = env.get_control_timestep()
    return {
        "logical_env_id": logical_env_id,
        "episode": env.get_episode(),
        "control_step": control_step,
        "control_dt_s": control_dt,
        "simulation_dt_s": env.get_simulation_timestep(),
        "simulation_substeps": env.get_control_to_simulation_ratio(),
        "nominal_control_elapsed_s": control_step * control_dt,
        "applied_structured_action": last.action,
        "next_structured_observation": last.observation,
        "reward_terms": last.reward,
        "terminated": last.terminated,
        "truncated": last.truncated,
        "info": last.info,
    }
