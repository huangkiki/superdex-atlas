# superdex-atlas 固定版本源码入口

阅读基线：`1d7150946fa3f3d3fb09c2bff07eaa138cbfdee6`。以下入口已核对官方 Git 树与文件内容身份；不是全仓审查或运行验收记录。

本阶段先理解引擎架构、建模、步进、控制、接触/求解、传感器/渲染、性能与扩展。独立实验、基准、训练和评分暂不开展，后续复用 DexLab。

| 源码文件 | 阅读目的 |
|---|---|
| [README.md](https://github.com/facebookresearch/project_superdex/blob/1d7150946fa3f3d3fb09c2bff07eaa138cbfdee6/README.md) | 核对对象职责、数据布局、参数与版本约定 |
| [superdex_physics/examples/example_rigid_bodies.py](https://github.com/facebookresearch/project_superdex/blob/1d7150946fa3f3d3fb09c2bff07eaa138cbfdee6/superdex_physics/examples/example_rigid_bodies.py) | 理解官方最小使用顺序；本轮不执行 |
| [superdex_physics/examples/example_state_capture_restore.py](https://github.com/facebookresearch/project_superdex/blob/1d7150946fa3f3d3fb09c2bff07eaa138cbfdee6/superdex_physics/examples/example_state_capture_restore.py) | 理解官方最小使用顺序；本轮不执行 |
| [superdex_robotics/src/controllers/controller_basic_jsc_pd.cpp](https://github.com/facebookresearch/project_superdex/blob/1d7150946fa3f3d3fb09c2bff07eaa138cbfdee6/superdex_robotics/src/controllers/controller_basic_jsc_pd.cpp) | 核对对象职责、数据布局、参数与版本约定 |
| [superdex_robotics/src/sensors/camera_sensor.cpp](https://github.com/facebookresearch/project_superdex/blob/1d7150946fa3f3d3fb09c2bff07eaa138cbfdee6/superdex_robotics/src/sensors/camera_sensor.cpp) | 区分传感数据、可视化与物理状态 |
| [superdex_physics/libraries/mochi/mochi_physics/src/mochi_scene.cpp](https://github.com/facebookresearch/project_superdex/blob/1d7150946fa3f3d3fb09c2bff07eaa138cbfdee6/superdex_physics/libraries/mochi/mochi_physics/src/mochi_scene.cpp) | 追踪构建、步进、数据更新与生命周期 |
| [superdex_physics/libraries/mochi/mochi_physics/include/mochi_physics/cpp_api/mochi_scene.h](https://github.com/facebookresearch/project_superdex/blob/1d7150946fa3f3d3fb09c2bff07eaa138cbfdee6/superdex_physics/libraries/mochi/mochi_physics/include/mochi_physics/cpp_api/mochi_scene.h) | 追踪构建、步进、数据更新与生命周期 |
| [superdex_physics/libraries/mochi/mochi_physics/src/mochi_integration.cpp](https://github.com/facebookresearch/project_superdex/blob/1d7150946fa3f3d3fb09c2bff07eaa138cbfdee6/superdex_physics/libraries/mochi/mochi_physics/src/mochi_integration.cpp) | 核对对象职责、数据布局、参数与版本约定 |
| [superdex_physics/libraries/mochi/mochi_core/include/mochi_core/integration/integration_params.h](https://github.com/facebookresearch/project_superdex/blob/1d7150946fa3f3d3fb09c2bff07eaa138cbfdee6/superdex_physics/libraries/mochi/mochi_core/include/mochi_core/integration/integration_params.h) | 核对对象职责、数据布局、参数与版本约定 |
| [superdex_physics/libraries/mochi/mochi_core/include/mochi_core/solvers/newton_solver_params.h](https://github.com/facebookresearch/project_superdex/blob/1d7150946fa3f3d3fb09c2bff07eaa138cbfdee6/superdex_physics/libraries/mochi/mochi_core/include/mochi_core/solvers/newton_solver_params.h) | 识别算法、输入状态、配置与限制 |
| [superdex_physics/libraries/mochi/mochi_core/src/solvers/newton_solver.cpp](https://github.com/facebookresearch/project_superdex/blob/1d7150946fa3f3d3fb09c2bff07eaa138cbfdee6/superdex_physics/libraries/mochi/mochi_core/src/solvers/newton_solver.cpp) | 识别算法、输入状态、配置与限制 |
| [superdex_physics/libraries/mochi/mochi_core/include/mochi_core/contact/contact_params.h](https://github.com/facebookresearch/project_superdex/blob/1d7150946fa3f3d3fb09c2bff07eaa138cbfdee6/superdex_physics/libraries/mochi/mochi_core/include/mochi_core/contact/contact_params.h) | 区分接触几何、接触律与数值近似 |
