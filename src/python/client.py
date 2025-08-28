# 
# Copy Right. The EHPCL Authors.
#

import subprocess

class SimulatorClient:
    """ Python client for interecting with C++ backend

    Examples
    --------
    >>> sim = SimulatorClient("path_to_C++_executable")
    >>> sim.startSimulation()
    """

    def __init__(self, executable_path):
        self.executable = executable_path
        self.procMap = {0: "CPU", 3:"DataCopy", 7: "GPU"}
        self.process = subprocess.Popen(
            [self.executable],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=None,
            text=True
        )
        self.alreadyQuit = False
        self.check_unit_type()
    
    def check_unit_type(self) -> type:
        import os
        directory = os.path.dirname(self.executable)
        compile_command_path = os.path.join(directory, 'compile_commands.json')
        
        import json

        with open(compile_command_path, 'r') as file:
            compile_commands = json.load(file)
        
        for entry in compile_commands:
            if "-DVARI_PROC" in entry["command"]:
                self.unit_type = float
            else:
                self.unit_type = int
                
        return self.unit_type
    
    def __del__(self):
        if (not self.alreadyQuit):
            self.quit()
        
    def restart(self):
        if self.process.poll() is None:
            self.process.kill()
        self.process = subprocess.Popen(
            [self.executable],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=None,
            text=True
        )

    def send_command(self, command: str):
        """send command in str to the C++ process

        Returns:
            str: striped stdout from the C++ backend
        """
        self.process.stdin.write(command + "\n")
        self.process.stdin.flush()
        return self.process.stdout.readline().strip()


    def command_decorator(command_template: str):
        from functools import wraps
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs) -> str:
                command = command_template.format(*args, **kwargs)
                return self.send_command(command)
            return wrapper
        return decorator

    def get_current_time_stamp(self) -> int:
        return int(self.send_command("queryCurrentTimeStamp"))
    
    @command_decorator("quit")
    def quit(self) -> str:
        self.alreadyQuit = True
        pass
    
    @command_decorator("setSimulationTimeBound {}")
    def set_simulation_timebound(self, bound: int) -> str:
        pass

    def is_simulation_completed(self) -> bool:
        """return true is the simulation have reached the limit"""
        return bool(self.send_command("isSimulationCompleted"))
    
    def does_task_miss_deadline(self) -> bool:
        """return true if there's any task miss deadline,
        the agent should stop simulation
        """
        return bool(self.send_command("doesTaskMissDeadline"))
    
    @command_decorator("updateProcessorAndTask")
    def update_processor_and_task_helper(self) -> str:
        pass

    def update_processor_and_task(self) -> int:
        res = self.update_processor_and_task_helper().split()
        executed = int(res[0])
        if executed < 0: 
            # print("Error occured during updating!")
            executed = 0
        return executed

    @command_decorator("sortProcessors")
    def sort_processors(self) -> str:
        pass

    @command_decorator("startSimulation")
    def start_simulation(self) -> str:
        pass

    @command_decorator("createProcessor {} {}")
    def _create_processor_helper(self, procType: str, procNum: int = 1) -> str:
        pass

    def create_processor(self, procType: int, procNum: int = 1) -> str:
        """create processors in the simulator

        Args:
            procType (int): 0 -> CPU, 7 -> GPU
            procNum (int, optional): Defaults to 1.

        Returns:
            str: Created Successfully
        """
        return self._create_processor_helper(self.procMap[procType], procNum)

    @command_decorator("createHeterSSTask {} {} {} {}")
    def _create_heter_ss_task_helper(self, period:int, procCount: int,
                                    procs: str, segs: str) -> str:
        pass

    def create_heter_ss_task(self, period:int, procCount: int,
                             proc: 'tuple[int]', segs: 'tuple[int]') -> str:
        """create a heterogenous self-suspension based task in the simulator

        Args:
            period (int): period of the task
            procCount (int): number of different processor involved
            proc (tuple[int]): e.g. (CPU, GPU) -> (0,7)
            segs (tuple[int]): segments

        Examples:
        >>> (5, 2, (0,7), (1,1,1,1,1))
        """
        return self._create_heter_ss_task_helper(period, procCount,
                                                " ".join([self.procMap[x] for x in proc]) + " ",
                                                " ".join(map(str, segs))+" ")

    @command_decorator("createDAGTask {}")
    def _create_dag_task_helper(self, args:str) -> str:
        pass

    def create_dag_task(self, args: list) -> str:
        return self._create_dag_task_helper(" ".join(map(str, args)) + " ")

    @command_decorator("queryProcessorState {}")
    def _query_processor_state_helper(self, procId: int) -> str:
        pass
    
    def query_processor_state(self, procId: int) -> 'tuple':
        """query the states of the given processor

        Returns:
            processorState: procType, processorState, taskIndex, segIndex \\
            The index of task / segment is only valid when state is busy
        """
        res = self._query_processor_state_helper(procId)
        mapped = tuple(map(int, res.split()))
        return mapped

    @command_decorator("queryProcessorStates")
    def _query_processor_states_helper(self) -> str:
        pass

    def query_processor_states(self) -> 'tuple':
        """query the states of all processors

        Returns:
            tuple: p1, p2, p3, ...
        Notes:
            processorState: procType, processorState, taskIndex, segIndex \\
            The index of task / segment is only valid when state is busy
        """
        res = self._query_processor_states_helper()
        mapped = list(map(int, res.split()))
        result = []
        for i in range(len(mapped)//4):
            temp = (mapped[4*i], mapped[4*i+1], mapped[4*i+2], mapped[4*i+3])
            result.append(temp)
        return tuple(result)

    @command_decorator("queryTaskState {}")
    def _query_task_state_helper(self, taskId: int) -> str:
        pass

    def query_task_state(self, taskId: int) -> 'tuple':
        """query the task state by index

        Returns:
            tuple: (period, (s1, s2, ...))
        Notes:
            segmentState: affinity, currentProcessor, isSegmentReady, length, remainLength
        """
        res = self._query_task_state_helper(taskId)
        mapped = list(map(self.unit_type, res.split()))
        if self.unit_type == float:
            for i in range(3): mapped[i] = int(mapped[i])
        result = []
        for i in range(len(mapped)//5):
            temp = (mapped[5*i+1], mapped[5*i+2], mapped[5*i+3], mapped[5*i+4], mapped[5*i+5])
            result.append(temp)
        return (mapped[0], tuple(result))
    
    def query_ss_task_state(self, taskId: int) -> 'tuple':
        """query the self-suspension based task state by index

        Returns:
            tuple: (period, readySegIndex, currentProcessor, remainLength, (SSSegStates))\\
            SSSegStates: affinity, segmentLength
        """
        mapped = list(map(self.unit_type, self.send_command(f"querySSTaskStates {taskId}").split()))
        if self.unit_type == float:
            for i in range(3): mapped[i] = int(mapped[i])
            for i in range(2, len(mapped)//2): mapped[2*i] = int(mapped[2*i])
        result = []
        for i in range(2, len(mapped)//2):
            temp = (mapped[2*i], mapped[2*i+1])
            result.append(temp)
        return (mapped[0],  mapped[1], -1 if mapped[2]>=999999 else mapped[2], mapped[3], tuple(result))
    
    def query_task_execution_states(self) -> 'list[int]':
        result = list(map(int, self.send_command("queryTaskExecutionStates").split()))
        return result

    @command_decorator("scheduleSegmentOnProcessor {} {} {}")
    def schedule_segment_on_processor(self, procId: int, taskId:int, segId: int) -> str:
        pass

    def reset_client(self) -> bool:
        result = self.send_command("resetSimulator")
        if result.find("Error") != -1: return False
        return True

    @command_decorator("setProcessorVariation {}")
    def _set_processor_variation_helper(self, args: str = {}) -> bool:
        pass

    def set_processor_variation(self, procId: int, var: int) -> bool:
        if self.unit_type == int: return False
        self._set_processor_variation_helper(f" {procId} {var}")
        return True

    @command_decorator("setProcessorParallelFactor {} {}")
    def set_processor_parallel_factor(self, procId: int, factor: int) -> str:
        pass

    def print(self):
        return self.send_command("printSimulatorState")

if __name__ == "__main__":
    simulator = SimulatorClient("../../build/main")
    CPU = 0; GPU = 7
    print(simulator.create_processor(CPU, 2))
    print(simulator.create_processor(GPU, 1))
    print(simulator.set_processor_variation(0,1))
    print(simulator.set_processor_variation(2,1))
    print(simulator.create_heter_ss_task(6,2,(CPU, GPU), (1,1,1,1,1)))
    print(simulator.start_simulation())
    print(simulator.print())
    print(simulator.schedule_segment_on_processor(0,0,0))
    print(simulator.print())
    print(simulator.update_processor_and_task())
    print(simulator.update_processor_and_task())
    print(simulator.update_processor_and_task())
    print(simulator.schedule_segment_on_processor(2, 0, 1))
    print(simulator.query_processor_states())
    print(simulator.query_ss_task_state(0))
    print(simulator.update_processor_and_task())
    print(simulator.print())
    print(simulator.update_processor_and_task())
    print(simulator.print())
    print(simulator.update_processor_and_task())
    print(simulator.does_task_miss_deadline())
    # simulator.quit()
