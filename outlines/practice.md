# 第 V 部分「工程篇」详细提纲（writer-practice 专用）

你负责 `chapters/ch25_ros2.tex` ~ `chapters/ch30_roadmap.tex` 共 6 章。前面各章由他人完成，你**假设**已定义：位姿、里程计、SLAM、前端/后端、LIO、Cartographer、Nav2、ESDF 等。用到时引用章 label（`\ref{ch:07-lidar-odom}` 等）。

**动笔前必须读**：`STYLE.md`、`main.tex`、`macros.tex`。只改这 6 个文件。

**本部分定位**：让读者能把前面的算法真正跑起来、标定好、调稳、评出来。工程细节要具体（命令、参数、表格、排错表），不要空泛。

---

## 第 25 章 ROS 2 工程实践（ch25_ros2，约 5 页）

1. **ROS 2 是什么**：DDS 通信、去中心化、节点/话题/服务/动作、QoS；与 ROS 1 的差异表。引用 `macenski2022ros2`。
2. **最小工作空间**：`colcon` 编译流程、`package.xml`/`CMakeLists.txt` 关键字段、`install/` 目录、`source` 顺序、`--symlink-install`。给一段 15 行命令。
3. **通信机制**：话题（发布/订阅）、服务（请求/响应）、动作（长任务 + 反馈 + 取消）；什么时候用哪个；给一张决策表。
4. **QoS**：可靠性（reliable/best_effort）、历史深度、durability；为什么传感器数据用 `best_effort`、地图用 `transient_local`；QoS 不匹配的典型报错。
5. **参数与 launch**：`declare_parameter`、YAML 覆盖、`launch.py`（Node/IncludeLaunchDescription/SetParameter）；给一个 20 行的 launch 示例。
6. **TF2**：`map→odom→base_link→sensor` 的发布与查询；`static_transform_publisher`；`tf2_ros::Buffer::lookupTransform` 的异常与时间戳；`ros2 run tf2_tools view_frames`。
7. **常用工具**：`ros2 topic hz/echo/info`、`ros2 node list`、`rqt_graph`、`rviz2`、`ros2 bag record/play`、`ros2 doctor`、`ros2 param`。
8. **工程习惯**：命名空间、多机器人、`use_sim_time`、日志级别、实时性（`rclcpp::executors`、回调组、CPU 亲和性）；给一个"定位节点延迟排查"的小案例。
9. **小结/练习/延伸阅读**。

图：ROS 2 通信模型图；TF 树图（选 1 张即可）。

---

## 第 26 章 标定与时间同步（ch26_calibration，约 7 页）

本章推导要细，因为标定误差是新手最常见的"玄学问题"来源。

1. **为什么标定**：外参错 1° 在 10 m 处产生 17 cm 误差（给公式 $d\sin\theta$ 与例子）；时间错 10 ms 在 2 m/s 时产生 2 cm 误差。
2. **相机内参**：针孔模型、内参矩阵 $K$、径向/切向畸变模型；**张正友标定法的推导**（单应矩阵、利用旋转向量正交性构造约束、求内参、求外参、最大似然细化），给出完整公式链。给一个标定结果示例（fx, fy, cx, cy, k1, k2, p1, p2）。
3. **IMU 标定**：零偏、尺度因子、轴间非正交；**Allan 方差**定义与用途：用不同平均时间 $\tau$ 的方差曲线读出角度随机游走、速度随机游走、零偏不稳定性；给出 Allan 方差的计算公式与典型曲线示意。
4. **LiDAR-IMU 外参**：旋转 + 平移 + **时间偏移**三个量；基于运动的方法（手眼标定 $AX=XB$ 的推导与求解）；连续时间轨迹方法；给一个标定流程（录 bag → 优化 → 验证）。
5. **相机-IMU 外参**：Kalibr 的连续时间批量估计思想；时间偏移估计；给命令示例。
6. **LiDAR-相机外参**：基于标定板/角点的方法、基于互信息的方法；验证方法（投影叠加图）。
7. **时间同步**：GPS/PPS、PTP（IEEE 1588）、`chrony`、硬件触发；ROS 2 `use_sim_time`、`rosbag --clock`；软件时间戳 vs 硬件时间戳；延迟补偿公式。
8. **标定验证与常见错误**：重投影误差、点云-图像对齐检查、IMU 重力模长检查（应为 9.81）、外参符号错误、坐标系方向错误。
9. **小结/练习/延伸阅读**。

图：针孔模型/畸变示意；手眼标定 $AX=XB$ 示意；Allan 方差曲线示意（选 2 张）。

---

## 第 27 章 调参与排错手册（ch27_tuning，约 6 页）

以"症状 → 原因 → 处理"为主线，做成大量表格，方便查。

