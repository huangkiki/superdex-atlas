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

## E1 建模、状态与时间追踪

对应[专题](modeling-state-time.md)与[验证记录](validation-e1.md)。以下新增文件已按固定 Git 树核对 blob；阅读不等于运行验收。

| 源码文件 | E1 阅读目的 |
|---|---|
| [superdex_physics/libraries/mochi/mochi_physics/include/mochi_physics/cpp_api/mochi_actor.h](https://github.com/facebookresearch/project_superdex/blob/1d7150946fa3f3d3fb09c2bff07eaa138cbfdee6/superdex_physics/libraries/mochi/mochi_physics/include/mochi_physics/cpp_api/mochi_actor.h) | 原生字段、API 维度与生命周期 |
| [superdex_physics/libraries/mochi/mochi_physics/include/mochi_physics/cpp_api/mochi_structs.h](https://github.com/facebookresearch/project_superdex/blob/1d7150946fa3f3d3fb09c2bff07eaa138cbfdee6/superdex_physics/libraries/mochi/mochi_physics/include/mochi_physics/cpp_api/mochi_structs.h) | 原生字段、API 维度与生命周期 |
| [superdex_physics/libraries/mochi/mochi_physics/src/mochi_actor.cpp](https://github.com/facebookresearch/project_superdex/blob/1d7150946fa3f3d3fb09c2bff07eaa138cbfdee6/superdex_physics/libraries/mochi/mochi_physics/src/mochi_actor.cpp) | 原生字段、API 维度与生命周期 |
| [superdex_physics/libraries/mochi/mochi_physics/pybind/stubs/public/mochi_physics/__init__.pyi](https://github.com/facebookresearch/project_superdex/blob/1d7150946fa3f3d3fb09c2bff07eaa138cbfdee6/superdex_physics/libraries/mochi/mochi_physics/pybind/stubs/public/mochi_physics/__init__.pyi) | 原生字段、API 维度与生命周期 |
| [superdex_physics/libraries/mochi/mochi_core/include/mochi_core/utils/quaternion.h](https://github.com/facebookresearch/project_superdex/blob/1d7150946fa3f3d3fb09c2bff07eaa138cbfdee6/superdex_physics/libraries/mochi/mochi_core/include/mochi_core/utils/quaternion.h) | 旋转次序、单位与 frame 转换 |
| [superdex_physics/libraries/mochi/mochi_core/include/mochi_core/utils/transform_rt_inl.h](https://github.com/facebookresearch/project_superdex/blob/1d7150946fa3f3d3fb09c2bff07eaa138cbfdee6/superdex_physics/libraries/mochi/mochi_core/include/mochi_core/utils/transform_rt_inl.h) | 旋转次序、单位与 frame 转换 |
| [superdex_physics/libraries/mochi/mochi_physics/pybind/src/generated/mochi_physics_pybind_actor.generated.cpp](https://github.com/facebookresearch/project_superdex/blob/1d7150946fa3f3d3fb09c2bff07eaa138cbfdee6/superdex_physics/libraries/mochi/mochi_physics/pybind/src/generated/mochi_physics_pybind_actor.generated.cpp) | 原生字段、API 维度与生命周期 |
| [superdex_physics/libraries/mochi/mochi_physics/pybind/src/generated/mochi_physics_pybind_scene.generated.cpp](https://github.com/facebookresearch/project_superdex/blob/1d7150946fa3f3d3fb09c2bff07eaa138cbfdee6/superdex_physics/libraries/mochi/mochi_physics/pybind/src/generated/mochi_physics_pybind_scene.generated.cpp) | 原生字段、API 维度与生命周期 |
| [superdex_physics/libraries/mochi/mochi_physics/pybind/src/pybind_nd_array.h](https://github.com/facebookresearch/project_superdex/blob/1d7150946fa3f3d3fb09c2bff07eaa138cbfdee6/superdex_physics/libraries/mochi/mochi_physics/pybind/src/pybind_nd_array.h) | Python 值、借用视图及输出缓冲 |
| [superdex_physics/libraries/mochi/mochi_physics/pybind/src/pybind_span.h](https://github.com/facebookresearch/project_superdex/blob/1d7150946fa3f3d3fb09c2bff07eaa138cbfdee6/superdex_physics/libraries/mochi/mochi_physics/pybind/src/pybind_span.h) | Python 值、借用视图及输出缓冲 |
| [superdex_python/superdex/physics/utils/coordinate_systems.py](https://github.com/facebookresearch/project_superdex/blob/1d7150946fa3f3d3fb09c2bff07eaa138cbfdee6/superdex_python/superdex/physics/utils/coordinate_systems.py) | 旋转次序、单位与 frame 转换 |
| [superdex_robotics/examples/basic/example_urdf_loading.py](https://github.com/facebookresearch/project_superdex/blob/1d7150946fa3f3d3fb09c2bff07eaa138cbfdee6/superdex_robotics/examples/basic/example_urdf_loading.py) | 导入变换、资产与 runtime 能力限制 |
| [superdex_robotics/src/utils/urdf_import_utils.cpp](https://github.com/facebookresearch/project_superdex/blob/1d7150946fa3f3d3fb09c2bff07eaa138cbfdee6/superdex_robotics/src/utils/urdf_import_utils.cpp) | 导入变换、资产与 runtime 能力限制 |
| [superdex_robotics/pybind/stubs/public/superdex_robotics/__init__.pyi](https://github.com/facebookresearch/project_superdex/blob/1d7150946fa3f3d3fb09c2bff07eaa138cbfdee6/superdex_robotics/pybind/stubs/public/superdex_robotics/__init__.pyi) | 原生字段、API 维度与生命周期 |
| [superdex_physics/libraries/mochi/mochi_core/include/mochi_core/integration/integration_utils.h](https://github.com/facebookresearch/project_superdex/blob/1d7150946fa3f3d3fb09c2bff07eaa138cbfdee6/superdex_physics/libraries/mochi/mochi_core/include/mochi_core/integration/integration_utils.h) | 时间离散、积分历史及外部状态改写 |
| [superdex_python/superdex/physics/__init__.py](https://github.com/facebookresearch/project_superdex/blob/1d7150946fa3f3d3fb09c2bff07eaa138cbfdee6/superdex_python/superdex/physics/__init__.py) | 进程精度选择与 native payload 校验 |
| [superdex_physics/libraries/mochi/mochi_physics/src/mochi_capture.cpp](https://github.com/facebookresearch/project_superdex/blob/1d7150946fa3f3d3fb09c2bff07eaa138cbfdee6/superdex_physics/libraries/mochi/mochi_physics/src/mochi_capture.cpp) | 状态捕获标记、拓扑与构建兼容边界 |
| [superdex_physics/libraries/mochi/mochi_physics/src/mochi_common_components.h](https://github.com/facebookresearch/project_superdex/blob/1d7150946fa3f3d3fb09c2bff07eaa138cbfdee6/superdex_physics/libraries/mochi/mochi_physics/src/mochi_common_components.h) | 原生字段、API 维度与生命周期 |
| [superdex_physics/libraries/mochi/mochi_physics/src/mochi_rigid.h](https://github.com/facebookresearch/project_superdex/blob/1d7150946fa3f3d3fb09c2bff07eaa138cbfdee6/superdex_physics/libraries/mochi/mochi_physics/src/mochi_rigid.h) | 原生字段、API 维度与生命周期 |
| [superdex_physics/libraries/mochi/mochi_physics/src/mochi_simulation.cpp](https://github.com/facebookresearch/project_superdex/blob/1d7150946fa3f3d3fb09c2bff07eaa138cbfdee6/superdex_physics/libraries/mochi/mochi_physics/src/mochi_simulation.cpp) | 时间离散、积分历史及外部状态改写 |
| [superdex_python/superdex/physics/loader.py](https://github.com/facebookresearch/project_superdex/blob/1d7150946fa3f3d3fb09c2bff07eaa138cbfdee6/superdex_python/superdex/physics/loader.py) | 进程精度选择与 native payload 校验 |
| [superdex_python/superdex/physics/environment.py](https://github.com/facebookresearch/project_superdex/blob/1d7150946fa3f3d3fb09c2bff07eaa138cbfdee6/superdex_python/superdex/physics/environment.py) | 进程精度选择与 native payload 校验 |
| [superdex_physics/libraries/mochi/mochi_core/include/mochi_core/utils/rigid_body_utils.h](https://github.com/facebookresearch/project_superdex/blob/1d7150946fa3f3d3fb09c2bff07eaa138cbfdee6/superdex_physics/libraries/mochi/mochi_core/include/mochi_core/utils/rigid_body_utils.h) | rigid pose 与 DoF 转换、空间速度表示 |
