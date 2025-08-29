
## Manual Testing

You can interact with the simulator manually:
```bash
cd build
./main int
```

Then the program will prompt `>>>` for user input.


| Type     | Command Name               | Notes           |
| -------- | -------------------------- | --------------- |
| query    | queryCurrentTimeStamp      |                 |
|          | queryProcessorStates       |                 |
|          | queryTaskExecutionStates   |                 |
|          | queryTaskState             |                 |
|          | querySSTaskStates          |                 |
|          | doesTaskMissDeadline       |                 |
| control  | quit                       | kill the client |
|          | startSimulation            | release at 0    |
|          | updateProcessorAndTask     |                 |
|          | setSimulationTimeBound     |                 |
| schedule | createProcessor            |                 |
|          | createHeterSSTask          |                 |
|          | scheduleSegmentOnProcessor |                 |


## Python Client

### Overview

`SimulatorClient` is a Python client class for interacting with a C++ simulation backend through subprocess communication.

### Class Definition

```python
class SimulatorClient(executable_path: str)
```
Python client for interacting with C++ backend simulator.

**Parameters:**
- `executable_path` (str): Path to the C++ executable

**Examples:**
```python
>>> sim = SimulatorClient("path_to_C++_executable")
>>> sim.startSimulation()
```

### Constructor

#### `__init__`
```python
def __init__(executable_path: str)
```
Initializes the simulator client and starts the C++ process.

**Parameters:**
- `executable_path` (str): Path to the C++ executable

### Properties

#### `procMap`
Dictionary mapping processor type codes to processor names:
- `0`: "CPU"
- `3`: "DataCopy" 
- `7`: "GPU"

#### `unit_type`
The data type used by the simulator (`int` or `float`), automatically detected from compilation settings.

### Core Methods

#### `check_unit_type`
```python
def check_unit_type() -> type
```
Detects the unit type (int or float) from the compilation commands.

**Returns:**
- `type`: The detected unit type (`int` or `float`)

#### `send_command`
```python
def send_command(command: str) -> str
```
Sends a command string to the C++ process.

**Parameters:**
- `command` (str): Command to send

**Returns:**
- `str`: Stripped stdout response from the C++ backend

### Simulation Control Methods

#### `restart`
```python
def restart()
```
Restarts the C++ simulation process.

#### `start_simulation`
```python
def start_simulation() -> str
```
Starts the simulation.

**Returns:**
- `str`: Response from backend

#### `quit`
```python
def quit() -> str
```
Quits the simulation and terminates the process.

**Returns:**
- `str`: Response from backend

#### `set_simulation_timebound`
```python
def set_simulation_timebound(bound: int) -> str
```
Sets the simulation time bound.

**Parameters:**
- `bound` (int): Time bound value

**Returns:**
- `str`: Response from backend

#### `is_simulation_completed`
```python
def is_simulation_completed() -> bool
```
Checks if simulation has reached its limit.

**Returns:**
- `bool`: True if simulation completed

#### `does_task_miss_deadline`
```python
def does_task_miss_deadline() -> bool
```
Checks if any task missed its deadline.

**Returns:**
- `bool`: True if any task missed deadline

#### `reset_client`
```python
def reset_client() -> bool
```
Resets the simulator to initial state.

**Returns:**
- `bool`: True if reset successful

### Processor Management Methods

#### `create_processor`
```python
def create_processor(procType: int, procNum: int = 1) -> str
```
Creates processors in the simulator.

**Parameters:**
- `procType` (int): Processor type (0 = CPU, 7 = GPU)
- `procNum` (int, optional): Number of processors to create. Defaults to 1.

**Returns:**
- `str`: Creation status message

#### `sort_processors`
```python
def sort_processors() -> str
```
Sorts the processors.

**Returns:**
- `str`: Response from backend

#### `set_processor_variation`
```python
def set_processor_variation(procId: int, var: int) -> bool
```
Sets processor variation (only available when unit_type is float).

**Parameters:**
- `procId` (int): Processor ID
- `var` (int): Variation value

**Returns:**
- `bool`: True if operation successful

