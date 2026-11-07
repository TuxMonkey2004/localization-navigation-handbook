# 《定位与导航技术文档》写作规范（所有撰稿人必读）

本文件是全书唯一的格式与内容契约。动笔前必须完整读完。任何与本书其他章节不一致的地方，以本文件为准。

---

## 0. 目标与读者

- **读者画像**：RoboMaster 算法组新队员，会 C++/Python，学过高等数学、线性代数、概率论，但**没有系统学过机器人定位与导航**。也可能有老队员用来查漏补缺。
- **目标**：读完能建立完整知识地图，理解每个算法的**问题、假设、推导、优缺点、工程落地方式**，能看懂并改 FAST-LIO / Point-LIO / Cartographer / Nav2 / Z-Localization 这类开源代码。
- **口吻**：一位有耐心的学长在讲。多用"为什么"，少用"显然"。每个新概念先回答"它解决什么问题"，再给定义，再给公式，再给例子。
- **深度要求（最重要）**：公式推导必须细致到最底层。
  - 任何数学名词**全书第一次出现**时，必须给出定义、计算式和一个具体数字例子。例如第一次出现"方差"时，要先写期望的定义式，再写方差的定义式，再解释它衡量什么，再举一个 3 个数的例子。
  - 推导不允许跳步："由上式可得"之前必须真的把代数步骤写出来。允许省略的只有纯机械的重复展开，且要用文字说明"重复展开后得到"。
  - 关键结论要说明：用了什么假设、做了什么近似、忽略了哪一阶项、近似的适用条件。
  - 每个重要公式后面用一两句话解释**每一项的物理含义**。

---

## 1. 全书结构与文件分工

```
main.tex                 # 由 Lead 维护，撰稿人禁止修改
macros.tex               # 由 Lead 维护，撰稿人禁止修改
reference.bib            # 由 Lead 维护，撰稿人禁止修改
STYLE.md                 # 本文件
chapters/chXX_*.tex      # 每个撰稿人只写自己负责的文件
outlines/XX_*.md         # 各部分的详细提纲，撰稿人必读自己的那份
```

| 部分 | 章节 | 负责人 |
| --- | --- | --- |
| 第 I 部分 基础篇 | ch01 全景导论 / ch02 数学基础 / ch03 传感器 | Lead |
| 第 II 部分 里程计篇 | ch04–ch10 | writer-odom |
| 第 III 部分 SLAM 篇 | ch11–ch15（框架/前端/后端/建图/Cartographer） | writer-slam |
| 第 III 部分 SLAM 篇 | ch16–ch17（LIO 进化史 / FAST-LIO2 与 Point-LIO） | writer-lio |
| 第 IV 部分 导航篇 | ch18–ch22（Nav2 / 全局规划 / 局部规划 / CMU 3D / 实战） | writer-nav |
| 第 IV 部分 导航篇 | ch23 Z-Localization（Lead 写）、ch24 前沿 | Lead |
| 第 V 部分 工程篇 | ch25–ch30 | writer-practice |
| 附录 | A 公式速查 / B 术语表 / C 参考文献 | Lead |

**篇幅**：每章 4–7 页（约 130–220 行 LaTeX）。公式多的章节可到 8 页。宁精勿水，不写凑字数的空话。

---

## 2. 每一章的标准骨架

```latex
\chapter{章标题}\label{ch:xx-name}

\chapterintro{用 150–250 字说明：本章要解决什么问题、为什么重要、学完能做什么、和前后章节的关系。}

\section{第一节标题}\label{sec:xx-name}
...
\subsection{...}

... 正文 ...

\section*{本章小结}
% 5–8 条要点，覆盖本章的核心结论与公式

\section*{思考与练习}
\begin{enumerate}
  \item ...
  \item ...
\end{enumerate}

\section*{延伸阅读}
% 2–4 条，指向具体论文/代码仓库/文档，写清楚"读它解决什么问题"
```
`\chapterintro`、`\section*` 均已可用。章内小节编号用 `\section`，不要手写编号。

---

## 3. 数学写作硬性规范

### 3.1 首次出现的名词必须定义

全书每个数学名词只在**第一次**出现处完整定义，之后可以引用。首次引入责任分配如下（写到该章的人必须完成定义，后面章节的人只能引用）：

