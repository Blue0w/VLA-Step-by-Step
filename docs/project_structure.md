# 目录与文件职责

本文记录项目的文件分工，作为学习和开发时的导航。尚未完成的章节在这里列出计划职责。

## 项目目标

围绕 LIBERO 中的红杯抓取放置任务，逐步实现视觉编码、语言编码、状态编码、注意力融合与连续动作预测。先跑通放到左盘，再加入放到右盘，通过不同指令验证语言作用。使用对应官方演示训练，在仿真环境中闭环评估；训练与推理分别以单张 RTX 4090 为资源上限，实际效果与资源开销需要实验验证。

## 目录总览

```text
VLA-Step-by-Step/
├── .gitignore                    # 排除数据、实验产物、本地环境和缓存
├── .vscode/
│   └── settings.json             # VS Code 将 Markdown 中粘贴的图片保存到 pictures/
├── README.md                     # 项目介绍、学习入口、最终效果与运行入口
├── pyproject.toml                # Python 包配置与依赖
├── docs/
│   └── project_structure.md      # 本文：目录、职责、学习顺序和维护规则
├── chapters/                     # 按顺序学习：每章笔记和局部实验
│   ├── 00_overview/
│   │   ├── README.md             # 任务、整体架构、数据流、预期效果
│   │   └── media/                # 本章配图
│   ├── 01_environment/
│   │   ├── README.md             # LIBERO 安装、场景、相机和控制接口
│   │   ├── experiment.md         # 预期效果和 Colab／本地运行步骤
│   │   ├── lab/
│   │   │   ├── demo.py           # 打开杯子场景、查看图片和观察数据
│   │   │   ├── colab.ipynb       # 在 Colab 打开场景并执行手写动作
│   │   │   └── requirements.txt  # 第 01、02 章共用的仿真实验依赖
│   │   └── media/
│   │       ├── libero90-red-mug-left.gif  # 笔记内嵌的仿真动图
│   │       └── libero90-red-mug-left.mp4  # 原始仿真视频
│   ├── 02_action/
│   │   ├── README.md             # 状态、7 维动作、控制器缩放与动作块
│   │   ├── experiment.md         # 关节空间与任务空间对照实验说明
│   │   ├── lab/
│   │   │   ├── demo.py           # 执行两组试验并记录关节和末端变化
│   │   │   └── colab.ipynb       # 在 Colab 运行两种控制方式的对照
│   │   └── media/                # 本章实验演示素材
│   ├── 03_dataset/
│   │   ├── README.md             # HDF5 轨迹结构、样本切片、轨迹划分与归一化
│   │   ├── experiment.md         # 查看单条轨迹与样本构造实验说明
│   │   ├── lab/
│   │   │   └── demo.py           # Python 实验入口（预留）
│   │   └── media/                # 本章单条轨迹样本与可视化素材
│   ├── 04_vision/
│   │   ├── README.md             # 图片预处理、视觉编码与空间 token
│   │   └── demo.py               # 展示图片处理过程和视觉特征形状
│   ├── 05_language/
│   │   ├── README.md             # 分词、词表、嵌入、词序与填充掩码
│   │   └── demo.py               # 将左右指令转换成语言 token
│   ├── 06_attention/
│   │   ├── README.md             # Q/K/V、自注意力、Transformer 与多模态融合
│   │   └── demo.py               # 注意力计算示例、融合与权重可视化
│   ├── 07_policy/
│   │   ├── README.md             # 特征汇总、动作头与完整策略
│   │   └── demo.py               # 复用已有模块、完成一次前向计算
│   ├── 08_training/
│   │   ├── README.md             # 损失、反向传播、验证和模型保存
│   │   └── demo.py               # 展示一次训练更新
│   └── 09_evaluation/
│       ├── README.md             # 闭环执行、成功率、语言对照和失败分析
│       └── demo.py               # 加载模型并运行一个评估回合
├── src/
│   └── vla_step/                 # 可复用的正式实现
│       ├── __init__.py           # 包入口，按需导出公共接口
│       ├── environment.py        # LIBERO 环境适配、观察提取和任务成功判定
│       ├── action.py             # 动作归一化、还原与动作块处理
│       ├── dataset.py            # 数据读取、轨迹划分与样本构造
│       ├── vision.py             # 图像预处理与视觉编码器
│       ├── language.py           # 分词器、词表与语言编码器
│       ├── attention.py          # 注意力和 Transformer 基础组件
│       ├── fusion.py             # 状态编码、模态对齐、位置/模态信息与融合
│       ├── policy.py             # 动作头、完整模型组装与动作预测接口
│       └── training.py           # 损失、训练/验证循环与检查点管理
├── scripts/                      # 完整工作流的命令行入口
│   ├── add_picture.ps1           # 从 Windows 剪贴板或文件添加编号图片
│   ├── prepare_data.py           # 数据准备、检查、划分与训练统计量生成
│   ├── train.py                  # 读取配置并启动完整训练
│   ├── evaluate.py               # 多回合闭环评估，保存指标和视频
│   └── play.py                   # 接收支持的文字指令，显示机械臂执行
├── configs/
│   └── cup.yaml                  # 杯子任务、数据、模型、训练与评估配置
├── tests/                        # 关键接口、数据处理和行为验证
├── pictures/                     # 截图粘贴和编号脚本的默认保存目录
├── assets/                       # 其他小型示例和演示素材
├── data/                         # 原始/处理后的数据，本地生成，不纳入 Git
└── outputs/                      # 权重、日志、评估结果，本地生成，不纳入 Git
```

