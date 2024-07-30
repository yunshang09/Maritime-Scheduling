import random
from datetime import datetime, timedelta
import json

# 基本参数定义
NUM_SHIPS = 2
NUM_CREWS_PER_SHIP = 3
AVG_DRAFT = 2.5
AVG_SPEED = 15.0
START_DATE = "2024-07-29"
START_TIME = "04:00"
END_TIME = "23:00"

UNITS = [
    {"id": "2D7", "latitude": 30.0, "longitude": 122.0, "depth": 10.0, "field": "WindFarm1"},
    {"id": "3A9", "latitude": 30.5, "longitude": 121.5, "depth": 8.0, "field": "WindFarm2"},
    {"id": "4B3", "latitude": 31.0, "longitude": 120.5, "depth": 9.0, "field": "WindFarm3"},
    {"id": "5C6", "latitude": 30.2, "longitude": 123.0, "depth": 11.0, "field": "WindFarm4"},
    {"id": "6D8", "latitude": 30.8, "longitude": 122.5, "depth": 12.0, "field": "WindFarm5"},
    {"id": "7E9", "latitude": 30.3, "longitude": 121.8, "depth": 10.5, "field": "WindFarm6"},
    {"id": "8F0", "latitude": 31.2, "longitude": 122.2, "depth": 9.5, "field": "WindFarm7"},
    {"id": "9G1", "latitude": 30.7, "longitude": 121.2, "depth": 8.5, "field": "WindFarm8"},
]

TASKS = [
    {"name": "#3变桨位置传感器异常故障处理", "type": "故障", "hours": 3, "position": "WindFarm1"},
    {"name": "叶片裂缝检测", "type": "缺陷", "hours": 4, "position": "WindFarm2"},
    {"name": "发电机温度异常", "type": "故障", "hours": 3, "position": "WindFarm3"},
    {"name": "主轴润滑系统检查", "type": "预警", "hours": 2, "position": "WindFarm4"},
    {"name": "控制系统校准", "type": "定期运维", "hours": 5, "position": "WindFarm5"},
    {"name": "电缆连接检查", "type": "缺陷", "hours": 1, "position": "WindFarm6"},
    {"name": "传感器校准", "type": "定期运维", "hours": 3, "position": "WindFarm7"},
    {"name": "变压器检查", "type": "预警", "hours": 2, "position": "WindFarm8"},
]

