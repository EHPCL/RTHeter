import pickle
import numpy as np

from dagenv import DAGEnv



if __name__ == '__main__':
    
    env = DAGEnv(991, 1.5)
    state, dep = env.reset()
    file = open("./episode_160.0_list.pkl", 'rb')

    done = False
    time, proc_state, task_states, request = state

    data = pickle.load(file)    

    for d in data:

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


