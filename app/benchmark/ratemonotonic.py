# 
# Copy Right. The EHPCL Authors.
#

class RateMonotonicScheduler:
    
    def __init__(self, seed: int, 
                 taskpattern: str = "dag", numTask: int = 5, uti: float = 3.0,
                 cpuCount: int = 2, datacopy: int = 2, gpuCount :int = 2,
                 releaseLimit = 200) -> None:
        import sys
        sim_path = '../../src/python'
        if sim_path not in sys.path:
            sys.path.append(sim_path)
        
        from client import SimulatorClient
        self.cli = SimulatorClient("../../build/main")
        self.cli.create_processor(0, cpuCount)
        self.cli.create_processor(3, datacopy)
        self.cli.create_processor(7, gpuCount)
        self.cli.sort_processors()
        self.proc_count = cpuCount + datacopy + gpuCount
        self.task_count = numTask
        
        from rand import DAGTaskGenerator, TaskRandomGenerator
        if taskpattern == "dag":
            gen = DAGTaskGenerator(seed, numTask, uti)
            taskset = gen.generate_tasksets()
            for task in taskset: self.cli.create_dag_task(task)
        else: return
        
        import numpy as np
        self.period = np.array([t[0] for t in taskset], dtype=int)
        self.prio = np.argsort(self.period)

        self.cli.set_simulation_timebound(np.min(self.period)*releaseLimit)
        self.limit = np.min(self.period)*releaseLimit
        self.cli.start_simulation()


    def simulate(self) -> bool:
        """ Return true if schedulable
        """
    
        import tqdm
        bar = tqdm.tqdm(total=self.limit, desc="Simulating")
        previousTime = 0
        
        while ((not self.cli.is_simulation_completed()) and not self.cli.does_task_miss_deadline()):
        
            # First round, search for all the idle processors and schedule
            for i in range(self.proc_count):
                proc_state = self.cli.query_processor_state(i)
                if proc_state[1] >= 2: continue
                scheduleFlag = False
                for _j in range(self.task_count):
                    if scheduleFlag: break
                    # access by rate monotonic
                    j = self.prio[_j]
                    task_seg_states = self.cli.query_task_state(j)[1]
                    for k, seg_state in enumerate(task_seg_states):
                        if (seg_state[0]!=proc_state[0] or seg_state[-1]<=0 or seg_state[2]!=1): continue
                        if (seg_state[1]>=0 and seg_state[1] <= 99999): continue
                        # The segment must be same affinity, ready, non-complete
                        if proc_state[1] ==0: scheduleFlag = True
                        else:
                            if self.period[proc_state[2]] > self.period[j]:
                                # preemption
                                scheduleFlag = True
                        if scheduleFlag:
                            self.cli.schedule_segment_on_processor(i, j, k)
                            break
            self.cli.update_processor_and_task()
            bar.update(self.cli.get_current_time_stamp() - previousTime)
            previousTime = self.cli.get_current_time_stamp()
        return not self.cli.does_task_miss_deadline()
    
if __name__ == "__main__":
    
    sche = RateMonotonicScheduler(31412, uti=4.0)
    print(sche.simulate())
