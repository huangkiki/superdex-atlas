# 版本与证据边界

| 身份 | 当前记录 |
|---|---|
| 阅读版本 | stable 固定提交；候选 Python 包 1.0.0 |
| 官方源码 | [facebookresearch/project_superdex](https://github.com/facebookresearch/project_superdex/tree/1d7150946fa3f3d3fb09c2bff07eaa138cbfdee6) |
| 固定提交 | `1d7150946fa3f3d3fb09c2bff07eaa138cbfdee6` |
| 源文件身份 | [sources.json](sources.json) 中的 Git blob 已与下载文件核对 |
| 已完成检查范围 | 文档相对链接、固定来源与源码文件身份；API 片段只做语法检查 |
| 原生运行与实验 | 本阶段未开展 |
| 完整专题 | [课程目录](curriculum.md)中明确标为待开发 |

固定文件身份不能证明整个引擎已审查，也不能证明候选二进制与源码具有相同构建配置。核心、绑定、插件和宿主身份分别记录。当前版本的默认值不用于补填 DexLab 历史配置。

[DexLab](https://github.com/huangkiki/Dexlab) 保留实验版本与协议；本仓不修改或追认其结果。

新增 [solver 配置解读](solver-reading-guide.md)对齐 DexLab 固定报告的 `superdex-physics==1.0.0` / `superdex-physics-fp64==1.0.0` 身份记录，官方阅读提交仍为 `1d71509…`，与既有课程相同。报告审计与本次独立验证分开：本次未安装或复现 wheel；具体来源、版本差异与限制见该章第 7 节。
