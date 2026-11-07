# 定位与导航技术文档

基于 [ElegantLaTeX/ElegantBook](https://github.com/ElegantLaTeX/ElegantBook) 模板编写的中文教材，
面向 RoboMaster 算法组新队员，由浅入深讲解定位、建图与导航。

- **成书**：`定位与导航技术文档.pdf`（A4，约 237 页，30 章 + 2 个附录）
- **模板**：ElegantBook 4.7（`elegantbook.cls` 已随项目附带）
- **引擎**：XeLaTeX + Biber（中文由 ctex 调用系统字体）

## 编译

```bash
xelatex main.tex
biber main
xelatex main.tex
xelatex main.tex
```

或用 latexmk：

```bash
latexmk -xelatex main.tex
```

> 注意：`main.tex` 与 `chapters/*.tex` 中的 `\input` 路径均相对项目根目录，
> 请在本目录下执行编译；使用 `-output-directory` 时同样保持工作目录为根目录。

## 目录结构

```
main.tex                 # 主文件：文档类、封面、篇/章组织、参考文献
macros.tex               # 公共宏：数学符号、导读框、要点框、伪代码、花饰标题
reference.bib            # 参考文献（biblatex，numeric-comp）
STYLE.md                 # 写作规范（体例、符号表、LaTeX 约定）
elegantbook.cls          # ElegantBook 文档类
figures/                 # 封面与徽标（tools/make_cover.py 生成）
chapters/                # 30 章正文 + 前言 + 附录
  ch01_overview.tex      #   第 1 章 定位、建图与导航：全景导论
  ch02_math.tex          #   第 2 章 数学基础：从概率到李群
  ch03_sensors.tex       #   第 3 章 传感器与观测模型
  ch04_odom_intro.tex    #   第 4 章 里程计总论
  ch05_wheel.tex         #   第 5 章 轮式里程计
  ch06_imu.tex           #   第 6 章 IMU 姿态解算与航迹推算
  ch07_lidar_odom.tex    #   第 7 章 激光里程计与扫描匹配
  ch08_visual_odom.tex   #   第 8 章 视觉里程计与 VIO
  ch09_fusion.tex        #   第 9 章 多传感器融合定位
  ch10_global_loc.tex    #   第 10 章 全局定位与重定位
  ch11_slam_framework.tex#   第 11 章 SLAM 框架：前端与后端
  ch12_frontend.tex      #   第 12 章 SLAM 前端详解
  ch13_backend.tex       #   第 13 章 SLAM 后端详解
  ch14_mapping.tex       #   第 14 章 地图与建图
  ch15_cartographer.tex  #   第 15 章 2D 激光 SLAM：Cartographer
  ch16_lio_evolution.tex #   第 16 章 3D LIO：从 LOAM 到 LIO
  ch17_advanced_lio.tex  #   第 17 章 FAST-LIO2、Point-LIO 深度解析
  ch18_nav_overview.tex  #   第 18 章 导航系统总览与 Nav2
  ch19_global_planning.tex #  第 19 章 全局路径规划
  ch20_local_planning.tex#   第 20 章 局部规划与控制
  ch21_3d_nav.tex        #   第 21 章 3D 导航与 CMU 自主探索栈
  ch22_nav2_practice.tex #   第 22 章 2D 建图 + 导航完整链路
  ch23_zlocalization.tex #   第 23 章 Z-Localization 深度解析
  ch24_frontier.tex      #   第 24 章 前沿方向与展望
  ch25_ros2.tex          #   第 25 章 ROS 2 工程实践
  ch26_calibration.tex   #   第 26 章 标定与时间同步
  ch27_tuning.tex        #   第 27 章 调参与排错手册
  ch28_evaluation.tex    #   第 28 章 数据集、评测与复现
  ch29_rm.tex            #   第 29 章 RoboMaster 场景实践建议
  ch30_roadmap.tex       #   第 30 章 学习路线与资源清单
  appA_formula.tex       #   附录 A 公式与符号速查
  appB_glossary.tex      #   附录 B 术语中英对照表
outlines/                # 各篇写作提纲（历史资料，可删）
tools/                   # 封面生成、章节格式转换等脚本
tests/                   # 单章编译自检入口（test-chNN.tex）
build/                   # 编译产物
```

## 自定义

- **主题色**：`main.tex` 中 `\definecolor{structurecolor}{RGB}{22,93,155}` 及
  `main` / `second` / `third` 三个辅助色。
- **封面与徽标**：修改 `tools/make_cover.py` 中的标题与配色，运行
  `python tools/make_cover.py` 重新生成 `figures/cover.png`、`figures/logo.png`。
- **数学符号**：`macros.tex`。
- **参考文献**：在 `reference.bib` 中添加条目，正文用 `\cite{key}`。

## 说明

- 全书插图均为内嵌 TikZ/pgfplots，不依赖外部图片，可直接移植编译。
- 代码清单内的注释统一使用英文，避免 XeLaTeX 下的中文断行问题。
- 单章自检：`xelatex -output-directory=build/ch02 tests/test-ch02.tex`。

## 许可证

本书内容采用 [CC BY-NC-SA 4.0](LICENSE) 许可；`elegantbook.cls` 模板遵循 LPPL 1.3c。
欢迎在保留署名、非商业、相同方式共享的前提下自由使用与改编。