- **ch02**：随机变量、概率、条件概率、贝叶斯公式、期望、方差、标准差、协方差、协方差矩阵、高斯（正态）分布、独立、泰勒展开、雅可比矩阵、海森矩阵、最小二乘、正规方程、特征值/特征向量、二次型、卡方分布、李群/李代数（SO(3)、SE(3)）、流形上的加法与乘法更新。
- **ch03**：测量模型、观测噪声、传感器外参、时间戳与时间同步、IMU 噪声与零偏、点云、视场角。
- **ch04**：里程计、绝对定位、相对定位、位姿递推、累积误差（漂移）。
- **ch06**：姿态解算、互补滤波、ESKF 误差状态、IMU 预积分、重力对齐、零速修正。
- **ch07**：扫描匹配、ICP、NDT、点到面残差、KD 树、最近邻。
- **ch08**：特征点、描述子匹配、对极几何、光束法平差（BA）、VIO。
- **ch09**：信息矩阵、马氏距离、紧耦合/松耦合。
- **ch10**：粒子滤波、重要性采样、重采样、AMCL。
- **ch11**：SLAM 问题形式化、前端、后端、数据关联。
- **ch12**：关键帧、局部地图、回环检测（概念级）。
- **ch13**：因子图、位姿图、舒尔补、鲁棒核函数、边缘化。
- **ch14**：占据栅格、八叉树、TSDF、ESDF、地图评价指标。
- **ch15**：submap、分支定界、Ceres 求解。
- **ch16**：LIO、紧耦合、去畸变。
- **ch17**：增量式 KD 树（iKD-Tree）、迭代扩展卡尔曼滤波（IEKF）、逐点更新、Manifold 更新、体素地图。
- **ch18**：代价地图、行为树、TF 树、Nav2 架构。
- **ch19**：图搜索、启发函数、A*、Hybrid A*、RRT*、可视图。
- **ch20**：DWA、TEB、MPC、ESDF 梯度。
- **ch21**：地形可通行性分析、探索、TARE、FAR Planner。
- **ch23**：后端的 NIS 检验、卡方检验（引用 ch02 定义）、SE₂(3) 误差建模。

### 3.2 推导规范

1. 每个公式前用一句话说明"要推导什么"，后用一个自然段说明"结果说明什么"。
2. 多行推导用 `align`，每行末尾用 `&` 对齐等号，**每行只做一个变换**。
3. 近似要显式写出，例如：`当 $\Delta t \to 0$ 时，保留一阶项，忽略 $O(\Delta t^2)$`。
4. 矩阵求导要写出维度：`$\bm{J}\in\mathbb{R}^{3\times 3}$`。
5. 符号必须与第 4 节全局符号表一致；新增符号必须在首次出现处用一句话说明。
6. 不要出现"容易证明""显然""众所周知"。
7. 每个公式都要 `\label{eq:...}` 吗？只有被后文引用的公式才必须 label，其余可省。

### 3.3 数学环境

- 行内：`$...$`；行间：`equation`、`align`、`gather`。
- 向量/矩阵用 `\bm{}`（已加载 bm）：`\bm{R}`、`\bm{p}`、`\bm{\omega}`。
- 集合：`\mathbb{R}`；函数名：`\mathrm{tr}`、`\mathrm{diag}`、`\mathrm{Cov}`。
- 范数：`\norm{\cdot}`，绝对值 `\abs{\cdot}`，微分 `\diff`。宏定义见 `macros.tex`。
- 转置一律 `^{\top}`，不要用 `^T`。
- 中文标点不出现在行间公式内。

---

## 4. 全局符号表（必须遵守）

