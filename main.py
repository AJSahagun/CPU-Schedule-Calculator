import heapq
from collections import deque
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import pyplot


class Process:
    def __init__(self, name, arrival_time, burst_time, priority):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.remaining_time = burst_time
        self.start_time = None
        self.finish_time = None

    def __lt__(self, other):
        return self.burst_time < other.burst_time


def get_input():
    processes = []
    n = int(input("Enter the number of processes: "))
    for i in range(n):
        print(f"\nProcess {i + 1}:")
        arrival_time = int(input("Arrival Time (ms): "))
        burst_time = int(input("Burst Time (ms): "))
        priority = int(input("Priority: "))
        processes.append(Process(i + 1, arrival_time, burst_time, priority))
    return processes


def fcfs(processes):
    timeline = []
    current_time = 0
    for process in sorted(processes, key=lambda p: p.arrival_time):
        if current_time < process.arrival_time:
            current_time = process.arrival_time
        process.start_time = current_time
        process.finish_time = current_time + process.burst_time
        timeline.append((process.name, current_time, process.finish_time))
        current_time = process.finish_time
    return timeline


def sjf(processes):
    timeline = []
    ready_queue = []
    current_time = 0
    remaining_processes = sorted(processes, key=lambda p: p.arrival_time)

    while remaining_processes or ready_queue:
        while remaining_processes and remaining_processes[0].arrival_time <= current_time:
            heapq.heappush(ready_queue, remaining_processes.pop(0))

        if ready_queue:
            process = heapq.heappop(ready_queue)
            process.start_time = current_time
            process.finish_time = current_time + process.burst_time
            timeline.append((process.name, current_time, process.finish_time))
            current_time = process.finish_time
        else:
            current_time = remaining_processes[0].arrival_time

    return timeline


def non_preemptive_priority(processes):
    timeline = []
    ready_queue = []
    current_time = 0
    remaining_processes = sorted(processes, key=lambda p: p.arrival_time)

    while remaining_processes or ready_queue:
        while remaining_processes and remaining_processes[0].arrival_time <= current_time:
            heapq.heappush(ready_queue, (remaining_processes[0].priority, remaining_processes[0]))
            remaining_processes.pop(0)

        if ready_queue:
            _, process = heapq.heappop(ready_queue)
            process.start_time = current_time
            process.finish_time = current_time + process.burst_time
            timeline.append((process.name, current_time, process.finish_time))
            current_time = process.finish_time
        else:
            current_time = remaining_processes[0].arrival_time

    return timeline


def srtf(processes):
    timeline = []
    ready_queue = []
    current_time = 0
    remaining_processes = sorted(processes, key=lambda p: p.arrival_time)
    current_process = None

    while remaining_processes or ready_queue or current_process:
        while remaining_processes and remaining_processes[0].arrival_time <= current_time:
            heapq.heappush(ready_queue, (remaining_processes[0].remaining_time, remaining_processes[0]))
            remaining_processes.pop(0)

        if current_process:
            heapq.heappush(ready_queue, (current_process.remaining_time, current_process))

        if ready_queue:
            _, next_process = heapq.heappop(ready_queue)
            if current_process != next_process:
                if current_process:
                    timeline.append((current_process.name, current_process.start_time, current_time))
                next_process.start_time = current_time
            current_process = next_process
            current_process.remaining_time -= 1
            current_time += 1

            if current_process.remaining_time == 0:
                current_process.finish_time = current_time
                timeline.append((current_process.name, current_process.start_time, current_time))
                current_process = None
        else:
            current_time = remaining_processes[0].arrival_time

    return timeline


def preemptive_priority(processes):
    timeline = []
    ready_queue = []
    current_time = 0
    remaining_processes = sorted(processes, key=lambda p: p.arrival_time)
    current_process = None

    while remaining_processes or ready_queue or current_process:
        while remaining_processes and remaining_processes[0].arrival_time <= current_time:
            heapq.heappush(ready_queue, (remaining_processes[0].priority, remaining_processes[0]))
            remaining_processes.pop(0)

        if current_process:
            heapq.heappush(ready_queue, (current_process.priority, current_process))

        if ready_queue:
            _, next_process = heapq.heappop(ready_queue)
            if current_process != next_process:
                if current_process:
                    timeline.append((current_process.name, current_process.start_time, current_time))
                next_process.start_time = current_time
            current_process = next_process
            current_process.remaining_time -= 1
            current_time += 1

            if current_process.remaining_time == 0:
                current_process.finish_time = current_time
                timeline.append((current_process.name, current_process.start_time, current_time))
                current_process = None
        else:
            current_time = remaining_processes[0].arrival_time

    return timeline


