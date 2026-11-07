# 第 III 部分「3D LIO 深度解析」详细提纲（writer-lio 专用）

你负责 `chapters/ch16_lio_evolution.tex` 与 `chapters/ch17_advanced_lio.tex` 共 2 章，但这两章是全书技术含量最高的部分，篇幅可以到 14–18 页。

**动笔前必须读**：`STYLE.md`、`main.tex`、`macros.tex`。只改这 2 个文件。第 2、6、7、13 章分别已完成/将由他人完成，你**假设**它们已定义：高斯噪声、泰勒展开、雅可比、最小二乘、ESKF、IMU 预积分、点到面残差、因子图。用到时引用章 label（`\ref{ch:06-imu}` 等），不要引用它们的 eq/sec label。

**本部分最高优先级**：用户点名 FAST-LIO、Point-LIO，且要求"推导细致到最底层"。你必须把 FAST-LIO2 的 IMU 传播、迭代 EKF、点到面观测雅可比、iKD-Tree 增量结构，以及 Point-LIO 的逐点更新讲清楚，公式逐步推导，不能只给结论。

---

## 第 16 章 3D 激光惯性里程计：从 LOAM 到 LIO（ch16_lio_evolution，约 8 页）

目标：给读者一条清晰的演化脉络，理解每个算法"解决了前一个的什么问题"。

1. **为什么需要 LIO**：3D 场景、2D Cartographer 的局限、纯激光里程计在退化/快速运动下的问题、IMU 的高频与短时精度。给出 LiDAR+IMU 互补表（频率、精度、失效场景）。
2. **去畸变（Deskewing）**：为什么 10 Hz 的一帧点云内部点的时间差可达 100 ms；匀速模型去畸变公式；IMU 辅助去畸变的分段线性/三次样条思想。给一个"点云被拉花"的示意。
3. **演化时间线**（画一张时间线图或表）：
   - **LOAM (2014)**：特征提取（线/面）、帧间匹配、帧到地图；无 IMU；优缺点。
   - **LeGO-LOAM (2018)**：地面分割 + 聚类 + 两步优化（地面/非地面），轻量化，适合嵌入式。
   - **LIO-SAM (2020)**：紧耦合 + 因子图；IMU 预积分因子、激光里程计因子、GPS 因子、回环因子；用 GTSAM 优化。给出因子图示意与"为什么用因子图而不是滤波器"的讨论。
   - **FAST-LIO (2021)**：紧耦合 IEKF、特征提取、点到面。
   - **FAST-LIO2 (2022)**：去掉特征提取、直接原地点云配准、iKD-Tree 增量地图。
   - **Point-LIO (2023)**：逐点更新、无帧累积、抗 IMU 饱和。
   - **VoxelMap (2022)**：自适应体素 + 平面模型 + 概率地图。
   - **FAST-LIVO / FAST-LIVO2 / R3LIVE**：加入视觉，一句话定位与适用场景。
   每个算法给：核心思想（1 段）、数据流（1 个框）、优点/缺点（2 行）、典型场景、引用。
4. **两条技术路线**：特征法（LOAM/LeGO-LOAM/FAST-LIO）vs 直接法（FAST-LIO2/Point-LIO/KISS-ICP）；滤波 vs 优化。用一张二维分类表。
5. **紧耦合到底"紧"在哪**：从"松散地把 IMU 积分结果当位姿初值"到"把 IMU 状态与 LiDAR 观测放进同一个估计器"；用公式说明松耦合是级联，紧耦合是联合估计。引用 `shan2020liosam`、`xu2022fastlio2`。
6. **选型建议**：一张决策表（算力、场景、频率、是否需要回环、是否要建图、是否有 IMU 饱和风险）。
7. **小结/练习/延伸阅读**。

图：演化时间线；LIO-SAM 因子图；松耦合/紧耦合对比图（可选 2 张）。

---

## 第 17 章 FAST-LIO2、Point-LIO 与先进 LIO 深度解析（ch17_advanced_lio，约 10 页）

本章必须"源码级"：每个公式都要能对应到代码里的变量。

1. **FAST-LIO2 总体架构**：输入（LiDAR 点云 + IMU）、两个模块（IMU 传播、迭代 EKF 更新）、输出（高频 odom + 去畸变点云 + 地图）。给架构图。
2. **状态定义**：
   $$\bm{x}=[\bm{R},\bm{p},\bm{v},\bm{b}_g,\bm{b}_a,\bm{g}]$$
   说明为什么把重力放进状态（在线估计重力，抗初始姿态误差）。
