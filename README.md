# SuperDex Atlas

**理解 SuperDex 的建模、控制、物理机制与源码实现。**

[English](README.en.md) · [入门导读](docs/guide.md) · [完整课程路线](docs/curriculum.md) · [源码地图](docs/source-map.md) · [版本](docs/versions.md) · [开发任务](docs/roadmap.md)

这是 **Sim Atlas · 仿真图谱** 的独立社区学习仓库，重点覆盖 Physics/Robotics/Studio 的边界、Scene/Actor、接触几何、精度与可微求解。

提供两条完整路线：**A 应用路线**从对象与建模走向控制、机器人、传感器、学习接口与数据；**B 原理与源码路线**解释动力学、接触模型、求解器、积分、观测及扩展。当前交付是首篇导读、固定版本源码地图和后续章节计划，完整课程仍在开发。

## 从这里开始

1. 阅读[导读](docs/guide.md)，建立对象与调用关系。
2. 跟随[源码地图](docs/source-map.md)，在固定提交中核对原生字段、配置和执行路径。
3. 按[课程路线](docs/curriculum.md)选择应用或原理专题；需要环境时看[安装说明](docs/installation.md)。

当前先完成引擎知识体系与源码课程。最小 API 片段服务于理解，运行状态逐项注明；本轮没有新增仿真实验、训练、基准或独立评分器。后续实验复用 [DexLab](https://github.com/huangkiki/Dexlab) 的版本、配置和工况记录。

## 维护与来源

每章保留原生 API、版本化来源、易错点和阅读练习。各 Atlas 仓库独立，不需要安装其他 Atlas 或 DexLab。教程进度和 DexLab 实验证据覆盖分别记录，不据此给引擎排名。

[官方源码基线](https://github.com/facebookresearch/project_superdex/tree/1d7150946fa3f3d3fb09c2bff07eaa138cbfdee6) · [贡献](CONTRIBUTING.md) · [来源与许可](THIRD_PARTY.md)
