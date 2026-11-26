# 第 02 章实验 · 对照关节空间和任务空间

## 预期效果

沿用第 01 章的红杯场景。两组试验从同一个仿真状态开始，每组只给一个方向发指令。比较前后画面，再对照实际的关节角变化和末端位移。

| 实验 | 怎么做 | 看什么 |
| --- | --- | --- |
| 关节空间 | 用 `JOINT_POSITION` 让 J2 朝正方向转一点。动作有 7 个关节增量和 1 个夹爪指令 | J2 转了多少度？末端在哪几个方向产生了位移？ |
| 任务空间 | 用第 01 章的 `OSC_POSE` 让末端沿 Z 轴抬高。动作有 6 个末端位姿增量和 1 个夹爪指令 | 末端抬高了多少毫米？为了抬高末端，有哪些关节一起动了？ |

两组都发送张开夹爪的指令。动作参数在 `[-1, 1]` 内，控制器每步以当时的实际角度或位置为起点更新目标：

- `joint_command = 0.8` 时，选中关节的目标角度增加 `0.8 × 0.05 = 0.04 rad`，约 2.29°。
- `z_command = 0.4` 时，末端的目标高度增加 `0.4 × 0.05 = 0.02 m`，也就是 20 mm。

`comparison_steps` 是两组各自重复发送同一条指令的最大次数。实际执行步数和整组试验的总变化见日志里的 `steps`、`Joint changes (deg)` 和 `End-effector displacement (mm)`。 [关节控制配置](https://github.com/ARISE-Initiative/robosuite/blob/v1.4.0/robosuite/controllers/config/joint_position.json) · [末端控制配置](https://github.com/ARISE-Initiative/robosuite/blob/v1.4.0/robosuite/controllers/config/osc_pose.json)

## 在免费 Colab 上运行

1. [在 Colab 打开第 02 章 Notebook](https://colab.research.google.com/github/Blue0w/VLA-Step-by-Step/blob/main/chapters/02_action/lab/colab.ipynb)，硬件加速器选「无」。
2. 点「运行全部」。Notebook 会准备仿真环境、运行两组试验，再显示日志和前后对照图。
3. 先跑默认值，再把 `joint_number` 从 `2` 改成 `1`。重跑「动手试一试」和「运行对照并查看结果」两格，对照末端位移的方向。

本章 Notebook 可以独立运行，依赖清单沿用第 01 章。如果代码还在本地，可以参照第 01 章的源码 ZIP 上传步骤，打开本章的 [`lab/colab.ipynb`](lab/colab.ipynb)。

## 在本地运行

先按 [第 01 章实验](../01_environment/experiment.md) 准备 LIBERO 和 MuJoCo，再从仓库根目录运行：

```bash
python chapters/02_action/lab/demo.py
```

本地脚本默认的 Z 轴指令是 `0.8`。如果要复现 Colab 中 `z_command = 0.4` 的设置，运行时加上 `--z-command 0.4`。

无图形桌面时沿用第 01 章的 `xvfb-run` 和渲染配置。脚本将四张对照图保存到 `outputs/chapter02/`。