3. **IMU 运动学与传播**（逐步推导）：
   - 连续运动方程
     $$\dot{\bm{R}}=\bm{R}[\bm{\omega}]_\times,\quad \dot{\bm{p}}=\bm{v},\quad \dot{\bm{v}}=\bm{R}\tilde{\bm{a}}+\bm{g},\quad \dot{\bm{b}}_g=\bm{n}_{bg},\quad \dot{\bm{b}}_a=\bm{n}_{ba},\quad \dot{\bm{g}}=0$$
   - 离散传播（用指数映射），给出 $\bm{R}_{k+1}=\bm{R}_k\exp([\bm{\omega}_k\Delta t]_\times)$ 的推导。
   - 误差状态传播：$\delta\dot{\bm{x}}=F\delta\bm{x}+G\bm{n}$，写出完整的 $F$ 矩阵（$15\times15$ 或 $18\times18$，含重力）分块形式，并**逐块解释来源**。
4. **迭代扩展卡尔曼滤波（IEKF）**：
   - 先给标准 EKF 预测/更新，再推导 IEKF：在更新步对测量方程反复线性化
     $$\bm{x}_{k+1}=\bm{x}_k\oplus K(\bm{z}-h(\bm{x}_k))$$
     写出迭代公式、收敛判据、与 EKF 的区别。
   - 说明 FAST-LIO2 的"先验来自传播、观测来自点面残差"的融合方式。
5. **点到面观测模型与雅可比**（重点）：
   - 残差 $r_i=\bm{n}_i^{\top}(\bm{R}\bm{p}_i+\bm{t}-\bm{q}_i)$，其中 $\bm{q}_i,\bm{n}_i$ 来自地图平面。
   - 推导 $\partial r_i/\partial \delta\bm{x}$（对姿态用右扰动/左扰动，写清楚假设），给出 $1\times 18$ 的雅可比分块，逐项解释。
   - 说明多个点如何组成 $H$ 与 $R$，以及为什么用点到面而不是点到点。
6. **iKD-Tree 增量地图**：
   - 为什么普通 KD-Tree 每帧重建太慢（复杂度 $O(n\log n)$）。
   - iKD-Tree 的增量插入、box-wise 操作、惰性删除（lazy delete）、并行化（OpenMP）；给一个插入流程伪代码。
   - 说明"地图只增不减"带来的内存问题与对策。
7. **Point-LIO 的核心差异**（重点，用户点名）：
   - 问题：FAST-LIO 需要一帧点云累积后更新，若 IMU 饱和/剧烈运动，帧内运动无法建模。
   - Point-LIO：**每个点到达就做一次更新**（$O(1)$ 状态更新），点的时间戳直接用于传播；无帧累积。
   - 推导逐点更新的状态传播与更新公式；说明"随机过程模型"如何替代 IMU 积分（当 IMU 不可信时把 IMU 读数当作观测）。
   - 抗 IMU 饱和的机理；代价：对单点噪声敏感、需要更谨慎的外点剔除。
   - 与 FAST-LIO2 的对比表（更新频率、计算量、鲁棒场景、内存、实现复杂度）。
8. **VoxelMap 与地图表示**：自适应体素（八叉树细分直到平面性）、平面参数与协方差、概率更新；与 iKD-Tree 的对比。
9. **FAST-LIVO2 简述**：LiDAR-惯性-视觉紧耦合，点到面 + 光度误差，适合退化场景；一句话说明适用条件。
10. **代码导览**：给出一张"论文公式 ↔ 代码文件/函数"对照表（如 `IMU_Processing.hpp`、`laserMapping.cpp`、`ikd-Tree`），帮助读者读源码（不必给完整代码，给 10–20 行关键片段即可）。
11. **实测经验**：参数敏感性（`filter_size_surf`、`filter_size_map`、`cube_side_length`、`point_filter_num`）、常见发散原因、CPU/内存量级。
12. **小结/练习/延伸阅读**。

图：FAST-LIO2 架构图；IEKF 迭代示意；iKD-Tree 增量插入示意；Point-LIO 逐点更新时序图（选 3 张）。

---

## 通用要求

1. 每章 `\chapterintro{...}`；结尾 `本章小结`、`思考与练习`、`延伸阅读`。
2. 只引用 `reference.bib` 中已有的 key。本部分推荐：`zhang2014loam,shan2018lego,shan2020liosam,xu2021fastlio,xu2022fastlio2,he2023pointlio,yuan2022voxelmap,yuan2022fastlivo,yuan2024fastlivo2,lin2022r3live,shan2021lvisam,chen2023dlio,vizzo2023kissicp,sola2017eskf,forster2017preintegration,dellaert2017factorgraphs`。
3. 不要引用其他章的 eq/sec label，只引章 label；自己的公式要充分 label。
4. 自检：`xelatex -interaction=nonstopmode -halt-on-error -output-directory=build/ch16 tests/test-ch16.tex`，ch17 同理。
5. 完成后 `send_message` 向 lead 汇报：页数、自检结果、不确定/需要 Lead 复核的公式。