WEATHER = [
    {"time": "00:00", "depth": {"dock": 4.29, "WindFarm1": 4.29, "WindFarm2": 4.29, "WindFarm3": 4.29, "WindFarm4": 4.29, "WindFarm5": 4.29, "WindFarm6": 4.29, "WindFarm7": 4.29, "WindFarm8": 4.29}},
    {"time": "02:00", "depth": {"dock": 2.75, "WindFarm1": 2.75, "WindFarm2": 2.75, "WindFarm3": 2.75, "WindFarm4": 2.75, "WindFarm5": 2.75, "WindFarm6": 2.75, "WindFarm7": 2.75, "WindFarm8": 2.75}},
    {"time": "04:00", "depth": {"dock": 1.23, "WindFarm1": 1.23, "WindFarm2": 1.23, "WindFarm3": 1.23, "WindFarm4": 1.23, "WindFarm5": 1.23, "WindFarm6": 1.23, "WindFarm7": 1.23, "WindFarm8": 1.23}},
    {"time": "06:00", "depth": {"dock": 0.55, "WindFarm1": 0.55, "WindFarm2": 0.55, "WindFarm3": 0.55, "WindFarm4": 0.55, "WindFarm5": 0.55, "WindFarm6": 0.55, "WindFarm7": 0.55, "WindFarm8": 0.55}},
    {"time": "08:00", "depth": {"dock": 3.33, "WindFarm1": 3.33, "WindFarm2": 3.33, "WindFarm3": 3.33, "WindFarm4": 3.33, "WindFarm5": 3.33, "WindFarm6": 3.33, "WindFarm7": 3.33, "WindFarm8": 3.33}},
    {"time": "10:00", "depth": {"dock": 4.12, "WindFarm1": 4.12, "WindFarm2": 4.12, "WindFarm3": 4.12, "WindFarm4": 4.12, "WindFarm5": 4.12, "WindFarm6": 4.12, "WindFarm7": 4.12, "WindFarm8": 4.12}},
    {"time": "12:00", "depth": {"dock": 5.23, "WindFarm1": 5.23, "WindFarm2": 5.23, "WindFarm3": 5.23, "WindFarm4": 5.23, "WindFarm5": 5.23, "WindFarm6": 5.23, "WindFarm7": 5.23, "WindFarm8": 5.23}},
    {"time": "14:00", "depth": {"dock": 4.02, "WindFarm1": 4.02, "WindFarm2": 4.02, "WindFarm3": 4.02, "WindFarm4": 4.02, "WindFarm5": 4.02, "WindFarm6": 4.02, "WindFarm7": 4.02, "WindFarm8": 4.02}},
    {"time": "16:00", "depth": {"dock": 3.44, "WindFarm1": 3.44, "WindFarm2": 3.44, "WindFarm3": 3.44, "WindFarm4": 3.44, "WindFarm5": 3.44, "WindFarm6": 3.44, "WindFarm7": 3.44, "WindFarm8": 3.44}},
    {"time": "18:00", "depth": {"dock": 2.32, "WindFarm1": 2.32, "WindFarm2": 2.32, "WindFarm3": 2.32, "WindFarm4": 2.32, "WindFarm5": 2.32, "WindFarm6": 2.32, "WindFarm7": 2.32, "WindFarm8": 2.32}},
    {"time": "20:00", "depth": {"dock": 1.43, "WindFarm1": 1.43, "WindFarm2": 1.43, "WindFarm3": 1.43, "WindFarm4": 1.43, "WindFarm5": 1.43, "WindFarm6": 1.43, "WindFarm7": 1.43, "WindFarm8": 1.43}},
    {"time": "22:00", "depth": {"dock": 3.24, "WindFarm1": 3.24, "WindFarm2": 3.24, "WindFarm3": 3.24, "WindFarm4": 3.24, "WindFarm5": 3.24, "WindFarm6": 3.24, "WindFarm7": 3.24, "WindFarm8": 3.24}}
]

ROUTE_TIMES = {"dock_WindFarm1": 3,
               "dock_WindFarm2": 4,
               "dock_WindFarm3": 5,
               "dock_WindFarm4": 3,
               "dock_WindFarm5": 4,
               "dock_WindFarm6": 3,
               "dock_WindFarm7": 3,
               "dock_WindFarm8": 3}


# 转换时间字符串为 datetime 对象
def str_to_datetime(time_str):
    return datetime.strptime(time_str, '%H:%M')


# 计算时间差（分钟）
def time_diff(start, end):
    return (end - start).total_seconds() / 60


# 检查任务的时间是否在安全窗口内，并且水深是否足够
def is_within_safe_window(task):
    task_position = task["position"]
    for weather in WEATHER:
        start = str_to_datetime(weather["time"])
        route = ROUTE_TIMES.get("dock_" + task_position, 0)
        end = start + timedelta(hours=route + task["hours"])

        dock_depth = weather["depth"]["dock"]
        wind_farm_depth = weather["depth"].get(task_position, 0)

        if dock_depth >= AVG_DRAFT and wind_farm_depth >= AVG_DRAFT:
            if (start.time() >= str_to_datetime(START_TIME).time()
                    and end.time() <= str_to_datetime(END_TIME).time()):
                return True
    return False


# 目标函数：计算总成本
def objective_function(schedule):
    total_cost = 0
    current = datetime.strptime(f"{START_DATE} {START_TIME}", '%Y-%m-%d %H:%M')

    for task in schedule:
        route = ROUTE_TIMES.get("dock_" + task["position"], 0)
        end = current + timedelta(hours=route + task["hours"])

        if end.time() >= str_to_datetime(END_TIME).time():
            continue

        task_cost = 1000 if task["type"] == "故障" else 500
        time_elapsed = time_diff(str_to_datetime(START_TIME), end)
        total_cost += time_elapsed * task_cost

        current = end

    return total_cost


