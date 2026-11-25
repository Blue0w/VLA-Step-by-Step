# 第 03 章实验 · 查看一条 LIBERO 演示轨迹

## 预期效果

打开红杯任务的官方 HDF5 演示文件（或从其中单独抽取出的单条轨迹样本），完成下面三件事：

| 实验 | 做什么 | 看什么 |
| --- | --- | --- |
| 检查文件结构 | 打印 HDF5 里的 `demo_0` 字段名、形状与数据类型 | 对照 `actions`、相机画面与自身状态的真实维度 |
| 观察一条轨迹 | 抽取 `demo_0` 的首、中、尾帧画面，并打印/绘制 7 维动作曲线 | 看动作如何从靠近杯子过渡到闭合夹爪（`gripper` 变号）与抬起移动 |
| 构造样本与划分 | 按完整轨迹划分 train/val，切出长度为 `K` 的动作块并计算训练集均值方差 | 验证不同划分之间没有 `demo_id` 重叠，且反归一化能还原原始动作 |

## 环境与运行入口

本章实验需要读取 LIBERO-90 红杯任务的 `.hdf5` 演示数据（`LIVING_ROOM_SCENE5_put_the_red_mug_on_the_left_plate_demo.hdf5` 与 `..._right_plate_demo.hdf5`）。环境准备见 [第 01 章实验](../01_environment/experiment.md)。

本地 Python 入口预留在 `lab/demo.py`（对应复用模块为 [`src/vla_step/dataset.py`](../../src/vla_step/dataset.py)）。实验代码待实现，`media/` 预留用于存放单条示例轨迹与可视化配图。
