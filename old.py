import heapq
from collections import deque
import matplotlib.pyplot as plt


class Process:
    def __init__(self, process, arrival_time, burst_time, priority):
        self.process = process
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.remaining_time = burst_time
        self.start_time = None
        self.finish_time = None


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
        timeline.append((process.process, current_time, process.finish_time))
        current_time = process.finish_time
    return timeline


def sjf(processes):
    timeline = []
    ready_queue = []
    current_time = 0
    remaining_processes = sorted(processes, key=lambda p: p.arrival_time)

    while remaining_processes or ready_queue:
        while remaining_processes and remaining_processes[0].arrival_time <= current_time:
            heapq.heappush(ready_queue, (remaining_processes[0].burst_time, remaining_processes[0]))
            remaining_processes.pop(0)

        if ready_queue:
            _, process = heapq.heappop(ready_queue)
            process.start_time = current_time
            process.finish_time = current_time + process.burst_time
            timeline.append((process.process, current_time, process.finish_time))
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
            timeline.append((process.process, current_time, process.finish_time))
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
                    timeline.append((current_process.process, current_process.start_time, current_time))
                next_process.start_time = current_time
            current_process = next_process
            current_process.remaining_time -= 1
            current_time += 1

            if current_process.remaining_time == 0:
                current_process.finish_time = current_time
                timeline.append((current_process.process, current_process.start_time, current_time))
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
                    timeline.append((current_process.process, current_process.start_time, current_time))
                next_process.start_time = current_time
            current_process = next_process
            current_process.remaining_time -= 1
            current_time += 1

            if current_process.remaining_time == 0:
                current_process.finish_time = current_time
                timeline.append((current_process.process, current_process.start_time, current_time))
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

            timeline.append((current_process.process, current_process.start_time, current_time))

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
            f"| {p.process:2d} | {p.arrival_time:11d} "
            f"| {p.burst_time:10d} | {p.priority:8d} "
            f"| {p.finish_time - p.start_time:13d} "
            f"| {p.turnaround_time:14d} | {p.waiting_time:11d} |")
    print("+----+-------------+------------+----------+---------------+----------------+-------------+")
    print(f"Average Turnaround Time: {avg_turnaround_time:.2f}")
    print(f"Average Waiting Time: {avg_waiting_time:.2f}")


def plot_gantt_chart(timeline, processes):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_ylim(0, len(processes))
    ax.set_xlabel('Time')
    ax.set_ylabel('Process')
    ax.set_yticks(range(1, len(processes) + 1))
    ax.set_yticklabels([f'P{p.process}' for p in processes])

    for i, (pprocess, start, end) in enumerate(timeline):
        ax.barh(pprocess, end - start, left=start, height=0.5, align='center', alpha=0.8)
        ax.text((start + end) / 2, pprocess, f'P{pprocess}', ha='center', va='center')

    plt.title('Gantt Chart')
    plt.grid(axis='x')
    plt.tight_layout()
    plt.show()


def main():
    processes = get_input()

    while True:
        print("\nChoose a scheduling algorithm:")
        print("1. FCFS (First Come First Serve)")
        print("2. SJF (Shortest Job First)")
        print("3. Non-Preemptive Priority")
        print("4. SRTF (Shortest Remaining Time First)")
        print("5. Preemptive Priority")
        print("6. Round Robin (Time Quantum = 4 ms)")
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
            timeline = round_robin(processes, time_quantum=4)
        else:
            print("Invalid process choice. Please try again.")
            continue

        avg_turnaround_time, avg_waiting_time = calculate_metrics(processes)
        print_table(processes, avg_turnaround_time, avg_waiting_time)
        plot_gantt_chart(timeline, processes)

        # Reset process states for the next algorithm
        for p in processes:
            p.remaining_time = p.burst_time
            p.start_time = None
            p.finish_time = None


if __name__ == "__main__":
    main()