# 生成初始解
def generate_initial_solution():
    schedule = []
    fault_tasks = [task for task in TASKS if task["type"] == "故障"]
    other_tasks = [task for task in TASKS if task["type"] != "故障"]

    # 确保故障任务被优先安排
    for task in fault_tasks:
        schedule.append(task)

    # 对其他任务按类型进行排序
    other_tasks.sort(key=lambda x: (x["type"] == "预警", x["type"] == "定期运维"))
    for task in other_tasks:
        schedule.append(task)

    return schedule


# 破坏算子：随机移除
def destroy_solution(schedule):
    schedule = list(schedule)
    n = len(schedule)
    num_remove = random.randint(1, max(1, n // 2))
    for _ in range(num_remove):
        schedule.pop(random.randint(0, len(schedule) - 1))
    return schedule


# 修复算子：随机修复
def repair_solution(schedule):
    schedule = list(schedule)
    fault_tasks = [task for task in TASKS if task["type"] == "故障" and task not in schedule]
    other_tasks = [task for task in TASKS if task["type"] != "故障" and task not in schedule]

    for task in fault_tasks:
        schedule.append(task)
    random.shuffle(other_tasks)
    for task in other_tasks:
            schedule.append(task)
    return schedule

# 任务分配算法
def task_assignment(tasks, num_ships, crews_per_ship):
    fault_tasks = [task for task in tasks if task["type"] == "故障"]
    other_tasks = [task for task in tasks if task["type"] != "故障"]

    selected_tasks = fault_tasks[:crews_per_ship * num_ships]
    remaining_capacity = crews_per_ship * num_ships - len(selected_tasks)

    if remaining_capacity > 0:
        other_tasks = sorted(other_tasks, key=lambda x: x["hours"], reverse=True)
        selected_tasks.extend(other_tasks[:remaining_capacity])

    return selected_tasks

# 自适应变邻域搜索算法
def adaptive_vns():
    initial_tasks = generate_initial_solution()
    assigned_tasks = task_assignment(initial_tasks, NUM_SHIPS, NUM_CREWS_PER_SHIP)
    current_solution = assigned_tasks
    current_cost = objective_function(current_solution)
    best_solution = current_solution[:]
    best_cost = current_cost

    iterations = 100
    for _ in range(iterations):
        destroyed_solution = destroy_solution(current_solution[:])
        repaired_solution = repair_solution(destroyed_solution[:])

        filtered_solution = [task for task in repaired_solution if is_within_safe_window(task)]

        new_cost = objective_function(filtered_solution)

        if new_cost is not None and (best_cost is None or new_cost < best_cost):
            best_solution = filtered_solution
            best_cost = new_cost

        current_solution = filtered_solution
        current_cost = new_cost

    return best_solution, best_cost

# 执行算法
best_schedule, best_cost = adaptive_vns()

# 计算每个任务的开始时间
current_time = datetime.strptime(f"{START_DATE} {START_TIME}", '%Y-%m-%d %H:%M')
output_schedule = []

for task in best_schedule:
    route_time = ROUTE_TIMES.get("dock_" + task["position"], 0)
    start_time = current_time + timedelta(hours=route_time)
    end_time = start_time + timedelta(hours=task["hours"])

    output_schedule.append({
        "任务": task["name"],
        "开始时间": start_time.strftime('%Y-%m-%d %H:%M'),
        "结束时间": end_time.strftime('%Y-%m-%d %H:%M'),
        "位置": task["position"],
        "类型": task["type"],
    })

    current_time = end_time

output = {
    "最佳调度方案": output_schedule,
    "最低成本": best_cost
}

# 打印最佳调度方案和最低成本
print(json.dumps(output, ensure_ascii=False, indent=4))
