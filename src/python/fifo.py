# Copy Right.
# The 2025 EHPCL Authors

# This python script adopts FIFO (first in first out) scheduling


from client import SimulatorClient

if __name__ == "__main__":
    # default scheduler example
    simulator = SimulatorClient("../../build/main")

    # Step 1: initilization
    CPU = 0; GPU = 7
    simulator.create_processor(CPU, 2)
    simulator.create_processor(GPU, 2)

    # create 5 tasks
    for i in range(5):
        filename = f"/home/hamster/HeterSchedulerSim/test/.taskset_prop/task{i}.txt"
        with open(filename) as taskfile:
            period: int = int(taskfile.readline().strip())
            line = taskfile.readline().strip()
            segs = tuple(map(int, line.split()))
            simulator.create_heter_ss_task(period, 2, (CPU, GPU), segs)
    simulator.set_simulation_timebound(200)
    simulator.start_simulation()
    simulator.print()

    # step 2: scheduling loop
    procAffinity = [0,0,7,7]

    timeStamp = 0
    while (not simulator.is_simulation_completed()):
        #schedule decision here

        procState = simulator.query_processor_states()
        for i in range(4):
            if procState[i][1] != 0: continue
            for j in range(5):
                period, segState = simulator.query_task_state(j)
                for k, seg in enumerate(segState):
                    affinity = seg[0]; isReady = seg[2]; currentProc = seg[1]
                    if (procAffinity[i] != seg[0]): continue
                    if (isReady==1 and currentProc==-1):
                        simulator.schedule_segment_on_processor(i, j, k)
                procState = simulator.query_processor_states()
                if procState[i][1] != 0: break

        simulator.update_processor_and_task()
        simulator.print()

        timeStamp = timeStamp + 1
        if simulator.does_task_miss_deadline():
            print("Task Missing Deadline!\n")
            break

        a = input("Enter to continue...")