| 符号 | 含义 |
| --- | --- |
| $W$ | 世界系 / 地图系（world / map） |
| $O$ | 里程计系（odom），局部连续、无跳变 |
| $B$ | 机体系（body，默认与 IMU 系重合） |
| $L$、$C$ | 雷达系、相机系 |
| $T_{AB}=(R_{AB},{}^{A}\bm{p}_{B})$ | 从 B 系到 A 系的位姿；$T_{WB}$ 表示机体在世界系中的位姿 |
| $\bm{R}\in SO(3)$ | 旋转矩阵，$\bm{R}_{AB}$ 把 B 系向量变到 A 系 |
| $\bm{q}$ | 单位四元数，$\bm{q}_{AB}$ 与 $\bm{R}_{AB}$ 等价 |
| $\bm{p}$、$\bm{v}$、$\bm{a}$ | 位置、速度、加速度 |
| $\bm{\omega}$、$\bm{g}$ | 角速度、重力向量（默认 $\bm{g}=[0,0,-9.81]^{\top}$，$z$ 轴向上） |
| $\tilde{\bm{\omega}}$、$\tilde{\bm{a}}$ | IMU 的**测量值**（带噪声和零偏） |
| $\bm{b}_g$、$\bm{b}_a$ | 陀螺仪零偏、加速度计零偏 |
| $\bm{n}_g$、$\bm{n}_a$、$\bm{n}_{bg}$、$\bm{n}_{ba}$ | 对应噪声项，均设为零均值高斯白噪声 |
| $\bm{x}$、$\delta\bm{x}$ | 状态、误差状态 |
| $\bm{z}$、$\bm{h}(\cdot)$、$\bm{r}$ | 测量、观测函数、残差 |
| $\bm{P}$、$\bm{Q}$、$\bm{R}$ | 状态协方差、过程噪声协方差、测量噪声协方差 |
| $\bm{J}$、$\bm{H}$ | 雅可比矩阵、海森矩阵 |
| $\Delta t$、$t_k$ | 时间间隔、第 $k$ 个时刻 |
| $\bm{p}_i$、$\bm{n}_\pi$、$\pi=(\bm{n}_\pi,d)$ | 第 $i$ 个点、平面法向、平面参数（$\bm{n}_\pi^{\top}\bm{x}=d$） |
| $\Lambda$ | 信息矩阵（$=\bm{P}^{-1}$ 或 $=\bm{J}^{\top}\bm{R}^{-1}\bm{J}$） |
| $\hat{(\cdot)}$ | 估计值；$\tilde{(\cdot)}$ 只用于 IMU 原始测量 |

坐标系约定：世界系 $z$ 轴向上（ENU 式），重力 $\bm{g}=[0,0,-9.81]^{\top}$；旋转矩阵作用方式为 ${}^{A}\bm{p}={}^{A}\bm{R}_{B}{}^{B}\bm{p}+{}^{A}\bm{p}_{B}$。全书统一，禁止混用。

---

## 5. LaTeX 约定

### 5.1 文件与标签

- 每个文件第一行就是 `\chapter{...}\label{ch:xx-name}`，章 label 已由 Lead 写在骨架里，**不要改动**。
- 标签前缀：节 `sec:xx-...`，公式 `eq:xx-...`，图 `fig:xx-...`，表 `tab:xx-...`，定义/定理 `def:xx-...`、`thm:xx-...`，代码 `lst:xx-...`。`xx` 是本文章号，保证全局唯一。
- 只引用**自己章**的标签，或引用**章级**标签（如 `见第~\ref{ch:06-imu}~章`）。跨章节引用小节/公式时必须确认标签存在，不确定就只引到章。
- 引用格式：`第~\ref{ch:06-imu}~章`、`式~\eqref{eq:06-prop}`、`图~\ref{fig:06-...}`、`表~\ref{tab:...}`。注意波浪号 `~` 防止换行断号。

### 5.2 图：只用 TikZ，禁止外部图片

- 所有示意图、流程图、曲线图都在 `.tex` 内用 TikZ / pgfplots 画，不引用任何图片文件（保证可移植编译）。
- 所需库已在 `main.tex` 中加载：`arrows.meta, shapes.geometric, shapes.misc, positioning, fit, calc, backgrounds, patterns, decorations.pathreplacing, pgfplots`。
- 风格统一：方框用 `rectangle, rounded corners=2pt, draw=structurecolor, thick, fill=structurecolor!8`；箭头用 `-{Stealth[length=2mm]}`；字体 `\small`；颜色只用 `structurecolor`、`black!60`、`red!60!black`、`green!45!black`、`orange!80!black`。
- 图宽默认 `width=0.9\linewidth`，图注 `\caption{...}\label{fig:xx-...}` 放在 `\begin{figure}[htbp]` 内。
- 每章 1–3 张图即可，公式与表格优先。**画图前先在纸上想清楚节点和连线，再写代码，避免复杂嵌套导致编译失败。**
- pgfplots 画曲线示例见 `outlines/` 中给出的模板。

### 5.3 表：booktabs

```latex
\begin{table}[htbp]
  \centering
  \caption{方法对比}\label{tab:xx-compare}
  \small
  \begin{tabular}{lccc}
    \toprule
    方法 & 精度 & 速度 & 内存 \\
    \midrule
    ...
    \bottomrule
  \end{tabular}
\end{table}
```
宽表用 `\small` 或 `\footnotesize`，禁止用 `\resizebox` 硬缩。

### 5.4 代码

