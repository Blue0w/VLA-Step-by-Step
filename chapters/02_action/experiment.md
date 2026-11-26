# 第 02 章实验 · 对照关节空间和任务空间

## 预期效果

沿用第 01 章的红杯场景。两组试验从同一个仿真状态开始，每组只给一个方向发指令。比较前后画面，再对照实际的关节角变化和末端位移。

| 实验 | 怎么做 | 看什么 |
| --- | --- | --- |
| 关节空间 | 用 `JOINT_POSITION` 让 J2 朝正方向转一点。动作有 7 个关节增量和 1 个夹爪指令 | J2 转了多少度？末端在哪几个方向产生了位移？ |
| 任务空间 | 用第 01 章的 `OSC_POSE` 让末端沿 Z 轴抬高。动作有 6 个末端位姿增量和 1 个夹爪指令 | 末端抬高了多少毫米？为了抬高末端，有哪些关节一起动了？ |

两组都保持夹爪张开。输入值在 `[-1, 1]`，实际转角和位移看日志里的 `Joint changes (deg)` 和 `End-effector displacement (mm)`。

## 在免费 Colab 上运行

1. [在 Colab 打开第 01、02 章共用的 Notebook](https://colab.research.google.com/github/Blue0w/VLA-Step-by-Step/blob/main/chapters/01_environment/lab/colab.ipynb)，硬件加速器选「无」。
2. 运行开头的「准备仿真环境」，再运行「第 02 章」下的两个代码格。想从第 01 章开始，也可以点「运行全部」。
3. 先跑默认值，再把 `joint_number` 从 `2` 改成 `1`。重跑本章两个代码格，对照末端位移的方向。

## 在本地运行

先按 [第 01 章实验](../01_environment/experiment.md) 准备 LIBERO 和 MuJoCo，再从仓库根目录运行：

```bash
python chapters/02_action/lab/demo.py
```

无图形桌面时沿用第 01 章的 `xvfb-run` 和渲染配置。脚本将四张对照图保存到 `outputs/chapter02/`。
