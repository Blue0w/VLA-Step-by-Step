# 第 03 章实验 · 红杯演示查看器

## 预期效果

打开「红杯放左盘」的 HDF5 小样本，从一条演示里取出训练输入和动作标签。

| 实验 | 做什么 | 看什么 |
| --- | --- | --- |
| 查看一条轨迹 | 选 `demo_id`，浏览字段、相机帧和七维动作曲线 | 看夹爪在接近、抓取、放下时做了什么 |
| 构造训练样本 | 选动作下标 `t` 和预测步数 `K` | 看动作前的观测、状态、任务指令，以及形状为 `(K, 7)` 的标签和掩码 |
| 划分和组批次 | 用固定划分选出训练轨迹，再取两个样本 | 看训练／验证轨迹编号、批次形状，以及动作归一化前后的数值 |

## 在免费 Colab 上运行

1. [在 Colab 打开第 03 章 Notebook](https://colab.research.google.com/github/Blue0w/VLA-Step-by-Step/blob/main/chapters/03_dataset/lab/colab.ipynb)，选择 CPU 运行时。
2. 点「运行全部」。首次运行会下载仓库里的约 12.7 MB 红杯小样本。之后在同一个运行时里改参数，只需重跑参数格和结果格。
3. 先用默认值看单步样本，再改成 `t = -2`、`K = 4`。此时从倒数第二个动作起，只有两条真实动作，掩码应为 `[True, True, False, False]`。

再把 `demo_id` 换成 `demo_1` 或 `demo_2`，比较同一句指令在不同演示里的动作。日志中的 `obs[t-1]` 是发出 `actions[t]` 前能看到的画面。批次预览用训练轨迹计算前六维动作的均值和标准差，夹爪指令保留原值。

## 在本地运行

在 Python 3.10–3.12 环境中，从仓库根目录运行：

```bash
python -m pip install -e . -r chapters/03_dataset/lab/requirements.txt
python chapters/03_dataset/lab/demo.py --t -2 --horizon 4
```

本章读取已经录好的画面，CPU 即可完成，无需启动 MuJoCo。脚本默认用本章小样本，图表保存到 `outputs/chapter03/trajectory.png`。如果已经下载了同一格式的官方 HDF5，可以用 `--data` 指定文件。

## 样本来源

[本章 HDF5 小样本](media/libero90-red-mug-left-sample.hdf5)保留官方「红杯放左盘」任务的 `demo_0`、`demo_1`、`demo_2`，分别有 127、143、161 步。图像、状态和动作数组保留原值并用 gzip 压缩。小样本省去了模型 XML 等回放配置，用于读取、可视化和构造样本。 [LIBERO 原始演示](https://huggingface.co/datasets/yifengzhu-hf/LIBERO-datasets/blob/f13aa24a3da8c43c7225569f28c562979fa0e35a/libero_90/LIVING_ROOM_SCENE5_put_the_red_mug_on_the_left_plate_demo.hdf5) · [数据许可证 Apache-2.0](media/LICENSE-LIBERO.txt)

[`lab/demo.py`](lab/demo.py)负责打印和绘图，[`src/vla_step/dataset.py`](../../src/vla_step/dataset.py)负责读取样本、划分轨迹与计算统计量，供后续训练章节使用。
