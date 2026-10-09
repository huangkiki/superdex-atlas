# SuperDex Atlas

Understand SuperDex through native APIs, physics concepts and versioned source code.

[中文](README.md) · [Introductory guide](docs/guide.md) · [Curriculum](docs/curriculum.md) · [Source map](docs/source-map.md) · [Versions](docs/versions.md) · [Roadmap](docs/roadmap.md) · [Project tracker](https://github.com/users/huangkiki/projects/2) · [Series home](https://github.com/huangkiki/sim-atlas)

Part of **Sim Atlas**, an independent community learning series with two complete planned tracks: applications (modeling, control, robotics, sensing and data) and principles/source (dynamics, contact, solvers, integration and extensions).

The initial guide, pinned source map, and [E1 modeling, coordinates, state and time chapter](docs/modeling-state-time.md) are available in Chinese. E1 covers native frames/inertia, URDF import limits, state dimensions and ownership, snapshots, stepping and integration foundations; it includes answered reading exercises and an unexecuted native API snippet. See [validation and limitations](docs/validation-e1.md). A1/A2 are documented; B0/B4 foundations are documented, with solver mathematics and numerical convergence analysis continuing in E3.

The [E2 control, robotics and task-interface chapter](docs/control-robotics.md) now covers A3/A5/A7: native DoF mapping, JSC/OSC, implicit pose tracking, transmissions, FK/IK, limits, callbacks and application-owned task scheduling. Its native command snippet remains unexecuted; see [E2 validation](docs/validation-e2.md). Contact/solver, sensing, data and extension topics remain in development.

This phase prioritizes understanding engine subsystems. Minimal snippets support explanation and are explicitly marked when unexecuted. No new simulation campaigns, benchmarks, training or scoring are included; later experimental material will reuse [DexLab](https://github.com/huangkiki/Dexlab) with its original version and workload boundaries.

[Pinned upstream source](https://github.com/facebookresearch/project_superdex/tree/1d7150946fa3f3d3fb09c2bff07eaa138cbfdee6) · [Attribution](THIRD_PARTY.md)
