# Copy Right.
# The EHPCL 2025 Authors.

# This python script implement EDF scheduler
# Based on synthetic self-suspension tasks

from environment import SimulationEnv

from numpy import random

random.seed(179)
# Test with different random seeds
for seeds in range(1, 10000):

    # Step 1: create the simulation environment
    env = SimulationEnv(seeds, utilization=2.3)

    # Step 2: reset the environment
    state = env.reset()
    period = [state[17 + 14 * i] for i in range(5)]
    env.client.set_simulation_timebound(period[-1]) + 1
    done = False

    idle_schedule_count = 0

    # Step 3: perform scheduling until receive "terminate"
    while not done:

        # get the time stamp
        current_time = env.current_time
        # calculate the deadlines
        deadline = [period[i] - current_time%period[i] for i in range(5)]
        if current_time == 30:
            print(f"deadline: {deadline}")
        sorted_indices = sorted(range(len(deadline)), key=lambda x: deadline[x])

        to_schedule = [True for _ in range(5)]
        for i in range(5):
            if int(state[19+14*i])!=-1:
                to_schedule[i] = False

        cpuTaskList = []
        gpuTaskList = []
        for tskIndex in sorted_indices:
            if to_schedule[tskIndex]==False:
                continue
            if int(state[18+14*tskIndex])%2==0:
                if len(cpuTaskList) < 2:
                    if int(state[20+14*tskIndex])>0:
                        cpuTaskList.append(tskIndex)
            else:
                if len(gpuTaskList) < 2:
                    if int(state[20+14*tskIndex])>0:
                        gpuTaskList.append(tskIndex)

        cpuStates = [state[2], state[6]]
        gpuStates = [state[10], state[14]]
        
        decisions = [0,0,0,0,0]
        for i in range(len(cpuTaskList)):
            for j in range(2):
                if int(cpuStates[j])==0:
                    decisions[cpuTaskList[i]] = j+1
                    cpuStates[j] = 10
                    break
                elif int(cpuStates[j])==1:
                    if deadline[int(state[j*4+3])] > deadline[cpuTaskList[i]]:
                        decisions[cpuTaskList[i]] = j+1
                        break

        for i in range(len(gpuTaskList)):
            for j in range(2):
                if int(gpuStates[j])==0:
                    decisions[gpuTaskList[i]] = j+3
                    gpuStates[j] = 2
                    break

        print(env.client.send_command("printSimulatorState "))
        print(f"cpuList: {cpuTaskList}")
        print(f"gpuList: {gpuTaskList}")
        print(f"decision: {decisions}")

        while int(state[0])==current_time:
            print(f"make decision! Task {state[-7]}")
            decision = decisions[int(state[-7])]
            state, _ , done, __ = env.step(decision)
            idle_schedule_count += 1 if decision==0 else 0
            # a = input()
            print(env.client.send_command("printSimulatorState "))
            

    # 6, 11 ,9 , 23, 19
    # 30, 36, 45, 60, 180
    if env.current_time < 199:
        print(f"Scheduling failed at seed: {seeds}!\n")
    else:
        print(f"Scheduling succeeded at seed: {seeds}!\n")
        
    a = input(f"Press enter to proceed to next, seed={seeds+1}\n")