## 如何阅读与复用代码

- 从 `chapters/00_overview/README.md` 开始，按编号学习。每章 README 讲解原理和操作，本章 `demo.py` 提供局部实验。
- 正式模块只在 `src/vla_step/` 中维护一份。后续模块直接导入前面的实现，不复制各章代码。
- 例如 `policy.py` 导入 `vision.py`、`language.py` 和 `fusion.py`；`fusion.py` 使用 `attention.py` 提供的基础组件。
- 章节实验也导入 `vla_step` 包。使用 `pip install -e .` 安装项目后可以直接导入，无需修改导入路径。
- `scripts/` 负责配置和工作流编排，具体算法保留在 `src`，避免与章节演示重复实现。

状态编码第一版放在 `fusion.py`，后续如果需要独立教学或复用，再拆为单独文件，并同步更新本文。

## 每章笔记的统一结构

1. 本章要解决的问题，以及依赖哪些前置章节。
2. 输入与输出：含义、形状、单位和一个具体例子。
3. 必要原理与对应 `src` 实现的讲解。
4. 运行本章实验所需的数据、命令和环境。
5. 预期现象、常见问题与当前能力限制。
6. 本章产出如何连接下一章。

需要区分“模块能够计算”“模型能够学习”和“策略能够完成任务”：随机初始化的编码器输出形状正确，不代表已经理解图片或语言。

## 数据、产物与维护约定

- 数据按完整轨迹划分；归一化统计量只从训练集计算。保留轨迹边界和任务身份，防止样本错配。
- 模型输入只包含图片、指令与机械臂自身状态，环境中的物体真实坐标不作为额外模型输入。
- 每次正式实验在 `outputs/` 中保存配置、权重、统计量和评估结果，使模型可以复现和重新加载。
- 章节专用的图片和视频放在本章的 `media/`。`assets/` 放其他小型素材，批量评估视频放在 `outputs/`。
- `data/` 和 `outputs/` 已通过 `.gitignore` 排除；本地 Python 环境、缓存、构建产物和 `.env` 文件也不纳入 Git。
- Git 不记录空目录；当前 `tests/`、`assets/`、`data/` 和 `outputs/` 为空，仅存在于本地。
- 文件新增、拆分或职责变化时，同步更新本文。根 README 保留本页入口，不重复维护完整目录树。

## 添加教程图片

在 VS Code 中把仓库根目录作为文件夹打开，然后在任意 Markdown 文件中粘贴截图。仓库设置会让 VS Code 将图片直接保存到根目录的 `pictures/` 并插入相对链接。遇到重名时，VS Code 会给新文件加数字后缀。若复制的是仓库内已有的图片文件，VS Code 会直接引用原文件。

想把粘贴后的图片改成 `00.png`、`01.png`，可以在 VS Code 左侧的资源管理器中选中图片并按 `F2`。仓库设置会自动更新引用该图片的 Markdown 路径。

如果希望自动分配纯数字编号，在 Windows 上复制截图或图片本身，然后在仓库根目录运行下面的命令。脚本会将剪贴板图片保存为 PNG，并输出保存路径。

```powershell
powershell.exe -NoProfile -STA -ExecutionPolicy RemoteSigned -File .\scripts\add_picture.ps1
```

已有图片文件时，传入路径即可，脚本会保留原格式。

```powershell
powershell.exe -NoProfile -STA -ExecutionPolicy RemoteSigned -File .\scripts\add_picture.ps1 'C:\path\to\image.jpg'
```

编号由所有章节共享，从 `00` 开始。脚本取现有最大编号加一，例如 `00.png`、`01.jpg`、`02.png`。已引用的图片保持原名，避免 Markdown 链接失效。手动复制图片到目录时，也可以沿用相同的编号规则。

在章节的 `README.md` 中，用相对路径引用图片。下面以第 00 章为例，说明文字换成实际图片的内容。

```markdown
![本章配图](media/00.png)
```