def round_robin(processes, time_quantum):
    timeline = []
    ready_queue = deque()
    current_time = 0
    remaining_processes = sorted(processes, key=lambda p: p.arrival_time)
    current_process = None

    while remaining_processes or ready_queue or current_process:
        while remaining_processes and remaining_processes[0].arrival_time <= current_time:
            ready_queue.append(remaining_processes.pop(0))

        if current_process:
            ready_queue.append(current_process)

        if ready_queue:
            current_process = ready_queue.popleft()
            current_process.start_time = current_time
            execution_time = min(time_quantum, current_process.remaining_time)
            current_process.remaining_time -= execution_time
            current_time += execution_time

            timeline.append((current_process.name, current_process.start_time, current_time))

            if current_process.remaining_time == 0:
                current_process.finish_time = current_time
                current_process = None
        else:
            current_time = remaining_processes[0].arrival_time

    return timeline


def calculate_metrics(processes):
    for process in processes:
        process.turnaround_time = process.finish_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time

    avg_turnaround_time = sum(p.turnaround_time for p in processes) / len(processes)
    avg_waiting_time = sum(p.waiting_time for p in processes) / len(processes)

    return avg_turnaround_time, avg_waiting_time


def print_table(processes, avg_turnaround_time, avg_waiting_time):
    print("\n+----+-------------+------------+----------+---------------+----------------+-------------+")
    print("| P | Arrival Time | Burst Time | Priority |      ET       |       TAT      |      WT     |")
    print("+----+-------------+------------+----------+---------------+----------------+-------------+")
    for p in processes:
        print(
            f"| {p.name:2d} | {p.arrival_time:11d} "
            f"| {p.burst_time:10d} | {p.priority:8d} "
            f"| {p.finish_time - p.start_time:13d} "
            f"| {p.turnaround_time:14d} | {p.waiting_time:11d} |")
    print("+----+-------------+------------+----------+---------------+----------------+-------------+")
    print(f"Average Turnaround Time: {avg_turnaround_time:.2f}")
    print(f"Average Waiting Time: {avg_waiting_time:.2f}")


def plot_gantt_chart(timeline, processes):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_ylim(0, 2)
    ax.set_xlabel('Time (ms)')
    ax.set_yticks([])

    colors = pyplot.get_cmap('tab10')(np.linspace(0, 1, len(processes)))
    color_map = {p.name: colors[i] for i, p in enumerate(processes)}

    max_time = max(end for _, _, end in timeline)
    ax.set_xlim(0, max_time)

    for pname, start, end in timeline:
        ax.barh(1, end - start, left=start, height=0.5, align='center', alpha=0.8, color=color_map[pname])
        ax.text((start + end) / 2, 1, f'P{pname}', ha='center', va='center', fontweight='bold')

    arrivals = [(p.arrival_time, f'P{p.name}') for p in processes]
    for time, pname in arrivals:
        ax.annotate(f'{pname} arrives', xy=(time, 0), xytext=(time, -0.2),
                    ha='center', va='top', rotation=90, fontsize=8)

    queue_changes = []
    current_queue = []
    for i, (pname, start, _) in enumerate(timeline):
        if i == 0 or pname != timeline[i-1][0]:
            queue_str = ', '.join([f'P{p}' for p in current_queue if p != pname])
            queue_changes.append((start, queue_str))
            if pname in current_queue:
                current_queue.remove(pname)
            else:
                current_queue.append(pname)

    for time, queue in queue_changes:
        if queue:
            ax.annotate(f'Queue: {queue}', xy=(time, 0), xytext=(time, -0.4),
                        ha='left', va='top', rotation=90, fontsize=8)

    ax.set_xticks(range(0, max_time + 1))
    ax.set_xticklabels(range(0, max_time + 1))
    plt.xticks(rotation=90)

    legend_elements = [plt.Rectangle((0, 0), 1, 1, fc=color_map[p.name], alpha=0.8, label=f'P{p.name}')
                       for p in processes]
    ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, 1.15),
              ncol=len(processes), title="Processes")

    plt.grid(axis='x')
    plt.tight_layout()
    plt.show()


def main():
    processes = get_input()
    quantum = 4

    while True:
        print("\nChoose a scheduling algorithm:")
        print("1. FCFS (First Come First Serve)")
        print("2. SJF (Shortest Job First)")
        print("3. Non-Preemptive Priority")
        print("4. SRTF (Shortest Remaining Time First)")
        print("5. Preemptive Priority")
        print(f"6. Round Robin (Time Quantum = {quantum} ms)")
        print("7. Exit")

        choice = int(input("Enter your choice (1-7): "))

        if choice == 7:
            break

        if choice == 1:
            timeline = fcfs(processes)
        elif choice == 2:
            timeline = sjf(processes)
        elif choice == 3:
            timeline = non_preemptive_priority(processes)
        elif choice == 4:
            timeline = srtf(processes)
        elif choice == 5:
            timeline = preemptive_priority(processes)
        elif choice == 6:
            timeline = round_robin(processes, time_quantum=quantum)
        else:
            print("Invalid choice. Please try again.")
            continue

        avg_turnaround_time, avg_waiting_time = calculate_metrics(processes)
        print_table(processes, avg_turnaround_time, avg_waiting_time)
        plot_gantt_chart(timeline, processes)

        for p in processes:
            p.remaining_time = p.burst_time
            p.start_time = None
            p.finish_time = None


if __name__ == "__main__":
    main()
