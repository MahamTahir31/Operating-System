# PROCESS SCHEDULING THROUGH SJF, SRTF AND HRRN
# _____________________________________________
import pandas as pd # using pandas to show output in a table form

class Process: # declaring and initializing different paramters
    def __init__(self, process_id, arrival_time, execution_time):
        self.process_id = process_id
        self.arrival_time = arrival_time
        self.execution_time = execution_time
        self.remaining_time = execution_time
        self.start_time = 0
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0
        self.utilization = 0
        
def srtf(processes): # function for SRTF Algo
    current_time = 0
    execution_order = []
    remaining_processes = processes.copy()
    active_process = None

    while remaining_processes:
        # Find the process with the shortest remaining time
        shortest_remaining_time = float('inf')
        for process in remaining_processes:
            if process.arrival_time <= current_time and process.remaining_time < shortest_remaining_time:
                shortest_remaining_time = process.remaining_time
                active_process = process

        if active_process:
            # Record execution order
            execution_order.append(active_process.process_id)

            # Update start time
            if active_process.start_time == 0:
                active_process.start_time = current_time

            # Decrement remaining time
            active_process.remaining_time -= 1

            # Check if the process is completed
            if active_process.remaining_time == 0:
                active_process.completion_time = current_time + 1
                active_process.turnaround_time = active_process.completion_time - active_process.arrival_time
                active_process.waiting_time = active_process.turnaround_time - active_process.execution_time
                active_process.utilization = (active_process.execution_time / active_process.turnaround_time) * 100
                remaining_processes.remove(active_process)

            current_time += 1
        else:
            current_time += 1

    return execution_order

def srtf_gantt_chart(execution_order): # gantt chart of processes following SRJF Algo
    gantt_chart = []
    current_time = 0

    for process_id in execution_order:
        while current_time < len(gantt_chart):
            if gantt_chart[current_time] == "":
                break
            current_time += 1
        gantt_chart.extend([f"P{process_id}"] * (current_time + 1 - len(gantt_chart)))
    print("\n\t\t\t\t\t\t     GANTT CHART\n\t\t\t\t\t\t  ==================\n")
    print("\t\t\t\t\t\t   |", end="")
    for time_slot in gantt_chart:
        print(time_slot.center(3), end="|")
    print()

def sjf(processes): # function for SJF Algo
    processes.sort(key=lambda x: (x[1], x[2], x[0]))  # Sort by arrival time, execution time, and process ID
    time = 0
    result = []
    gantt_chart = []

    while processes:
        eligible_processes = [p for p in processes if p[1] <= time]
        if not eligible_processes:
            time += 1
            gantt_chart.append("-")
            continue

        eligible_processes.sort(key=lambda x: (x[2], x[0]))  # Sort by execution time and process ID
        next_process = eligible_processes.pop(0)
        start_time = max(time, next_process[1])
        time = start_time + next_process[2]
        next_process[3] = start_time
        next_process[4] = start_time + next_process[2]
        next_process[7] = round((next_process[2] / next_process[4]),2)
        result.append(next_process)
        gantt_chart.append(f"P{next_process[0]}")

        processes.remove(next_process)

    result.sort(key=lambda x: x[0])  # Sort the result by Process ID
    return result, gantt_chart

def hrrn(processes): # function for HRRN Algo
    current_time = 0
    execution_order = []
    remaining_processes = processes.copy()

    while remaining_processes:
        # Calculate the response ratio for each process and store them in a dictionary
        response_ratios = {}
        for process in remaining_processes:
            if process.arrival_time <= current_time:
                waiting_time = current_time - process.arrival_time
                response_ratio = (waiting_time + process.execution_time) / process.execution_time
                response_ratios[process] = response_ratio

        if response_ratios:
            # Select the process with the highest response ratio
            next_process = max(response_ratios, key=response_ratios.get)

            # Record execution order
            execution_order.append(next_process.process_id)

            # Update start time
            if next_process.start_time == 0:
                next_process.start_time = current_time

            # Decrement remaining time
            next_process.remaining_time -= 1

            # Check if the process is completed
            if next_process.remaining_time == 0:
                next_process.completion_time = current_time + 1
                next_process.turnaround_time = next_process.completion_time - next_process.arrival_time
                next_process.waiting_time = next_process.turnaround_time - next_process.execution_time
                next_process.utilization = (next_process.execution_time / next_process.turnaround_time) * 100
                remaining_processes.remove(next_process)

            current_time += 1
        else:
            current_time += 1

        # Print the Response Ratios for each process at each step
        print("Step:", current_time)
        for process, rr in response_ratios.items():
            print(f"Process P{process.process_id}: RR = {rr:.2f}")

    return execution_order


