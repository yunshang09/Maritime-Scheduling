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
    {"id": "2D7", "latitude": 30.0, "longitude": 122.0, "field": "1"},
    {"id": "3A9", "latitude": 30.5, "longitude": 121.5, "field": "2"},
    {"id": "4B3", "latitude": 31.0, "longitude": 120.5, "field": "3"},
    {"id": "5C6", "latitude": 30.2, "longitude": 123.0, "field": "4"},
    {"id": "6D8", "latitude": 30.8, "longitude": 122.5, "field": "5"},
    {"id": "7E9", "latitude": 30.3, "longitude": 121.8, "field": "6"},
    {"id": "8F0", "latitude": 31.2, "longitude": 122.2, "field": "7"},
    {"id": "9G1", "latitude": 30.7, "longitude": 121.2, "field": "8"},
]

TASKS = [
    # {"name": "#3变桨位置传感器异常故障处理", "type": "故障", "hours": 3, "position": "WindFarm1"},
    {"name": "#3变桨位置传感器异常故障处理", "type": "故障", "hours": 3, "position": "1"},
    {"name": "叶片裂缝检测", "type": "缺陷", "hours": 4, "position": "2"},
    {"name": "发电机温度异常", "type": "故障", "hours": 3, "position": "3"},
    {"name": "主轴润滑系统检查", "type": "预警", "hours": 2, "position": "4"},
    {"name": "控制系统校准", "type": "定期运维", "hours": 5, "position": "5"},
    {"name": "电缆连接检查", "type": "缺陷", "hours": 1, "position": "6"},
    {"name": "传感器校准", "type": "定期运维", "hours": 3, "position": "7"},
    {"name": "变压器检查", "type": "预警", "hours": 2, "position": "8"},
]


WEATHER = [
    {"time": "00:00", "depth": {"0": 4.29, "1": 4.29, "2": 4.29, "3": 4.29, "4": 4.29, "5": 4.29, "6": 4.29, "7": 4.29, "8": 4.29}},
    {"time": "02:00", "depth": {"0": 2.75, "1": 2.75, "2": 2.75, "3": 2.75, "4": 2.75, "5": 2.75, "6": 2.75, "7": 2.75, "8": 2.75}},
    {"time": "04:00", "depth": {"0": 1.23, "1": 1.23, "2": 1.23, "3": 1.23, "4": 1.23, "5": 1.23, "6": 1.23, "7": 1.23, "8": 1.23}},
    {"time": "06:00", "depth": {"0": 0.55, "1": 0.55, "2": 0.55, "3": 0.55, "4": 0.55, "5": 0.55, "6": 0.55, "7": 0.55, "8": 0.55}},
    {"time": "08:00", "depth": {"0": 3.33, "1": 3.33, "2": 3.33, "3": 3.33, "4": 3.33, "5": 3.33, "6": 3.33, "7": 3.33, "8": 3.33}},
    {"time": "10:00", "depth": {"0": 4.12, "1": 4.12, "2": 4.12, "3": 4.12, "4": 4.12, "5": 4.12, "6": 4.12, "7": 4.12, "8": 4.12}},
    {"time": "12:00", "depth": {"0": 5.23, "1": 5.23, "2": 5.23, "3": 5.23, "4": 5.23, "5": 5.23, "6": 5.23, "7": 5.23, "8": 5.23}},
    {"time": "14:00", "depth": {"0": 4.02, "1": 4.02, "2": 4.02, "3": 4.02, "4": 4.02, "5": 4.02, "6": 4.02, "7": 4.02, "8": 4.02}},
    {"time": "16:00", "depth": {"0": 3.44, "1": 3.44, "2": 3.44, "3": 3.44, "4": 3.44, "5": 3.44, "6": 3.44, "7": 3.44, "8": 3.44}},
    {"time": "18:00", "depth": {"0": 2.32, "1": 2.32, "2": 2.32, "3": 2.32, "4": 2.32, "5": 2.32, "6": 2.32, "7": 2.32, "8": 2.32}},
    {"time": "20:00", "depth": {"0": 1.43, "1": 1.43, "2": 1.43, "3": 1.43, "4": 1.43, "5": 1.43, "6": 1.43, "7": 1.43, "8": 1.43}},
    {"time": "22:00", "depth": {"0": 3.24, "1": 3.24, "2": 3.24, "3": 3.24, "4": 3.24, "5": 3.24, "6": 3.24, "7": 3.24, "8": 3.24}}
]
weather_dict = {entry["time"]: entry["depth"] for entry in WEATHER}


def get_depth_at_time(time_str, position):
    depth = weather_dict.get(time_str, {}).get(str(position), None)
    return depth


