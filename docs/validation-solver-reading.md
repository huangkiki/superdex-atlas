# Learning 改名与 solver 配置解读：验证记录

任务：[Sim Learning #1](https://github.com/huangkiki/sim-learning/issues/1)。检查日期：2026-10-14；本地起点为 `767bd8e00374f810029baa94370b381f3fee1861`，分支 `autodev/learning-migration`。本次交付 [solver-reading-guide.md](solver-reading-guide.md)，以及现行品牌、导航、课程/roadmap 的对应更新。提交与远端集成由主任务统一核验，不在这里预先宣称发布。

## 范围

- 覆盖 DexLab 固定分类中的 SuperDex 全部标签：实验性壳、三种外层方法、13 种线性选项、AUTO、两种摩擦正则化和 FP64。
- 核对原生参数、只读配置片段、AUTO island 分支、装配周期为 1 的 Newton 等价条件，以及已报告的 1.0.0 wheel 身份与 CUDA 准入拒绝。
- 复用 E3/E6 深入课程，新增直觉解释、最小公式、6 道诊断练习及答案、英文摘要。
- E7 保持暂停。没有安装、native import、JIT、模型编译、仿真、渲染、数值求导、训练、性能基准或独立评分。

## 检查记录

- `git diff --check` 通过；`python scripts/check_docs.py` 通过，本仓相对 Markdown 文件链接可解析。该脚本不检查远端或锚点，未把它当成全部链接的证明。
- 新章 11 个官方源码链接逐一核对固定 Git tree 的 path/blob，并下载 blob 字节重算 Git blob SHA-1，与既有 `sources.json` 一致。仅核对本章所引用范围，没有宣称重新审查整个引擎。
- 3 个 DexLab 固定文件均通过 commit/path/blob 与实际字节身份检查：分类说明 `90db453020a00c3a5d7a5024fbb47d87cc6f15ba`，斜面报告 `46cc716d91bcdd61d12d7a6e94ee0beac515e9af`，wheel 身份文件 `be149b1cd4e3981b1f806c54bc07ec52e5a91391`。它们是报告证据，非本次重跑结果。
- 新章 reference-style 引用均有定义；两个内部/跨文件标题锚点与实际标题人工核对。21 个冻结标签（13 个线性选项另计于其中）均有正文解释，未只给名词表。
- 7 个仓库 Python 文件与 4 个完整 Markdown Python 块通过 `ast.parse`；新增片段为只读 `get_solver_params`，字段/枚举 `.name` 对照原生 stub 检查，没有执行对象代码。
- 现行 `sim-learning`、`superdex-learning` 仓库身份及总仓 Issue #1 已从 GitHub API 读回；本子任务没有进行改名或远端写入。GitHub 页面视觉呈现与最终发布由主任务另验。
- 6 份 `validation-e1` 至 `validation-e6` 对照本地起点逐字节未变。全仓旧 Atlas 命中仅来自这些历史记录和本页的例外说明。
- 自审检查公式的状态增量/线搜索含义、摩擦平滑尺度与单位、AUTO 的 island 门槛、构建与执行证据区别及 E7 暂停边界。独立主审由主任务处理，不预先写成已通过。

## 保留的历史引用

`docs/validation-e1.md` 至 `docs/validation-e6.md` 保留原有 `superdex-atlas` Issue URL、当时的 Sim Atlas 品牌、base/head 与检查结论。这些是 2026-10-09 的不可改写历史验收记录，不是现行导航。现行仓库入口为 [SuperDex Learning](https://github.com/huangkiki/superdex-learning)，历史 Issue 可从新仓同号入口访问；历史正文未因改名变更。

本次不改上游项目名、原生模块/枚举、官方源文件、实验结果或历史版本。运行未验收不会因文档通过检查变成已验收。