def main():
    algo = input("\nChoose scheduling algorithm (SJF, SRTF, HRRN): ").upper()

    num_processes = int(input("\nEnter the number of processes: "))
    if num_processes >= 3:
        processes = []
        if (algo == "SRTF"):
            for i in range(num_processes):
                process_id = i + 1
                arrival_time = int(input(f"\nEnter arrival time for process {process_id}: "))
                execution_time = int(input(f"Enter execution time for process {process_id}: "))
                processes.append(Process(process_id, arrival_time, execution_time))  # Create Process objects
            print("\n\t\t\t\t\t PROCESS SCHEDULING THROUGH \"SRTF\"\n\t\t\t\t\t==================================")
            execution_order = srtf(processes)  # Call the SRTF scheduling function
            

            for process in processes:  # Iterate over the original processes list, not execution_order
                process.waiting_time = process.start_time - process.arrival_time  # Calculate wait time
                process.turnaround_time = process.completion_time - process.arrival_time  # Calculate turnaround time

            # Calculate statistics based on the original processes list
            total_wait_time = sum(process.waiting_time for process in processes)
            total_turnaround_time = sum(process.turnaround_time for process in processes)
            total_utilization = sum((process.execution_time / process.turnaround_time) * 100 for process in processes)

            avg_wait_time = round((total_wait_time / num_processes), 2)
            avg_turnaround_time = round((total_turnaround_time / num_processes), 2)
            avg_utilization = round((total_utilization / num_processes), 2)

            df = pd.DataFrame([vars(process) for process in processes],
                            columns=["process_id", "arrival_time", "execution_time", "start_time", "completion_time", "waiting_time", "turnaround_time", "utilization"])

            print("\n", df.to_string(index=False))
            print(f"\n-> Average Wait Time: {avg_wait_time}")
            print(f"-> Average Turnaround Time: {avg_turnaround_time}")
            print(f"-> Utilization Rate of Whole System: {avg_utilization}%")
            srtf_gantt_chart(execution_order)

            
        elif algo == "SJF":
            for i in range(num_processes):
                process_id = i + 1
                arrival_time = int(input(f"\nEnter arrival time for process {process_id}: "))
                execution_time = int(input(f"Enter execution time for process {process_id}: "))
                processes.append([process_id, arrival_time, execution_time, 0, 0, 0, 0, 0])

            print("\n\t\t\t\t\t PROCESS SCHEDULING THROUGH \"SJF\"\n\t\t\t\t\t=================================")
            result, gantt_chart = sjf(processes)

            for process in result:
                process[5] = process[3] - process[1]  # Calculate wait time
                process[6] = process[4] - process[1]  # Calculate turnaround time

            total_wait_time = sum(process[5] for process in result)
            total_turnaround_time = sum(process[6] for process in result)
            total_utilization = sum(process[7] for process in result)
            
            avg_wait_time = round((total_wait_time / num_processes), 2)
            avg_turnaround_time = round((total_turnaround_time / num_processes), 2)
            avg_utilization = round((total_utilization / num_processes), 2)

            df = pd.DataFrame(result, columns=["Process ID", "Arrival Time", "Execution Time", "Start Time", "Completion Time", "Wait Time", "Turnaround Time", "Utilization"])
            print("\n", df.to_string(index=False))
        
            print(f"\n-> Average Wait Time: {avg_wait_time}")
            print(f"-> Average Turnaround Time: {avg_turnaround_time}")
            print(f"-> Utilization Rate of Whole System: {avg_utilization}%")
            # Display Gantt Chart
            print("\n\t\t\t\t\t\t   GANTT CHART\n\t\t\t\t\t\t=================")
            print("\n\t\t\t\t\t\t|", " |".join(gantt_chart), "|")


        elif algo == "HRRN":
            for i in range(num_processes):
                process_id = i + 1
                arrival_time = int(input(f"\nEnter arrival time for process {process_id}: "))
                execution_time = int(input(f"Enter execution time for process {process_id}: "))
                processes.append(Process(process_id, arrival_time, execution_time))
            
            print("\n\t\t\t\t\t PROCESS SCHEDULING THROUGH \"HRRN\"\n\t\t\t\t\t==================================")
            execution_order = hrrn(processes)  # Call the HRRN scheduling function
            for process in processes:  # Iterate over the original processes list, not execution_order
                process.waiting_time = process.start_time - process.arrival_time  # Calculate wait time
                process.turnaround_time = process.completion_time - process.arrival_time  # Calculate turnaround time

            # Calculate statistics based on the original processes list
            total_wait_time = sum(process.waiting_time for process in processes)
            total_turnaround_time = sum(process.turnaround_time for process in processes)
            total_utilization = sum((process.execution_time / process.turnaround_time) * 100 for process in processes)

            avg_wait_time = round((total_wait_time / num_processes), 2)
            avg_turnaround_time = round((total_turnaround_time / num_processes), 2)
            avg_utilization = round((total_utilization / num_processes), 2)

            df = pd.DataFrame([vars(process) for process in processes],
                            columns=["process_id", "arrival_time", "execution_time", "start_time", "completion_time", "waiting_time", "turnaround_time", "utilization"])

            print("\n", df.to_string(index=False))
            print(f"\n-> Average Wait Time: {avg_wait_time}")
            print(f"-> Average Turnaround Time: {avg_turnaround_time}")
            print(f"-> Utilization Rate of Whole System: {avg_utilization}%")
            gantt_chart = []
            current_time = 0

            for process_id in execution_order:
                while current_time < len(gantt_chart):
                    if gantt_chart[current_time] == "":
                        break
                    current_time += 1
                gantt_chart.extend([f"P{process_id}"] * (current_time + 1 - len(gantt_chart)))

            print("\n\t\t\t\t\t\t\tGANTT CHART\n\t\t\t\t\t\t=====================\n")
            print("\t\t\t\t\t\t     |", end="")
            for time_slot in gantt_chart:
                print(time_slot.center(3), end="|")
            print()
                    
        else:
            print("\nInvalid algorithm choice!")
            return
        
    else:
        print("\nProcesses must be at least 3 to be scheduled!")

if __name__ == "__main__":
    main()