"""Read one already-created dynamic rigid actor through native SuperDex APIs.

Teaching snippet only: source-reviewed and syntax-checked, never executed.
The caller owns initialization, precision selection, scene, actor and sampling phase.
Call after a completed step when studying post-step data. No stepping occurs here.
"""

import superdex.physics as physics


def inspect_rigid_state(
    scene: physics.Scene, actor: physics.Actor
) -> dict[str, float | list[float]]:
    """Copy a dynamic rigid actor's state into plain Python values.

    Precondition: actor belongs to scene, is a standalone dynamic rigid actor,
    and no other thread/callback mutates the scene during this sequence of reads.
    This is a teaching function, not an atomic snapshot or a replay checkpoint.
    """
    dofs = physics.DynamicArrayReal()
    dofs.resize(actor.get_num_dofs())
    actor.get_dof_values([], dofs)

    root = actor.get_root_transform()
    center = actor.get_center_of_mass_transform()
    return {
        "simulation_time_s": scene.get_total_simulation_time(),
        "root_translation_world_m": list(root.translation),
        "root_rotation_xyzw": root.rotation.tolist(),
        "center_of_mass_world_m": list(center.translation),
        "linear_velocity_com_world_m_s": list(actor.get_linear_velocity()),
        "angular_velocity_world_rad_s": list(actor.get_angular_velocity()),
        "mass_kg": actor.get_mass(),
        "inertia_at_com_local_kg_m2": list(actor.get_rigid_moment_of_inertia_local()),
        "dofs_com_position_then_rotation_vector": list(dofs),
    }
