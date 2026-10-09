# SuperDex Atlas

Understand SuperDex through native APIs, physics concepts and versioned source code.

[中文](README.md) · [Introductory guide](docs/guide.md) · [Curriculum](docs/curriculum.md) · [Source map](docs/source-map.md) · [Versions](docs/versions.md) · [Roadmap](docs/roadmap.md) · [Project tracker](https://github.com/users/huangkiki/projects/2) · [Series home](https://github.com/huangkiki/sim-atlas)

Part of **[Sim Atlas](https://github.com/huangkiki/sim-atlas)**, an independent community learning series with two complete planned tracks: applications (modeling, control, robotics, sensing and data) and principles/source (dynamics, contact, solvers, integration and extensions).

The initial guide, pinned source map, and [E1 modeling, coordinates, state and time chapter](docs/modeling-state-time.md) are available in Chinese. E1 covers native frames/inertia, URDF import limits, state dimensions and ownership, snapshots, stepping and integration foundations; it includes answered reading exercises and an unexecuted native API snippet. See [validation and limitations](docs/validation-e1.md). A1/A2 are documented; B0/B4 foundations are documented, with dynamics assembly and numerical solving developed further in E3 below.

The [E2 control, robotics and task-interface chapter](docs/control-robotics.md) now covers A3/A5/A7: native DoF mapping, JSC/OSC, implicit pose tracking, transmissions, FK/IK, limits, callbacks and application-owned task scheduling. Its native command snippet remains unexecuted; see [E2 validation](docs/validation-e2.md). Data and extension topics remain in development.

The [E3 contact, solvers and force-observation chapter](docs/contact-solvers-forces.md) documents A4 and B1–B5, extending B0 with dynamics assembly. It explains directional contact geometry, field-specific geometric-mean material rules and static-collider exceptions, penalty and regularized friction equations, Backward Euler assumptions, island/stage execution, nonlinear and linear solvers, convergence modes, and force/query timing. It includes 16 answered exercises and an unexecuted native reader; see [E3 validation](docs/validation-e3.md). This fixed source does not establish the binary or solver configuration of historical DexLab runs. Detailed deformable/differentiable extensions remain E6 work.

The [E4 sensors, rendering and visualization chapter](docs/sensors-rendering.md) documents A6: CameraSensor metadata versus image production, distance/ray/force/tactile boundaries, RGB/RGBA and missing depth/segmentation contracts, native projection and distortion, frame delays, and GUI/headless ownership. It traces Polyscope, Mochi renderer, UnrealCV and Studio separately, including a pinned Polyscope 2.5.0 reference for its actual RGBA screenshot contract. Sixteen answered exercises, a native metadata reader and a render-readback snippet are source/syntax checked only; no native imports, rendering or simulation were performed. See [E4 validation](docs/validation-e4.md). UE/plugin server identity and depth/mask semantics remain explicit gaps, not invented native capabilities.

This phase prioritizes understanding engine subsystems. Minimal snippets support explanation and are explicitly marked when unexecuted. No new simulation campaigns, benchmarks, training or scoring are included; later experimental material will reuse [DexLab](https://github.com/huangkiki/Dexlab) with its original version and workload boundaries.

[Pinned upstream source](https://github.com/facebookresearch/project_superdex/tree/1d7150946fa3f3d3fb09c2bff07eaa138cbfdee6) · [Attribution](THIRD_PARTY.md)
