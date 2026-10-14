# 读懂 SuperDex 的 solver 配置

**建议先修：**先沿 [Physics-Based Simulation 中文伴读路线](https://github.com/huangkiki/sim-learning/blob/main/docs/physics-based-simulation.md)建立离散化、优化、接触和摩擦基础，再读本引擎的具体配置。

[课程路线](curriculum.md) · [共同概念：Sim Learning](https://github.com/huangkiki/sim-learning) · [English summary](#english-summary) · [验证范围](validation-solver-reading.md)

本章面向熟悉 VLA、WAM、RL 训练与机器人任务的工程师和硕博。你已经知道 policy 输出 action、仿真返回 observation；这里补上 `scene.step(h)` 内部的数值层次。读完后，应能解释 DexLab 的一条 SuperDex 配置、按矩阵/模型条件缩小候选范围，并从残差与执行证据诊断异常。推导与完整源码链继续阅读 [E3 接触与求解](contact-solvers-forces.md)和 [E6 柔性实现与可微边界](extensions-boundaries.md)。

## 1. 先把一行配置拆开

设想一个夹爪夹住方块：接触变形、摩擦、机器人状态与驱动目标共同决定下一时刻。像阅读训练配置中的 optimizer、precision、batch size 一样，不能把下面各项都当成一个层级的算法。

| DexLab 名称 | 它回答的问题 | 原生入口或解读位置 |
|---|---|---|
| `experimental-shell` | 这个柔性物体如何表示与产生内力？ | `experimental.create_shell_actor`，第 6 节 |
| `Newton`、`BFGS`、`SR1` | 如何迭代求解当前隐式阶段的非线性方程？ | `SolverParams.non_linear_solver`，第 2 节 |
| 13 个线性选项 | 每次迭代的局部线性方程怎么解？ | `SolverParams.linear_solver`，第 3 节 |
| `AUTO` | 由哪条规则选择线性实现？ | `GetIslandNewtonParams`，第 4 节 |
| `C1_REGULARIZED`、`CINF_REGULARIZED` | 低速摩擦怎样平滑？ | `experimental_eval.friction_model`，第 5 节 |
| `FP64` | 核心/绑定使用哪种浮点精度？ | 匹配的 double payload 与导入前精度选择，第 6 节 |
| `1.0.0` | 哪个发行包、构建与实验记录？ | 第 7 节的身份链 |

例如 `NEWTON / GMRES / C1_REGULARIZED / FP64` 可以读作：“外层使用 Newton 形式的更新；每步用 GMRES 解线性子问题；采用 C1 摩擦平滑；记录的是 FP64 构建。”它没有同时告诉你材料参数、时间步长、积分方法、残差容差、实际终止原因或任务成功率。`experimental-shell` 也不等于“另一个与 Newton 竞争的约束 solver”。

这些名字来自 [DexLab 固定分类说明][taxonomy]；该表的范围是已登记配置标签，不是已验证算法名录。特别是 SuperDex 的 `CG` 在这里是**线性**子求解器，不能直接与 MuJoCo 的非线性 CG 当作同一比较轴。

## 2. 外层方法：每次构造局部近似，再尝试更新

把已经选定时间离散、接触与材料模型后的方程记为 $R(x)=0$。$x$ 代表本次求解的状态参数，$R$ 是残差。一次外层迭代的教学形式是：

$$
H_k\Delta x_k=-R(x_k),\qquad x_{k+1}=x_k\oplus\alpha_k\Delta x_k.
$$

$H_k$ 是残差导数或其近似，$\alpha_k$ 是线搜索比例；$\oplus$ 提醒我们旋转等变量有原生增量规则，不是把任意 pose 数组直接相加。线搜索比例不是物理时间步长。源码先解正号右端，再施加负增量，与此教学写法一致。[求解循环][newton]和 [E3 第 8 节](contact-solvers-forces.md#8-非线性算法线性算法与-warm-start)说明重装配、PSD 与失败重试。

| 外层选项 | 怎样产生下一次局部矩阵 | 阅读时必须带上的条件 |
|---|---|---|
| `NEWTON` | 使用装配导数；按周期重装配，也可跨迭代复用 | 名字不保证每项都是精确 Hessian；投影、拟合和惯性分支另读 |
| `BFGS` | 从装配矩阵起步，用步长与残差变化作低秩更新 | `d_residual_assembly_period > 1` 才留下组装之间的更新机会；失败可提前重启 |
| `SR1` | 用对称秩一修正更新局部模型 | 同样依赖装配周期和重启；矩阵性质与稳定性不能只按名称判断 |

原生参数名是 `non_linear_solver.solver_type` 与 `non_linear_solver.d_residual_assembly_period`，定义见 [Python 契约][api]和 [非线性参数][nonlinear]。

**必须保留的实测限定：**DexLab 冻结斜面报告中的 BFGS/SR1 两行，请求枚举虽不同，但有效读回都是 `d_residual_assembly_period=1`。固定原生实现明确发出 Newton 等价提示；每次重装配使两次组装之间的低秩更新没有发挥空间。因而该批不能算另外独立验证了 BFGS 与 SR1，也不能用相同成绩声称三种一般算法等价。[原始报告][incline] · [原生条件判断][newton]

这是一项具体配置的解释。它既不删除原始枚举记录，也不否定更长装配周期下真正的拟 Newton 路径；后者的运行证据本章没有补做。

## 3. 内层方法：解的是一个线性子问题

给定当前 $H_k$ 与 $R_k$ 后，内层只负责近似求出 $\Delta x_k$。例如线性残差是 $r_k=-R_k-H_k\Delta x_k$。线性残差小不保证整个非线性残差已小；两者都小也不保证建模正确。

下表覆盖冻结 DexLab 表中的全部 13 个选项，名称使用原生 Python 枚举拼写。SPD 指对称正定。这里给出理解与筛选条件，不承诺某个方法在你的 workload 上更快。枚举/条件由 [LinearSolverParams][linear-params]定义，具体分派与构建条件继续核对 [LinearSolver][linear]。

| 配置标签 | 直觉与主要条件 |
|---|---|
| `CG` | 在 SPD 系统上沿共轭方向迭代；此实现主要并行矩阵向量乘，不能据此假定所有操作都并行 |
| `ASYNC_CG` | 重排 CG 以重叠矩阵向量乘与其他工作；实验性，有限精度稳定性弱于经典 CG，仍要求 SPD |
| `AUGMENTED_CG` | 利用回收的 Krylov 子空间补充 CG；实验性，要求 SPD 及 Eigen 构建 |
| `PARALLEL_CG` | 将更多 CG 运算并行化；要求支持并行求解的预条件器和 SPD，原生契约明确非确定性 |
| `CUDA_CG` | CUDA 上的 CG 子求解；要求 SPD、CUDA 构建及兼容预条件器 |
| `GMRES` | 在 Krylov 子空间中降低残差；可面向非对称系统，要同时查看 restart 与预算 |
| `CUDA_GMRES` | CUDA 上的 GMRES 子求解；构建与预条件器条件仍需满足 |
| `MINRES` | 面向对称系统的最小残差迭代；可用于对称不定问题，预条件器也要满足适用条件 |
| `LDLT` | 对称矩阵直接分解；该实现无 pivoting，病态或不定时仍有稳定性风险 |
| `LU` | 一般矩阵直接分解；此路径为无 pivoting 的稠密 LU，大系统成本高 |
| `EXPERIMENTAL_CUDA_SPARSE_CHOLESKY` | CUDA 稀疏/块稀疏 Cholesky，要求 SPD；实验性 |
| `EXPERIMENTAL_CUDA_SPARSE_LDLT` | CUDA 稀疏/块稀疏对称分解；实验性，还要求 cuDSS |
| `EXPERIMENTAL_CUDA_SPARSE_LU` | CUDA 稀疏/块稀疏 LU；实验性，不能仅凭名字推断与 CPU LU 的相同数值行为 |

迭代方法的预条件器用于改善求解条件；它不是另一个接触模型。直接分解也有舍入和条件数问题，不能理解成“精确到真实物理”。`CUDA_` 只说明这条线性实现的设备路径，不能说明碰撞检测、装配、观测和渲染全部在 GPU；源码中还存在 CPU/GPU 数据传输。[E5 性能与数据边界](batch-learning-data.md)进一步拆解这些成本。

实际选择顺序是：先确认矩阵性质与构建可用性，再记录预条件器/容差/预算，最后在同一模型和任务上比较收敛与物理观测。这里的静态阅读只能完成前两项的源码理解，不能代替后续原生运行验收。

## 4. AUTO、配置读回与实际执行是三份信息

此固定源码在每个 **island** 的 `GetIslandNewtonParams` 中处理线性 `AUTO`：自由度不超过 50 时选择 LDLT 并取消预条件器；超过 50 时选择 CG。island 是当前有耦合的子问题，不是“整个场景物体数”或“机器人关节数”的别名。这是一条源码启发式，不是自动性能评测，也没有按显卡可见性自动选 CUDA。[实际分支][island]

学习时把证据分成三栏：

| 证据 | 能回答什么 | 仍不能回答什么 |
|---|---|---|
| 应用请求 `AUTO` | 用户传入了什么 | 最终是否接受、每个 island 的选择 |
| `scene.get_solver_params()` | Scene 保存的有效参数；例如装配周期、friction 枚举 | 内部实际分支并不因此自动变成可观测字段 |
| 对应构建源码与执行遥测 | 源码支持怎样推断、运行究竟观测到了什么 | 缺失的历史遥测不能由当前默认值补写 |

下面是原创的最小只读片段，假设调用者已拥有一个原生 `scene`。它只做语法核验，**没有导入 SuperDex、创建场景或执行**。枚举 `.name` 与字段均按 [原生 stub][api]核对；返回字段刻意称 `linear_setting`，避免把 `AUTO` 的参数读回误写成已执行的 LDLT。

```python
def read_solver_settings(scene):
    params = scene.get_solver_params()
    return {
        "outer_setting": params.non_linear_solver.solver_type.name,
        "assembly_period": params.non_linear_solver.d_residual_assembly_period,
        "linear_setting": params.linear_solver.solver_type.name,
        "preconditioner_setting": params.linear_solver.preconditioner_type.name,
        "friction_setting": params.experimental_eval.friction_model.name,
        "integration_setting": params.integration_method.name,
    }
```

DexLab 报告也明确：该批 AUTO 内部分支仍属源码推断，统计没有直接暴露该字段。不要将上面片段改写成能证明内部执行路径的“验证器”。[报告边界][incline]

## 5. C1 与 C∞：改变低速摩擦响应

夹爪抓住方块后，理想静摩擦可以在严格零滑移处承担一段范围内的切向载荷。正则化摩擦则把零附近的非光滑关系变成平滑响应，便于隐式求解，但可能出现微小滑动/蠕动。因此改 `C1_REGULARIZED` 为 `CINF_REGULARIZED` 是改变摩擦模型的一部分，不只是给相同方程换一个求解器。

设切向位移大小为 $r$，平滑尺度 $\epsilon=v_0h_s>0$，其中 $v_0$ 对应 `friction_falloff_vel`，$h_s$ 是当前积分阶段的有效时长。在固定法向及基准法向强度的局部解释下，Coulomb 阻力的幅值由 $\mu p_{\rm ref}\phi(r)$ 给出：

$$
\phi_{C1}(r)=
\begin{cases}
2r/\epsilon-(r/\epsilon)^2,&0\le r<\epsilon,\\
1,&r\ge\epsilon,
\end{cases}
\qquad
\phi_{C\infty}(r)=\frac{r}{\sqrt{r^2+\epsilon^2/4}}.
$$

C1 在有限区间后到达单位幅值，C∞ 渐近接近它；平滑尺度非零时，两者在零位移的幅值均为零。C1 过渡不是整段线性 ramp。这里的 $p_{\rm ref}$ 是接触装配使用的法向基准强度，不能不看采样权重与配置就当作传感器总法向力。原生公式见 [activation 实现][activations]；接触装配、附加黏性项及量纲见 [E3 第 5 节](contact-solvers-forces.md)。

对训练的启示是：先辨认低速响应、时间步长与观测时点，再决定是否调整策略或奖励。看到慢滑，不能直接归因于 policy，也不能只增加 solver 迭代后宣称模型等同理想静摩擦。本章没有通过重新调参消除 DexLab 的失败记录。

## 6. experimental-shell 与 FP64 分别解释什么

`experimental-shell` 是 DexLab 的柔性实现标签；原生创建入口是 `experimental.create_shell_actor`。壳用三角表面上的膜/弯曲响应表达薄结构，参数包含面密度，不能把体积密度数值直接填入。它与刚体、四面体 soft actor 的自由度和材料含义不同，仍然需要积分与求解配置。官方实验性 API 与 [E6 壳材料、厚度和构建边界](extensions-boundaries.md)是深入入口；`experimental` 表示接口成熟度，不能翻译成“已有实验验证”。[原生实验性定义][experimental]

`FP64` 表示记录的双精度数值路径。固定 Python loader 通过 `SUPERDEX_PRECISION` 的选择寻找对应 double payload；应该在导入前选择，且要有匹配的绑定/核心构建。使用 NumPy 的 float64 输入不自动证明 native 核心是双精度。[loader][loader] · [精度环境变量][environment]

FP64 可以降低舍入误差，但不会补齐错误材料、过粗几何、过大时间步长、未收敛的非线性迭代或缺少 CUDA 支持。也不能从“FP64 斜面批次”推广出壳模型的可微性；E6 明确区分各 Actor 的反向路径支持。

## 7. 版本对齐与 DexLab 证据

本章跟随 DexLab 已登记的 **SuperDex 1.0.0**，官方源码固定到 `1d7150946fa3f3d3fb09c2bff07eaa138cbfdee6`，与本仓已有 E1–E6 阅读提交一致，因此本章无需迁移原生字段版本。但证据层仍有差别：旧课程记录的是候选包和源码；DexLab 后续报告记录了特定 wheel/core/binding 的身份审计。本次只阅读该审计，没有重新安装或独立复现。

| 身份层 | 固定来源与限制 |
|---|---|
| 分类与实验报告 | DexLab `7e4a0774efb4f8b332e866e1495e032b4969c8aa` 的[分类说明][taxonomy]及[斜面报告][incline]；后续表格新增配置须重新对照 |
| 已报告的发行包 | [official-proof.json][proof]分别记录 `superdex-physics==1.0.0` 与 `superdex-physics-fp64==1.0.0`，含 wheel SHA-256、构建提交和 mapped native 哈希 |
| 教程源码 | 官方提交 `1d71509…`；文件身份沿用并复核 [sources.json](sources.json)，不把包版本号当成全部构建选项 |
| 本次验证 | 文本、原生字段、固定来源身份及语法检查；没有 native import、JIT、仿真、训练或性能运行 |

冻结报告中的五个 CUDA 选项在 `set_solver_params` 阶段被该 FP64 wheel 拒绝，物理时间尚未推进。源码有这些实现，和该 wheel 没有 CUDA 支持可以同时成立；这不是五次物理任务失败，更不是 SuperDex 全部构建都不支持 CUDA。[原始报告][incline] · [Scene 配置校验][scene]

阅读实验时还要区分“无效记录”“有效但不通过物理要求”和“已获得任务覆盖资格”。该斜面批次没有消除所有静态蠕动失败，也没有得到 coverage-v1 可靠覆盖资格；本章不重新发布跨引擎名次，完整数值与负例留在原报告。

## 8. 诊断练习与答案

1. **记录是 `BFGS / AUTO / C1_REGULARIZED`，装配周期为 1；可以说 BFGS 比 Newton 更稳吗？**
   答：不可以。先记录请求枚举与有效读回；此固定实现对应 Newton 等价步。需要真正发生低秩更新的配置与独立运行证据才可比较一般拟 Newton 行为。
2. **80 DoF 的单个 island 配置 AUTO，机器有 GPU。源代码预测哪条线性分支？**
   答：固定源码选择 CG。GPU 可见性不参与这里的 AUTO 规则；这仍是源码预测，要与运行遥测分栏。
3. **`CUDA_GMRES` 在设置参数时被拒绝，任务计数能写成一次物理失败吗？**
   答：不能。先检查 wheel 的 CUDA 能力与预条件器兼容性；这是准入/配置失败，没有时间推进，不能混入已运行工况的物理失败分母。
4. **线性残差很小，但 actor/scene 报告 STOPPED，能直接保留为收敛样本吗？**
   答：不能。检查非线性残差、停止原因与预算，并独立核对力/状态一致性；STOPPED 不等于 CONVERGED。详见 E3 的终止语义。
5. **提高到 FP64 后，夹持仍慢滑，下一步只需要把 CG 换成 LU 吗？**
   答：没有这个结论。先看模型是否使用平滑摩擦、平滑尺度、步长和收敛记录，再查观测力是否匹配状态时刻；精度、模型、离散和迭代误差分别诊断。
6. **shell 标注与 Newton 标注能放在一张同级 solver 排名中吗？**
   答：不能。前者指柔性表示/材料实现，后者指非线性解法；比较前需要固定任务、表示、参数与证据标准。

继续学习：[原生对象导读](guide.md) → [E3 接触/装配/求解/力观测](contact-solvers-forces.md) → [E6 壳/可微/扩展](extensions-boundaries.md)。本章是新入门桥梁，E7 完整安装与全路线运行审校仍暂停。

## English summary

SuperDex configuration labels span different roles: experimental shell actors, outer nonlinear methods, inner linear solves, automatic branch selection, friction regularization and floating-point precision. Read the requested setting, effective parameter readback, source-predicted branch and observed execution separately.

This guide covers every SuperDex token in the pinned DexLab taxonomy and uses the same official source commit as the existing deep lessons. It preserves the reported Newton-equivalence of BFGS/SR1 with assembly period 1, AUTO's source-inferred island selection, and the five CUDA options rejected by the recorded FP64 wheel before stepping. The native snippet is syntax checked only. No new engine execution, installation, JIT, training or performance evidence is claimed; E7 remains paused.

[taxonomy]: https://github.com/huangkiki/Dexlab/blob/7e4a0774efb4f8b332e866e1495e032b4969c8aa/docs/solver-taxonomy.zh-CN.md
[incline]: https://github.com/huangkiki/Dexlab/blob/7e4a0774efb4f8b332e866e1495e032b4969c8aa/docs/superdex-incline-results.zh-CN.md
[proof]: https://github.com/huangkiki/Dexlab/blob/7e4a0774efb4f8b332e866e1495e032b4969c8aa/docs/evidence/superdex-incline/official-proof.json
[api]: https://github.com/facebookresearch/project_superdex/blob/1d7150946fa3f3d3fb09c2bff07eaa138cbfdee6/superdex_physics/libraries/mochi/mochi_physics/pybind/stubs/public/mochi_physics/__init__.pyi
[newton]: https://github.com/facebookresearch/project_superdex/blob/1d7150946fa3f3d3fb09c2bff07eaa138cbfdee6/superdex_physics/libraries/mochi/mochi_core/src/solvers/newton_solver.cpp
[nonlinear]: https://github.com/facebookresearch/project_superdex/blob/1d7150946fa3f3d3fb09c2bff07eaa138cbfdee6/superdex_physics/libraries/mochi/mochi_core/include/mochi_core/solvers/nonlinear_solver_params.h
[linear-params]: https://github.com/facebookresearch/project_superdex/blob/1d7150946fa3f3d3fb09c2bff07eaa138cbfdee6/superdex_physics/libraries/mochi/mochi_core/include/mochi_core/solvers/linear_solver_params.h
[linear]: https://github.com/facebookresearch/project_superdex/blob/1d7150946fa3f3d3fb09c2bff07eaa138cbfdee6/superdex_physics/libraries/mochi/mochi_core/include/mochi_core/solvers/linear_solver.h
[island]: https://github.com/facebookresearch/project_superdex/blob/1d7150946fa3f3d3fb09c2bff07eaa138cbfdee6/superdex_physics/libraries/mochi/mochi_physics/src/mochi_simulation.cpp
[activations]: https://github.com/facebookresearch/project_superdex/blob/1d7150946fa3f3d3fb09c2bff07eaa138cbfdee6/superdex_physics/libraries/mochi/mochi_core/include/mochi_core/utils/activations.h
[experimental]: https://github.com/facebookresearch/project_superdex/blob/1d7150946fa3f3d3fb09c2bff07eaa138cbfdee6/superdex_physics/libraries/mochi/mochi_physics/include/mochi_physics/mochi_physics_experimental.h
[loader]: https://github.com/facebookresearch/project_superdex/blob/1d7150946fa3f3d3fb09c2bff07eaa138cbfdee6/superdex_python/superdex/physics/loader.py
[environment]: https://github.com/facebookresearch/project_superdex/blob/1d7150946fa3f3d3fb09c2bff07eaa138cbfdee6/superdex_python/superdex/physics/environment.py
[scene]: https://github.com/facebookresearch/project_superdex/blob/1d7150946fa3f3d3fb09c2bff07eaa138cbfdee6/superdex_physics/libraries/mochi/mochi_physics/src/mochi_scene.cpp
