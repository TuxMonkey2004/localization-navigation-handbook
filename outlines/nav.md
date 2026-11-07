# 第 IV 部分「导航篇」详细提纲（writer-nav 专用）

你负责 `chapters/ch18_nav_overview.tex` ~ `chapters/ch22_nav2_practice.tex` 共 5 章。第 23 章（Z-Localization）与第 24 章由 Lead 写，你不要碰。

**动笔前必须读**：`STYLE.md`、`main.tex`、`macros.tex`。假设第 2、11–15 章已定义：概率、最小二乘、因子图、占据栅格、ESDF、SLAM 前后端。用到时引用章 label。

**本部分重点**：用户点名"2D 的 Cartographer、3D 的 CMU 导航算法"，并关心"导航前端/后端"的说法。第 18 章要先把"导航系统里的前端/后端"和"SLAM 的前端/后端"区分清楚，避免混淆。

---

## 第 18 章 导航系统总览与 Nav2（ch18_nav_overview，约 6 页）

1. **导航 = 定位 + 建图 + 规划 + 控制**：给一张大图（感知→定位/建图→规划→控制→执行器），标出每部分对应的本书章节。
2. **导航的"前端/后端"**：明确区分三种语境（SLAM 前端/后端、定位系统前端/后端、导航系统前端/后端）；给出"导航后端 = 规划与控制，导航前端 = 定位与地图"的说法为什么会流行、以及它的不严谨之处。**这一节要写清楚，直接回应用户的疑问。**
3. **Nav2 架构**（ROS 2 事实标准）：
   - `bt_navigator`（行为树）、`planner_server`、`controller_server`、`smoother_server`、`behavior_server`、`waypoint_follower`、`velocity_smoother`、`lifecycle_manager`。
   - 给一张 Nav2 节点数据流图；说明 action 接口（`NavigateToPose`）。
   - Nav2 与 ROS 1 `move_base` 的差异（行为树、生命周期、插件化、多机器人）。
   - 引用 `macenski2020nav2`、`macenski2022ros2`。
4. **代价地图（Costmap 2D）**：分层结构（static / obstacle / inflation / voxel）、每层作用、`update_frequency` 与 `publish_frequency`、膨胀半径的几何意义（内切/外切半径）。给一个"机器人过窄门"的例子说明膨胀参数怎么调。
5. **TF 树与坐标系**：`map → odom → base_link → laser/imu` 的语义；谁发布谁；`map→odom` 由定位模块发布；常见 TF 错误（重复发布、断链、时间戳）。
6. **全局规划 vs 局部规划**：定义、输入输出、频率（1 Hz vs 10–20 Hz）、评价指标（路径长度、平滑度、安全性、可行性）。
7. **小结/练习/延伸阅读**。

图：导航大图；Nav2 节点数据流图；TF 树图。

---

## 第 19 章 全局路径规划（ch19_global_planning，约 6 页）

1. **问题定义**：栅格图上的最短路；代价函数 $g(n)$、启发函数 $h(n)$；完备性与最优性定义。
2. **Dijkstra**：算法伪代码、正确性证明要点、复杂度 $O((V+E)\log V)$。
3. **A\***：$f=g+h$；**可采纳性证明**（$h\le h^*$ 推出最优）；一致性（单调性）与"不重复扩展"的证明思路；启发函数设计（曼哈顿/欧氏/对角距离），给一个 10×10 网格的手算例子。引用 `hart1968astar`。
4. **JPS**：跳点思想、强制邻居、为什么能减少扩展节点；给出伪代码。引用 `harabor2011jps`。
5. **Hybrid A\***：连续状态 + 栅格索引、运动基元（Reeds-Shepp/自行车模型）、启发函数（非完整约束下的 distance heuristic）、为什么适合车/差速底盘。引用 `dolgov2010hybridastar`。
6. **采样规划**：RRT、RRT*（重连与渐近最优）、Informed RRT*；适用场景（高维、无栅格）。引用 `karaman2011rrtstar`。
7. **其他**：可视图（visibility graph）、Voronoi 图、势场法（简述，第 20 章展开局部）。
8. **工程实践**：Nav2 `planner_server` 的插件（`NavfnPlanner`、`SmacPlanner`、`SmacPlannerHybrid`）、代价地图代价值如何映射、路径平滑（`smoother_server`）。
9. **小结/练习/延伸阅读**。

图：A* 扩展过程（小网格示意）；Hybrid A* 运动基元；RRT* 重连示意（选 2 张）。

---

## 第 20 章 局部规划与控制（ch20_local_planning，约 6 页）

1. **局部规划要解决什么**：跟踪全局路径、避障、满足运动学/动力学约束、实时（10–20 Hz）。
2. **DWA（动态窗口法）**：速度空间 $(v,\omega)$ 采样、动态窗口约束（加速度限制）、评价函数
   $$G(v,\omega)=\alpha\cdot \mathrm{heading}+\beta\cdot \mathrm{clearance}+\gamma\cdot \mathrm{velocity}$$
   逐项定义并给出完整公式；为什么能实时；局限（局部最优、窄通道）。引用 `fox1997dwa`。
3. **TEB（时间弹性带）**：把轨迹表示成带时间戳的位姿序列，构造图优化问题（位姿节点 + 时间间隔节点），目标函数（路径跟随 + 障碍距离 + 速度/加速度约束 + 运动学约束），用 g2o 求解；给目标函数公式。引用 `rosmann2012teb`。
4. **MPC**：滚动时域、预测模型、约束、二次规划形式；与 DWA 的关系；计算量。引用 `rawlings2017mpc`。
5. **梯度类局部规划（EGO-Planner / Fast-Planner 思想）**：ESDF 梯度、碰撞代价、平滑代价、B 样条轨迹优化；给碰撞代价公式（梯形/二次惩罚）。引用 `zhou2021egoplanner`、`zhou2019fastplanner`。
6. **人工势场**：引力/斥力公式、局部极小值问题、改进思路。
7. **底盘约束**：差速、麦轮、阿克曼的运动学约束如何进入局部规划（给出约束方程）。
8. **Nav2 controller 插件**：`DWB`、`TEB`、`MPPI`、`RegulatedPurePursuit` 的适用场景对比表。
9. **小结/练习/延伸阅读**。

