import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from collections import deque


class Process:
    def __init__(self, id, arrival_time, burst_time, priority):
        self.id = id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.remaining_time = burst_time
        self.start_time = None
        self.finish_time = None


def fcfs(processes):
    time = 0
    schedule = []
    for p in sorted(processes, key=lambda x: x.arrival_time):
        if time < p.arrival_time:
            time = p.arrival_time
        p.start_time = time
        schedule.append((time, p.id))
        time += p.burst_time
        p.finish_time = time
    return schedule


def sjf(processes):
    time = 0
    remaining = sorted(processes, key=lambda x: x.arrival_time)
    schedule = []
    while remaining:
        available = [p for p in remaining if p.arrival_time <= time]
        if not available:
            time = min(p.arrival_time for p in remaining)
            continue
        next_process = min(available, key=lambda x: x.burst_time)
        next_process.start_time = time
        schedule.append((time, next_process.id))
        time += next_process.burst_time
        next_process.finish_time = time
        remaining.remove(next_process)
    return schedule


def non_preemptive_priority(processes):
    time = 0
    remaining = sorted(processes, key=lambda x: x.arrival_time)
    schedule = []
    while remaining:
        available = [p for p in remaining if p.arrival_time <= time]
        if not available:
            time = min(p.arrival_time for p in remaining)
            continue
        next_process = min(available, key=lambda x: x.priority)
        next_process.start_time = time
        schedule.append((time, next_process.id))
        time += next_process.burst_time
        next_process.finish_time = time
        remaining.remove(next_process)
    return schedule


def srtf(processes):
    time = 0
    remaining = sorted(processes, key=lambda x: x.arrival_time)
    schedule = []
    current_process = None
    while remaining or current_process:
        if not current_process and not [p for p in remaining if p.arrival_time <= time]:
            time = min(p.arrival_time for p in remaining)
            continue
        available = [p for p in remaining if p.arrival_time <= time]
        if current_process:
            available.append(current_process)
        next_process = min(available, key=lambda x: x.remaining_time)
        if next_process != current_process:
            if current_process:
                schedule.append((time, current_process.id))
            current_process = next_process
            if current_process in remaining:
                remaining.remove(current_process)
            if current_process.start_time is None:
                current_process.start_time = time
        time += 1
        current_process.remaining_time -= 1
        if current_process.remaining_time == 0:
            current_process.finish_time = time
            schedule.append((time, current_process.id))
            current_process = None
    return schedule


def preemptive_priority(processes):
    time = 0
    remaining = sorted(processes, key=lambda x: x.arrival_time)
    schedule = []
    current_process = None
    while remaining or current_process:
        if not current_process and not [p for p in remaining if p.arrival_time <= time]:
            time = min(p.arrival_time for p in remaining)
            continue
        available = [p for p in remaining if p.arrival_time <= time]
        if current_process:
            available.append(current_process)
        next_process = min(available, key=lambda x: x.priority)
        if next_process != current_process:
            if current_process:
                schedule.append((time, current_process.id))
            current_process = next_process
            if current_process in remaining:
                remaining.remove(current_process)
            if current_process.start_time is None:
                current_process.start_time = time
        time += 1
        current_process.remaining_time -= 1
        if current_process.remaining_time == 0:
            current_process.finish_time = time
            schedule.append((time, current_process.id))
            current_process = None
    return schedule


def round_robin(processes, time_quantum=4):
    time = 0
    remaining = deque(sorted(processes, key=lambda x: x.arrival_time))
    schedule = []
    current_process = None
    time_left = 0
    while remaining or current_process:
        if not current_process and not [p for p in remaining if p.arrival_time <= time]:
            time = min(p.arrival_time for p in remaining)
        available = [p for p in remaining if p.arrival_time <= time]
        if not current_process or time_left == 0:
            if current_process:
                if current_process.remaining_time > 0:
                    remaining.append(current_process)
                schedule.append((time, current_process.id))
            if available:
                current_process = available[0]
                remaining.remove(current_process)
                time_left = min(time_quantum, current_process.remaining_time)
                if current_process.start_time is None:
                    current_process.start_time = time
            else:
                current_process = None
                time_left = 0
        if current_process:
            time += 1
            current_process.remaining_time -= 1
            time_left -= 1
            if current_process.remaining_time == 0:
                current_process.finish_time = time
                schedule.append((time, current_process.id))
                current_process = None
                time_left = 0
        else:
            time += 1
    return schedule


