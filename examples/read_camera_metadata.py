"""Copy CameraSensor metadata; source-reviewed and syntax-checked, NOT executed.

The caller owns the live native CameraSensor and all of its contexts. Keep the
physics state unchanged throughout these reads. This is metadata, not an image,
an atomic snapshot, or a rendering adapter. No native import occurs in this file.
"""

from __future__ import annotations

import math
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from superdex.robotics import CameraSensor


def read_camera_metadata(
    camera: CameraSensor,
    *,
    parent_kind: Literal["actor", "scene_root"],
    sample_time_s: float,
) -> dict[str, object]:
    """Preserve unresolved zero defaults and copy native frame/parameter values.

    parent_kind is the caller's remembered construction intent; get_actor() alone
    cannot distinguish an actor-less sensor from one whose actor was destroyed.
    sample_time_s is supplied by that caller, not reported by the sensor.
    """
    if not math.isfinite(sample_time_s) or sample_time_s < 0:
        raise ValueError("sample_time_s must be a finite nonnegative physical time")
    if parent_kind not in ("actor", "scene_root"):
        raise ValueError("parent_kind must identify the original sensor attachment")
    if not camera.is_valid():
        raise ValueError("the camera component is no longer valid")
    actor = camera.get_actor()
    if (parent_kind == "actor") != (actor is not None):
        raise ValueError("live actor does not match the original attachment intent")

    params = camera.get_params()
    parent_from_sensor = camera.get_parent_from_sensor()
    world_from_sensor = camera.get_world_transform()
    return {
        "application_sample_time_s": sample_time_s,
        "parent_kind": parent_kind,
        "actor_handle": actor.get_handle().value if actor is not None else None,
        "sensor_instance_name": camera.get_name(),
        "camera_parameter_name": params.name,
        "parent_from_sensor_translation_m": parent_from_sensor.translation.tolist(),
        "parent_from_sensor_xyzw": parent_from_sensor.rotation.tolist(),
        "world_from_sensor_translation_m": world_from_sensor.translation.tolist(),
        "world_from_sensor_xyzw": world_from_sensor.rotation.tolist(),
        "image_width_px": params.image_width,
        "image_height_px": params.image_height,
        "fov_vertical_deg": params.fov_vertical_deg,
        "near_clip_m": params.near_clip,
        "far_clip_m": params.far_clip,
        "fixed_look_at_world_m": params.look_at.tolist(),
        "wrist_offset_ee_local_m": params.offset_local.tolist(),
        "wrist_forward_axis_ee_local": params.forward_axis.tolist(),
        "wrist_up_axis_ee_local": params.up_axis_local.tolist(),
        "wrist_look_distance_m": params.look_distance,
    }
