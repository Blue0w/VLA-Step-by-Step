# 实验：打开红杯场景，执行一步动作

## 预期效果

程序会打开 LIBERO-90 的「红杯放左盘」场景，读一次相机画面和机械臂状态，然后给机械臂一个小幅移动指令，再读一次观察。

- **画面**：两张 `256 × 256` 的工作区相机图。`before.png` 是重置后的画面，`after.png` 是执行一步动作后的画面。
- **终端**：任务指令、图像形状、夹爪关节位置、发出的动作，以及机械臂末端位置的变化。单步移动在画面上可能很小，可以对照打印出来的位移。

这个实验演示 `reset()` 和 `step(action)` 的作用。完整的抓取放置过程可以看[本章开头的动图](README.md)。实验画面由仿真器现场渲染，运行时无需下载演示数据。

## 在免费 Colab 上运行

1. [在 Colab 打开 Notebook](https://colab.research.google.com/github/Blue0w/VLA-Step-by-Step/blob/main/chapters/01_environment/lab/colab.ipynb)。如果你在别的分支开发，请在 Colab 的 GitHub 打开方式中选择已经推送实验代码的分支，并把 Notebook 安装单元格的 `git clone` 改为克隆该分支。
2. 在「运行时 → 更改运行时类型」里把硬件加速器设为「无」，使用免费 CPU 运行时。
3. 点击「运行全部」。第一格在 Colab 临时环境中安装依赖，第二格运行 `demo.py`，第三格并排显示 PNG。首次运行需要联网下载代码和依赖。

代码还在本地、尚未推送时，可以把仓库根目录里的 `pyproject.toml`、`src/` 和 `chapters/` 一起压成 ZIP，确保打开 ZIP 就能看到这三项。将 ZIP 上传到 Colab 的文件面板，再把本地 [lab/colab.ipynb](lab/colab.ipynb) 上传到 Colab 打开。把安装单元格的 `source_zip` 改成上传路径，例如 `'/content/vla-source.zip'`，然后运行全部。

## 在本地运行 Python 脚本

使用 Python 3.10–3.12 的独立环境，安装本章依赖。下面的命令从 **VLA-Step-by-Step 仓库根目录**运行，LIBERO 放在同级目录：

```bash
git clone https://github.com/Lifelong-Robot-Learning/LIBERO.git ../LIBERO
git -C ../LIBERO checkout 8f1084e3132a39270c3a13ebe37270a43ece2a01
python -m pip install -r chapters/01_environment/lab/requirements.txt
python -m pip install -e .
```

运行前，把下载好的 LIBERO 源码目录加到 Python 的模块搜索路径。Colab 会自动设置这一步。

```bash
export PYTHONPATH="$(cd ../LIBERO && pwd)"
```

如果使用 PowerShell，对应的命令是 `$env:PYTHONPATH = (Resolve-Path ../LIBERO).Path`。

无图形桌面的 Ubuntu 或 Debian 可以用虚拟显示器和 CPU 软件渲染，和 Colab 版采用同样的方式：

```bash
sudo apt-get install -y xvfb xauth libgl1 libglx-mesa0 libgl1-mesa-dri
MUJOCO_GL=glx PYOPENGL_PLATFORM=glx LIBGL_ALWAYS_SOFTWARE=1 MPLBACKEND=Agg \
  xvfb-run -a python chapters/01_environment/lab/demo.py
```

有图形桌面时可先用 MuJoCo 的默认渲染配置运行：

```bash
python chapters/01_environment/lab/demo.py
```

LIBERO 首次运行可能询问是否自定义数据目录，选 `n` 使用默认值即可。脚本默认把两张图保存在仓库根目录的 `outputs/chapter01/`。

## 代码在哪儿

| 文件 | 职责 |
| --- | --- |
| [`lab/demo.py`](lab/demo.py) | 执行本章实验，打印观察和位移，保存两张相机图像。 |
| [`environment.py`](../../src/vla_step/environment.py) | 封装场景加载和观察数据，供本章和后续章节复用。 |
| [`lab/colab.ipynb`](lab/colab.ipynb) | 安装云端依赖，调用同一份 Python demo，再把截图显示在 Notebook 里。 |
| [`lab/requirements.txt`](lab/requirements.txt) | 记录 Python demo 和 Colab 共用的依赖版本。 |

[返回本章笔记](README.md) · [下一章：动作表示](../02_action/README.md)