def calculate_metrics(processes):
    for p in processes:
        if p.finish_time is None or p.start_time is None:
            p.turnaround_time = None
            p.waiting_time = None
        else:
            p.turnaround_time = p.finish_time - p.arrival_time
            p.waiting_time = p.turnaround_time - p.burst_time
    completed_processes = [p for p in processes if p.turnaround_time is not None]
    if completed_processes:
        avg_turnaround = sum(p.turnaround_time for p in completed_processes) / len(completed_processes)
        avg_waiting = sum(p.waiting_time for p in completed_processes) / len(completed_processes)
    else:
        avg_turnaround = avg_waiting = 0
    return avg_turnaround, avg_waiting


def plot_results(processes, schedule, algorithm_name, avg_turnaround, avg_waiting):
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 12), gridspec_kw={'height_ratios': [1, 2, 0.5]})
    fig.suptitle(f'CPU Scheduling - {algorithm_name}')

    # Table
    cell_text = [[p.id, p.arrival_time, p.burst_time, p.priority,
                  p.start_time if p.start_time is not None else 'N/A',
                  p.finish_time if p.finish_time is not None else 'N/A',
                  p.turnaround_time if p.turnaround_time is not None else 'N/A',
                  p.waiting_time if p.waiting_time is not None else 'N/A'] for p in processes]
    columns = ['Process', 'Arrival Time', 'Burst Time', 'Priority', 'Start Time', 'Finish Time',
               'Turnaround Time', 'Waiting Time']
    ax1.axis('tight')
    ax1.axis('off')
    table = ax1.table(cellText=cell_text, colLabels=columns, cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1, 1.5)

    # Gantt chart
    ax2.set_ylim(0, 1)
    max_time = max(t for t, _ in schedule) if schedule else 0
    ax2.set_xlim(0, max_time)
    ax2.set_xlabel('Time (ms)')
    ax2.set_yticks([])

    process_colors = plt.cm.get_cmap('Set3')(np.linspace(0, 1, len(processes)))
    color_map = {p.id: process_colors[i] for i, p in enumerate(processes)}

    for i in range(len(schedule) - 1):
        start, proc_id = schedule[i]
        end, _ = schedule[i + 1]
        ax2.broken_barh([(start, end - start)], (0, 1), facecolors=color_map[proc_id])
        ax2.text((start + end) / 2, 0.5, f'P{proc_id}', ha='center', va='center')

    # Show arrivals and queue changes
    arrivals = sorted(set(p.arrival_time for p in processes))
    for t in arrivals:
        ax2.axvline(x=t, color='r', linestyle='--', alpha=0.5)
        arriving = [p.id for p in processes if p.arrival_time == t]
        ax2.text(t, -0.05, f'A: {",".join(map(str, arriving))}', ha='center', va='top', rotation=90)

    queue_changes = sorted(set(t for t, _ in schedule))
    for t in queue_changes:
        queue = [p.id for p in processes if p.arrival_time <= t and (p.finish_time is None or p.finish_time > t)]
        ax2.text(t, -0.1, f'Q: {",".join(map(str, queue))}', ha='center', va='top', rotation=90)

    legend_elements = [Patch(facecolor=color_map[p.id], label=f'P{p.id}') for p in processes]
    ax2.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=5)

    # Set x-axis ticks to integer values
    ax2.set_xticks(range(0, max_time + 1))
    ax2.tick_params(axis='x', rotation=90)

    # Average Turnaround and Waiting Time
    ax3.axis('off')
    ax3.text(0.5, 0.6, f'Average Turnaround Time: {avg_turnaround:.2f}', ha='center', va='center')
    ax3.text(0.5, 0.2, f'Average Waiting Time: {avg_waiting:.2f}', ha='center', va='center')

    plt.tight_layout()
    plt.show()


def main():
    processes = [
        Process(1, 0, 10, 3),
        Process(2, 2, 1, 1),
        Process(3, 4, 2, 4),
        Process(4, 6, 1, 2),
        Process(5, 8, 5, 5)
    ]

    algorithms = {
        1: ('FCFS', fcfs),
        2: ('SJF', sjf),
        3: ('Non-Preemptive Priority', non_preemptive_priority),
        4: ('SRTF', srtf),
        5: ('Preemptive Priority', preemptive_priority),
        6: ('Round Robin', round_robin)
    }

    print("Choose a scheduling algorithm:")
    for key, value in algorithms.items():
        print(f"{key}. {value[0]}")

    choice = int(input("Enter your choice (1-6): "))

    algorithm_name, algorithm_func = algorithms[choice]

    # Reset remaining time for each process
    for p in processes:
        p.remaining_time = p.burst_time
        p.start_time = None
        p.finish_time = None

    schedule = algorithm_func(processes)
    avg_turnaround, avg_waiting = calculate_metrics(processes)

    print(f"\nAverage Turnaround Time: {avg_turnaround:.2f}")
    print(f"Average Waiting Time: {avg_waiting:.2f}")

    plot_results(processes, schedule, algorithm_name, avg_turnaround, avg_waiting)


if __name__ == "__main__":
    main()