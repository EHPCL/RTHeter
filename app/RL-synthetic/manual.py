# Copy Right.
# The EHPCL 2025 Authors.

# This python script is for environment debugging
# You can feel how challenging it is!

from environment import SimulationEnv

env = SimulationEnv(6122, 2.4)

state = env.reset()

done = False

acc_reward = 0

while not done:
    # The taskset features self-suspension structure
    # The i-th segment is CPU task if i%2==0
    # The i-th segment is GPU task if i%2==1 
    env.debug_print()
    
    # enter exactly one integer ranging from 0 to 4
    # 0 -> skip this round, do nothing (useful for reserving resources)
    # 1, 2 -> schedule onto CPU 0 / CPU 1, respectively
    # 3, 4 -> schedule onto GPU 0 / GPU 1, respectively
    # illegal scheduling such as schedule CPU task on GPUs leads to negative rewards
    decision = input(f"Please make decision for task {int(state[-7])}, seg {int(state[-6])}:")
    
    state, reward, done , info = env.step(int(decision))
    
    import os
    os.system("clear")
    
    acc_reward += reward
    print(f"Get reward {reward}, accumulated reward: {acc_reward}")