- 用 `lstlisting`，短小（≤ 25 行），只放关键片段，不放整文件。
- 语言标注：`language=C++`、`language=Python`、`language=bash`。
- **listing 内部的注释和字符串一律用英文**（避免 XeLaTeX 下中文断行问题）；代码前后的正文用中文解释。
- 不要用 tab 缩进，用 4 个空格。行宽不超过 78 字符。
- 伪代码用 `pseudo` 环境（见 `macros.tex`），格式：
```latex
\begin{pseudo}{点到面 ICP 的单次迭代}
  \item 对每个点 $\bm{p}_i$，在目标点云中找最近点 $\bm{q}_i$
  \item ...
\end{pseudo}
```

### 5.5 提示框与定理环境

- 章节导语：`\chapterintro{...}`。
- 要点框：`\begin{keybox}{标题}...\end{keybox}`（自定义，见 macros）。
- 常见坑：`\begin{note}...\end{note}`、`\begin{remark}...\end{remark}`（elegantbook 自带）。
- 定义/定理：`\begin{definition}[名称]...\end{definition}`、`\begin{theorem}...\end{theorem}`、`\begin{lemma}`、`\begin{example}` 均可直接用。
- 注意：`definition`、`theorem` 等环境已经自带编号，**不要在里面再手写"定义 1"**。

### 5.6 其他

- 列表：`itemize` / `enumerate`，嵌套最多两层。
- 强调用 `\textbf{}`；中文不用斜体。
- 超链接 `\href{https://...}{显示文字}`，URL 里的下划线不用转义。
- 行内代码 `\lstinline{...}` 或 `\texttt{}`。
- 不要用 `\part`（由 main.tex 统一组织）。
- 不要写 `\bibliography`、`\printbibliography`（由 main.tex 统一处理）。
- 不要用 `\maketitle`、`\tableofcontents`。

---

## 6. 参考文献

- 只允许引用 `reference.bib` 里**已存在**的 key，**禁止自己编造 key**（编造会导致整本书编译失败）。
- 引用写法：`\cite{zhang2014loam}`；一句里多个：`\cite{zhang2014loam,shan2018lego}`。
- 可用 key 清单与对应文献见 `reference.bib` 文件开头注释；也可在 `outlines/` 各文件末尾看到本部分推荐引用。
- 如果确实需要一篇清单外的文献，在正文中给出完整的 `\href{}{}` 链接和作者年份文字描述，不要 `\cite`。

---

## 7. 禁止事项（会导致返工）

1. 修改 `main.tex`、`macros.tex`、`reference.bib`、`STYLE.md`、其他人的章节文件。
2. 使用未加载的宏包（`\usepackage` 一律禁止；需要新宏时先用已有宏实现，或告知 Lead）。
3. 引用不存在的 label / bib key；写错环境名（如 `\begin{defination}`）。
4. 大段英文原文照抄；可以翻译并标注出处。
5. 出现"如下图所示"却根本没有图；出现"见表"却没有表。
6. 把代码、公式、列表塞进 tcolorbox 的 title 里。
7. 输出未闭合的 `\begin{}`/`\end{}`、未配对的 `$`、未转义的 `%`、`&`、`_`、`#`。
8. 使用中文全角括号/逗号写 LaTeX 命令或数学公式。

---

## 8. 交稿前自检清单

- [ ] 本章 `\chapter` 标题与骨架一致，label 未被改动。
- [ ] 每个新数学名词首次出现处都有定义 + 计算式 + 数字例子（至少关键的要有）。
- [ ] 所有推导步骤完整，没有"显然""易证"。
- [ ] 所有 `\ref`/`\cite` 的 label/key 都存在。
- [ ] TikZ 图能独立编译（可先在小文件里试）。
- [ ] 无未转义的 `% & _ #`，无中文标点进入公式。
- [ ] 每个 `lstlisting` 都标注了 language，且内部无中文。
- [ ] 有 `本章小结`、`思考与练习`、`延伸阅读`。
- [ ] 通读一遍，确认前后逻辑连贯、没有与相邻章节重复大段内容。

---

## 9. 编译自检命令（撰稿人用）

每个章节都有独立测试文件，可以单独编译检查语法：

```powershell
# 在项目根目录执行；只会编译你这一章，不碰 main.tex
xelatex -interaction=nonstopmode -halt-on-error -output-directory=build/ch04 tests/test-ch04.tex
```

- 测试文件 `tests/test-ch04.tex` 已生成，内容为加载类和宏 + `\input{chapters/ch04_...}`。
- 如果报错，先看 `build/ch04/test-ch04.log` 里第一个 `!` 开头的错误。
- **不要**编译 `main.tex`（Lead 负责），否则会互相覆盖 aux 文件。
- 测试编译成功不要求生成完整目录/交叉引用，能过语法即可。