# 时间矩阵（各个位置之间的到达时间）
data = {
    "time_matrix": [
        [0, 6, 9, 8, 7, 3, 6, 2, 3],
        [6, 0, 8, 3, 2, 6, 8, 4, 8],
        [9, 8, 0, 11, 10, 6, 3, 9, 5],
        [8, 3, 11, 0, 1, 7, 10, 6, 10],
        [7, 2, 10, 1, 0, 6, 9, 4, 8],
        [3, 6, 6, 7, 6, 0, 2, 3, 2],
        [6, 8, 3, 10, 9, 2, 0, 6, 2],
        [2, 4, 9, 6, 4, 3, 6, 0, 4],
        [3, 8, 5, 10, 8, 2, 2, 4, 0],
    ]
}


# 转换时间字符串为 datetime 对象
def str_to_datetime(time_str):
    return datetime.strptime(time_str, '%H:%M')


# 计算时间差（小时）
def time_diff(start, end):
    return (end - start).total_seconds() / 3600


# 时间回调
def get_travel_time(from_node, to_node):
    return data["time_matrix"][from_node][to_node]


# 检查任务的时间是否在安全窗口内，并且水深是否足够
def is_within_safe_window(previous_task, task):
    task_position = task["position"]
    if previous_task is None:
        last_position = 0
    else:
        last_position = previous_task["position"]
    for weather in WEATHER:
        start = str_to_datetime(weather["time"])
        route = get_travel_time(int(last_position), int(task_position))
        arrive = start + timedelta(hours=route)
        end = start + timedelta(hours=route + task["hours"])

        start_str = start.strftime('%H:%M')
        arrive_str = arrive.strftime('%H:%M')
        end_str = end.strftime('%H:%M')

        depth_start = get_depth_at_time(start_str, task_position)
        depth_arrive = get_depth_at_time(arrive_str, task_position)
        depth_end = get_depth_at_time(end_str, task_position)
        if depth_start is not None and depth_arrive is not None:
            if depth_start >= AVG_DRAFT and depth_arrive >= AVG_DRAFT:
                if start.time() >= str_to_datetime(START_TIME).time() and end.time() <= str_to_datetime(END_TIME).time():
                    return True
    return False


# 目标函数：计算总成本
def objective_function(schedule):
    start = datetime.strptime(f"{START_DATE} {START_TIME}", '%Y-%m-%d %H:%M')
    current_time= start
    last_position = 0
    total_downtime = 0
    for task in schedule:
        task_position = int(task["position"])
        travel_time = get_travel_time(last_position, task_position)
        end = current_time + timedelta(hours=travel_time + task["hours"])

        # 更新当前时间为任务结束时间
        current_time = end
        last_position = task_position
        total_downtime += time_diff(start, current_time)

    return total_downtime


# 生成初始解
def generate_initial_solution():
    schedule = []
    fault_tasks = [task for task in TASKS if task["type"] == "故障"]
    other_tasks = [task for task in TASKS if task["type"] != "故障"]

    # 确保故障任务被优先安排
    for task in fault_tasks:
        schedule.append(task)

    # 对其他任务按类型进行排序
    # other_tasks.sort(key=lambda x: (x["type"] == "预警", x["type"] == "定期运维"))
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

        # filtered_solution = [task for task in repaired_solution if is_within_safe_window(task)]
        filtered_solution = []
        previous_task = None  # 初始化上一个任务为 None

        for task in repaired_solution:
            if is_within_safe_window(previous_task, task):
                filtered_solution.append(task)

        new_cost = objective_function(filtered_solution)

        if new_cost is not None and (best_cost is None or new_cost < best_cost):
            best_solution = filtered_solution
            best_cost = new_cost

        current_solution = filtered_solution
        current_cost = new_cost

    return best_solution, best_cost


# 执行算法
best_schedule, best_cos = adaptive_vns()

# 计算每个任务的开始时间
current = datetime.strptime(f"{START_DATE} {START_TIME}", '%Y-%m-%d %H:%M')
output_schedule = []
last = 0
for task_item in best_schedule:
    position = task_item["position"]
    route_time = get_travel_time(last, int(position))
    start_time = current + timedelta(hours=route_time)
    end_time = start_time + timedelta(hours=task_item["hours"])

    output_schedule.append({
        "任务": task_item["name"],
        "开始时间": start_time.strftime('%Y-%m-%d %H:%M'),
        "结束时间": end_time.strftime('%Y-%m-%d %H:%M'),
        "位置": task_item["position"],
        "类型": task_item["type"],
    })

    now = end_time

output = {
    "最佳调度方案": output_schedule,
    "最低成本": best_cos
}

# 打印最佳调度方案和最低成本
print(json.dumps(output, ensure_ascii=False, indent=4))