#### `set_processor_parallel_factor`
```python
def set_processor_parallel_factor(procId: int, factor: int) -> str
```
Sets processor parallel factor.

**Parameters:**
- `procId` (int): Processor ID
- `factor` (int): Parallel factor value

**Returns:**
- `str`: Response from backend

### Task Management Methods

#### `create_heter_ss_task`
```python
def create_heter_ss_task(period: int, procCount: int, 
                        proc: tuple[int], segs: tuple[int]) -> str
```
Creates a heterogeneous self-suspension based task.

**Parameters:**
- `period` (int): Task period
- `procCount` (int): Number of different processors involved
- `proc` (tuple[int]): Processor types (e.g., (0, 7) for CPU, GPU)
- `segs` (tuple[int]): Segment specifications

**Returns:**
- `str`: Creation status message

**Examples:**
```python
>>> create_heter_ss_task(5, 2, (0, 7), (1, 1, 1, 1, 1))
```

#### `create_dag_task`
```python
def create_dag_task(args: list) -> str
```
Creates a DAG task.

**Parameters:**
- `args` (list): Task arguments

**Returns:**
- `str`: Creation status message

#### `schedule_segment_on_processor`
```python
def schedule_segment_on_processor(procId: int, taskId: int, segId: int) -> str
```
Schedules a task segment on a specific processor.

**Parameters:**
- `procId` (int): Processor ID
- `taskId` (int): Task ID
- `segId` (int): Segment ID

**Returns:**
- `str`: Response from backend

### Query Methods

#### `get_current_time_stamp`
```python
def get_current_time_stamp() -> int
```
Gets the current simulation timestamp.

**Returns:**
- `int`: Current timestamp

#### `query_processor_state`
```python
def query_processor_state(procId: int) -> tuple
```
Queries the state of a specific processor.

**Parameters:**
- `procId` (int): Processor ID

**Returns:**
- `tuple`: (procType, processorState, taskIndex, segIndex)
  - Note: taskIndex and segIndex are only valid when state is busy

#### `query_processor_states`
```python
def query_processor_states() -> tuple
```
Queries the states of all processors.

**Returns:**
- `tuple`: List of processor state tuples (p1, p2, p3, ...)
  - Each tuple: (procType, processorState, taskIndex, segIndex)

#### `query_task_state`
```python
def query_task_state(taskId: int) -> tuple
```
Queries the state of a specific task.

**Parameters:**
- `taskId` (int): Task ID

**Returns:**
- `tuple`: (period, (segmentStates))
  - Each segmentState: (affinity, currentProcessor, isSegmentReady, length, remainLength)

#### `query_ss_task_state`
```python
def query_ss_task_state(taskId: int) -> tuple
```
Queries the state of a self-suspension based task.

**Parameters:**
- `taskId` (int): Task ID

**Returns:**
- `tuple`: (period, readySegIndex, currentProcessor, remainLength, (SSSegStates))
  - Each SSSegState: (affinity, segmentLength)

#### `query_task_execution_states`
```python
def query_task_execution_states() -> list[int]
```
Queries execution states of all tasks.

**Returns:**
- `list[int]`: List of task execution states

### Utility Methods

#### `update_processor_and_task`
```python
def update_processor_and_task() -> int
```
Updates processor and task states.

**Returns:**
- `int`: Number of executed operations

#### `print`
```python
def print() -> str
```
Prints the current simulator state.

**Returns:**
- `str`: Formatted simulator state

### Destructor

#### `__del__`
```python
def __del__()
```
Automatically quits the simulation when the object is destroyed.

### Internal Methods

*Note: The following methods are internal helpers and should not be called directly:*

- `_create_processor_helper()`
- `_create_heter_ss_task_helper()`
- `_create_dag_task_helper()`
- `_query_processor_state_helper()`
- `_query_processor_states_helper()`
- `_query_task_state_helper()`
- `_set_processor_variation_helper()`
- `update_processor_and_task_helper()`
- `command_decorator()` (decorator for command formatting)

<div class="admonition warning">
<p class="admonition-title">Under Construction</p>
<p>This page is under construction and will be ready later.</p>
</div>
