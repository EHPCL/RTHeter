# 
# Copy Right. The EHPCL Authors.
#

import numpy as np

class SimulationEnv:
    """ RL environment for interecting with the scheduling simulation python client.

    Main APIs:
    ---
        action_space: return tuple of available processor to schedule \n
        schedule: perform a scheduling command \n
        reset: restart the client \n
        update_time: update the timestamp by 1

    Notes:
        current processor and task patterns are fixed; Using same seed and utilization
    will reproduce **exact** same tasksets.
    """

    def __init__(self, seed: int, utilization: float = 2.0) -> None:
        import sys
        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        sim_path = os.path.join(current_dir, '../../src/python')
        if sim_path not in sys.path:
            sys.path.append(sim_path)

        self.seed = seed
        self.client = None
        self.utilization = utilization

        from rand import TaskRandomGenerator
        self.task_generator = TaskRandomGenerator(self.seed)
        self.accumulated_reward = 0

        self.task_state = np.zeros(5, dtype=tuple)
        self.avail_schedules = []
        self.searched_at = -1

        self.self_suspension = True
        self.to_schedule = [-1, -1]

        self.invalid_schedule_count = 0
        self.schedule_mask = [1.0, 1.0, 1.0, 1.0, 1.0]

    
    def __del__(self):
        del self.client

    def reset(self, flash_client = True):

        if flash_client:
            del self.client
            from client import SimulatorClient
            self.client = SimulatorClient("../../build/main")

            self.client.create_processor(0, 2)
            self.client.create_processor(7, 2)
            self.client.set_simulation_timebound(200)

            tasks = self.task_generator.generate(self.utilization)
            for task in tasks:
                self.client.create_heter_ss_task(task[0], 2, (0,7), task[1])
    
            self.client.start_simulation()
        else:
            self.reset_client()

        self.action_space = [-1, 0, 1, 2, 3]
    
        self.searched_at = -1
        self.to_schedule = [-1, -1]
        self.schedule_mask = [1.0, 1.0, 1.0, 1.0, 1.0]
        self.schedule_space()
        self.find_next_task()
        self.terminated = False
        self.survive_score = 0
        self.schedule_score = 0
        self.execution_score = 0
        self.invalid_schedule_count = 0
        self.current_time = self.client.get_current_time_stamp()

        return self.query_state()
    
    def reset_client(self) -> bool:
        return self.client.reset_client()

    def schedule_space(self) -> list:
        """search and return list of available schedulings

        Returns:
            list[tuple]: (i,j,k), schedule the k-th segment of j-th task on i-th processor
        """
        if self.client is None:
            from sys import stderr
            print("Please use reset() first before find the action spaces", file=stderr)
        self.query_state()
        if self.searched_at == self.client.get_current_time_stamp():
            return self.avail_schedules

        self.avail_schedules = []
        self.schedule_mask = [0.0 for _ in self.task_state]
        for i, proc_state in enumerate(self.proc_states):
            # ignore non-preemptive procs
            if proc_state[1] > 1: continue
            for j, task_state in enumerate(self.task_state):
                if self.self_suspension:
                    if task_state[2] != -1: continue
                    # already completed, negative index
                    if task_state[1] < 0: continue
                    # not same affinity
                    # if proc_state[0] != task_state[4][task_state[1]][0]: continue
                    self.avail_schedules.append((i, j, task_state[1]))
                    self.schedule_mask[j] = 1.0
                else:
                    for k,segment in enumerate(task_state[1]):
                        # not the same affinity
                        if segment[0]!=proc_state[0]: continue
                        # already on some processor, useless to schedule on others
                        if segment[1]!=-1: continue
                        # segment not ready yet
                        if segment[2]==0: continue
                        # segment is already completed
                        if segment[4]==0: continue
                        self.avail_schedules.append((i, j, k))
                        self.schedule_mask[j] = 1.0

        self.searched_at = self.client.get_current_time_stamp()

        return self.avail_schedules

    def find_next_task(self) -> None:
        # update self.to_schedule
        flag = False
        for taskId in range(self.to_schedule[0]+1, 5):
            if flag: break
            for action in self.avail_schedules:
                if action[1] == taskId:
                    self.to_schedule[0] = action[1]
                    self.to_schedule[1] = action[2]
                    flag = True
                    break
        if not flag:
            self.to_schedule[0] = -1

    def step(self, procId: int) -> 'tuple[tuple, float, bool, dict]':
        reward = 0.0
        procId = procId -1
        info = {}
        if (procId >= 0):
            reward = self.schedule(procId, self.to_schedule[0], self.to_schedule[1])
        else:
            self.survive_score += 1
            reward = 1.0 / (np.sum(self.schedule_mask)+1)
        self.find_next_task()
        while (self.to_schedule[0] == -1):
            # no action
            rewardacc, terminate = self.update_time()
            reward = reward + rewardacc
            if terminate:
                self.terminated = True
                return self.query_state(), reward, True, {"Survive": self.survive_score, "Schedule": self.schedule_score, "Execution": self.execution_score, "Endtime": self.current_time, "Invalid": self.invalid_schedule_count}
            self.schedule_space()
            self.find_next_task()

        return self.query_state(), reward, False, {}

    def schedule(self, procId:int, taskId: int, segId: int) -> float:
        """Perform the schedule command. The avail action is updated.

        Returns:
            reward (float): 0 if schedule a task, -1000 if wrong behavior
        """
        if (not (procId, taskId, segId) in self.avail_schedules):
            self.invalid_schedule_count += 1
            return -0.25
        reward = 1.15 if self.proc_states[procId][1]==0 else 0.95
        res = self.client.schedule_segment_on_processor(procId, taskId, segId)
        if res.find("Error")!=-1 :
            self.invalid_schedule_count += 1
            return -0.25

        new_avail_schedules = []
        for action in self.avail_schedules:
            if (action[0]==procId): continue
            if (action[1]==taskId and action[2]==segId): continue
            new_avail_schedules.append(action)
        self.avail_schedules = new_avail_schedules
        self.schedule_score += 1

        return reward / (np.sum(self.schedule_mask)+1)

    def decode_state(self) -> 'tuple':
        result = [float(self.client.get_current_time_stamp())]
        for proc_st in self.proc_states:
            for item in proc_st:
                result.append(float(item))
        for task in self.task_state:
            result.append(float(task[0]));result.append(float(task[1]))
            result.append(float(task[2]))
            result.append(float(task[3]))
            for seg in task[4]:
                result.append(float(seg[0])); result.append(float(seg[1]))
        result.append(float(self.to_schedule[0]))
        result.append(float(self.to_schedule[1]))
        result += self.schedule_mask
        return tuple(result)

    def query_state(self) -> 'tuple':
        self.current_time = self.client.get_current_time_stamp()
        self.proc_states: 'tuple' = self.client.query_processor_states()
        for i in range(5):
            if self.self_suspension:
                self.task_state[i] = self.client.query_ss_task_state(i)
            else:
                self.task_state[i] = self.client.query_task_state(i)
        
        return self.decode_state()
    
    def query_state_lazy(self) -> 'tuple':
        return self.decode_state()

    def is_terminated(self) -> bool:
        if self.client.does_task_miss_deadline(): return True
        if self.client.is_simulation_completed(): return True
        return False

    def update_time(self) -> 'tuple[float, bool]':
        """advance the simulator by 1 time

        Returns:
            reward (float):  -5000 if miss ddl, 1000 if complete
            terminate (bool): true if (either miss ddl / complete)
        """
        reward = self.client.update_processor_and_task()
        self.execution_score += reward

        terminate = False
        if self.client.does_task_miss_deadline():
            reward = 0.0
            terminate = True
        elif self.client.is_simulation_completed():
            reward += 10.0
            terminate = True

        return reward, terminate

    def debug_print(self):
        self.client.print()
