import pickle
import numpy as np

from dagenv import DAGEnv



if __name__ == '__main__':
    
    env = DAGEnv(991, 1.5)
    state, dep = env.reset()
    file = open("./episode_160.0_list.pkl", 'rb')

    done = False
    time, proc_state, task_states, request = state
    typeDict = {0: "CPU", 7: "GPU"}
    task_unit = np.zeros(env.task_num, dtype=int)
    for i in range(env.task_num):
        for seg in task_states[i]: task_unit[i]+= seg[3]

    data = pickle.load(file)    

    for d in data:

        print(f"Scheduling Request, type: {typeDict[state[-1][0]]}, index: {state[-1][1]}, count: {state[-1][2]}")
        execution = env.client.query_task_execution_states()
        print("Execution Progress: ", end=None)
        for i in range(env.task_num):
            print(f"Task {i}: {execution[i]}/{task_unit[i]}", end=", ")
        print()
        
        timestamp = d[0]
        task_id, node_id = d[1]
        state, reward, done,_=env.step(task_id, node_id)

        print(f"Time {timestamp}, schedule task {task_id} segment {node_id}, period: {task_states[task_id][node_id][5]}")
        env.visualize_all_tasks()
        print()
        input("Enter to continue...")
        from os import system
        system('clear')
    
    print("Scheduling completed successfully!\n")
    file.close()