图：DWA 速度空间采样示意；TEB 图结构；MPC 滚动时域示意（选 2 张）。

---

## 第 21 章 3D 导航与 CMU 自主探索栈（ch21_3d_nav，约 7 页）

用户点名"3D 的 CMU 导航算法"，本节要讲清楚 CMU（Ji Zhang 组）开源的 Autonomous Exploration Development Environment（`caochao39/autonomous_exploration_development_environment`，论文 ICRA 2022）。

1. **为什么 2D 导航不够**：坡道、台阶、多层、室外地形；3D 点云地图 + 地形分析。
2. **CMU 栈的总体架构**：`terrain_analysis` / `terrain_analysis_ext`（地形可通行性）、`local_planner`（局部规划）、`far_planner`（全局规划/可视图）、`tare_planner`（自主探索）、`path_follower`（路径跟踪）、`visualization_tools`。给一张模块数据流图，标注每个模块的输入/输出话题与频率。引用 `cao2022tare`、`yang2022farplanner`。
3. **地形分析（Terrain Analysis）**：
   - 把点云投影成 2.5D 栅格（每格记录高度/密度）；**推导坡度、粗糙度、台阶高度的计算方法**：
     $$\text{slope}=\arctan\left(\frac{\Delta z}{\sqrt{\Delta x^2+\Delta y^2}}\right)$$
     以及用邻域点拟合平面求法向、用高度差的标准差求粗糙度。
   - 可通行性判定（坡度阈值、台阶阈值、障碍高度）；给出伪代码与参数（如 `maxRelZ=0.3`、`slopeThreshold=0.6` 等量级）。
   - 2.5D 与真 3D 的折中。
4. **局部规划（Local Planner）**：在 2.5D 地形图上做"避障 + 跟随全局路径"；考虑机器人尺寸/离地间隙；与 2D DWA 的区别；给核心步骤。
5. **FAR Planner（Fast, Attemptable Route Planner）**：
   - 可视图（visibility graph）增量构建：节点=可通行区域采样点，边=无碰撞连线；**给出可见性检查与增量更新思路**。
   - "Attemptable"：允许规划穿过未知区域，走不通就重规划；与 A* 的区别。
   - 为什么适合大范围未知环境；计算量。
   - 引用 `yang2022farplanner`。
6. **TARE（自主探索）**：层次化探索（局部/全局）、探索增益、路径规划；"探索"与"导航"的区别；给伪代码框架。引用 `cao2022tare`。
7. **部署与调参**：ROS 1/ROS 2 版本、`vehicle_height`/`sensor_height` 等参数、常见问题（地形分析抖动、局部规划卡住）。
8. **与 LIO 的配合**：为什么 CMU 栈通常配 FAST-LIO2/LIO-SAM；点云地图如何喂给地形分析。
9. **小结/练习/延伸阅读**。

图：CMU 栈模块图；2.5D 地形分析示意；可视图/FAR 规划示意；探索流程（选 3 张）。

---

## 第 22 章 2D 建图 + 导航完整链路实战（ch22_nav2_practice，约 5 页）

1. **全链路**：建图（Cartographer）→ 保存地图（`map_server` 的 pgm/yaml）→ 定位（AMCL）→ 规划（Nav2）→ 控制（DWB）→ TF。
2. **Cartographer 建图实操**：`cartographer_ros` 配置（`backpack_2d.lua`）、launch、`finish_trajectory`、`write_state` 导出 pbstream、`cartographer_pbstream_to_ros_map` 转 pgm。
3. **Nav2 配置**：`nav2_params.yaml` 关键段（`amcl`、`planner_server`、`controller_server`、`costmap`）、`map_server` 加载地图、`lifecycle_manager` 启动顺序。给一份可用的最小参数框架（30–50 行 YAML）。
4. **仿真验证**：Gazebo/TurtleBot3 例程、`ros2 launch nav2_bringup`。
5. **常见问题排查表**：地图漂移、定位跳变、规划失败、机器人原地转、TF 断链、代价地图不更新，每行给现象→原因→解决。
6. **性能与安全**：控制频率、CPU 占用、急停与恢复行为（`behavior_server`）。
7. **小结/练习/延伸阅读**。

图：全链路数据流图；TF 时序图（选 1–2 张）。

---

## 通用要求

1. 每章 `\chapterintro{...}`；结尾 `本章小结`、`思考与练习`、`延伸阅读`。
2. 只引用 `reference.bib` 已有的 key。推荐：`macenski2020nav2,macenski2022ros2,fox1997dwa,rosmann2012teb,rawlings2017mpc,zhou2021egoplanner,zhou2019fastplanner,dolgov2010hybridastar,hart1968astar,harabor2011jps,karaman2011rrtstar,yang2022farplanner,cao2022tare,hess2016cartographer,thrun2005probabilistic,oleynikova2017voxblox,xu2022fastlio2`。
3. 配置/代码片段用 `lstlisting[language=...]`，内部注释用英文。
4. 自检：`xelatex -interaction=nonstopmode -halt-on-error -output-directory=build/ch18 tests/test-ch18.tex`，其余章同理。
5. 完成后 `send_message` 向 lead 汇报：页数、自检结果、需要复核的点。