1. **调参方法论**：一次只改一个参数、固定数据集、记录指标、先调数据质量再调算法；给一个"调参记录表"模板。
2. **FAST-LIO / FAST-LIO2 参数**：`lid_topic`、`imu_topic`、`extrinsic_T/R`、`filter_size_surf`、`filter_size_map`、`cube_side_length`、`point_filter_num`、`max_iteration`、`acc_cov`/`gyr_cov`/`b_acc_cov`/`b_gyr_cov`；每个参数"调大/调小"的后果表。给一段 20 行 YAML。
3. **Point-LIO 参数**：与 FAST-LIO 的差异参数（逐点更新相关）、IMU 饱和处理、`lidar_type` 等。
4. **Cartographer 参数**：`num_range_data`、`submaps.resolution`、`submaps.num_range_data`、`constraint_builder.min_score`、`optimization_problem.huber_scale`、`TRAJECTORY_BUILDER_2D` 各参数；给"建图糊了/重影/回环失败"的参数线索。
5. **Nav2 参数**：`robot_radius`/`footprint`、`inflation_radius`、`cost_scaling_factor`、`max_vel_x`、`acc_lim`、`xy_goal_tolerance`、规划器/控制器插件选择；给一段 30 行 YAML。
6. **排错速查表**（重点）：至少 12 行，覆盖：定位起飞、点云拖影、地图重影、回环错误、TF 报错、时间戳乱序、CPU 打满、内存增长、IMU 数据异常、外参错、UWB 跳变、导航原地转。每行：现象 / 可能原因 / 排查命令 / 处理。
7. **日志与可视化**：RViz2 看什么（点云、轨迹、协方差、TF）、`ros2 bag` 回放定位问题、`evo` 看轨迹、`rqt_plot`。
8. **小结/练习/延伸阅读**。

图：调参决策流程图（1 张）。

---

## 第 28 章 数据集、评测与复现（ch28_evaluation，约 5 页）

1. **公开数据集**：KITTI、EuRoC、TUM VI、NTU VIRAL、Newer College、M2DGR、RM 自采数据；每个给：传感器、场景、适合评测什么、下载方式。做一张对比表。
2. **评价指标**：
   - **ATE**：定义、对齐方式（SE(3) Umeyama 对齐，给出闭式解推导）、RMSE 公式
     $$\mathrm{ATE}_{\mathrm{RMSE}}=\sqrt{\frac1N\sum_i\norm{\mathrm{trans}(\hat T_i^{-1}T_i)}^2}$$
   - **RPE**：固定时间间隔/距离间隔的相对位姿误差；为什么里程计看 RPE。
   - 漂移率、地图精度、实时性（CPU/内存/延迟）。
3. **evo 工具**：`evo_traj`、`evo_ape`、`evo_rpe` 的命令与输出解读；给 4 条命令。
4. **自采数据规范**：时间同步、标定文件、真值获取（动捕/全站仪/RTK）、bag 命名与元数据。
5. **可复现实验**：固定随机种子、记录配置、多次运行取中位数、消融实验设计（给一个消融表模板）。
6. **小结/练习/延伸阅读**。

图：ATE/RPE 示意（轨迹与误差）；评测流程图（选 1 张）。

---

## 第 29 章 RoboMaster 场景实践建议（ch29_rm，约 4 页）

用户要求"少量提及即可"，所以写成"实战清单"，不要展开成完整比赛教程。

1. **赛场环境特点**：场地尺寸、对称结构、动态障碍（机器人、弹丸）、光照变化、多楼层/坡道（如果有）、观众干扰。
2. **定位方案选型**：LIO（FAST-LIO2/Point-LIO）为主、UWB 辅助、先验地图定位（Z-Localization 思路）、雷达站全局视角；给一张"方案-优点-风险"表。
3. **哨兵/步兵/雷达站的不同需求**：算力、体积、功耗、动态性；给一张对比表。
4. **坐标系与标定清单**：`map→odom→base→gimbal→camera/lidar`；云台与底盘解耦；标定顺序；上车检查表（10 条）。
5. **备赛流程建议**：建图 → 地图清理 → 先验地图包 → 定位验证 → 导航联调 → 压力测试；每步给验收标准。
6. **常见坑**：动态残影、地图过期、UWB 多径、场地对称导致重定位错误、算力不足。
7. **小结/延伸阅读**（练习可省）。

图：RM 机器人坐标系与模块关系图（1 张）。

---

## 第 30 章 学习路线与资源清单（ch30_roadmap，约 4 页）

1. **分阶段路线**（0–1 月、1–3 月、3–6 月、6–12 月）：每阶段目标、要读的章节、要跑的代码、要做的项目、验收标准。
2. **代码阅读顺序**：KISS-ICP（最简单）→ FAST-LIO2 → Point-LIO → Cartographer → Nav2 → Z-Localization；每个给"先看哪个文件、看什么"。
3. **书与课程**：Probabilistic Robotics、State Estimation for Robotics、视觉 SLAM 十四讲、深蓝学院课程等（给中文/英文资源与链接）。
4. **工具链清单**：Ubuntu/ROS 2、C++/CMake、Eigen、PCL、Ceres、GTSAM、OpenCV、RViz2、evo、CloudCompare、Foxglove。
5. **给新队员的 10 条建议**：先跑通再改、先看数据再看代码、记录实验、学会看 TF、重视标定、从失败案例学、多读 issue、写文档……
6. **结语**：与全书呼应。

---

## 通用要求

1. 每章 `\chapterintro{...}`；结尾 `本章小结`、`思考与练习`（第 29、30 章可只保留小结与延伸阅读）、`延伸阅读`。
2. 只引用 `reference.bib` 已有 key。推荐：`macenski2022ros2,macenski2020nav2,xu2022fastlio2,he2023pointlio,hess2016cartographer,sola2017eskf,thrun2005probabilistic,barfoot2017state,zloc2026,cao2022tare`。
3. 代码/配置/命令用 `lstlisting`，内部注释英文；表格用好 `booktabs`，排错表可以宽一些（用 `\footnotesize`）。
4. 自检：`xelatex -interaction=nonstopmode -halt-on-error -output-directory=build/ch25 tests/test-ch25.tex`，其余章同理。
5. 完成后 `send_message` 向 lead 汇报。
