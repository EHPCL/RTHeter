
## Build your Scheduler

### Prepare the environment
To build your own scheduler, you can create a folder under `app/`:
```bash
cd app
mkdir myscheduler
cd myscheduler
touch scheduler.py
```

Configure the python path by:

```python
import sys
sim_path = '../../src/python'
if sim_path not in sys.path:
    sys.path.append(sim_path)
        
from client import SimulatorClient
cli = SimulatorClient("../../build/main")
```

You may also configure the analysis path of the editor to have a better coding experience, e.g. 
```json
{
    "python.analysis.extraPaths": [
        "${workspaceFolder}/src/python/"
    ]
}
```

### Parameter Configuration

Step 1. create the processors

```python
cli.create_processor(0, cpuCount)
cli.create_processor(7, gpuCount)
cli.sort_processors()
```

Step 2. create the tasks

The following codes randomly generate DAG taskset.

```python
from rand import DAGTaskGenerator
gen = DAGTaskGenerator(seed, numTask, uti)
taskset = gen.generate_tasksets()
for task in taskset: cli.create_dag_task(task)
```

Step 3. start simulation

```python
# May change according to your taskset size
cli.set_simulation_timebound(1000)
cli.start_simulation()
```

### Scheduling loop

We recommend you implement a separate function:

```python
def simulate(self) -> bool:
    """ Return true if schedulable
    """

    while ((not cli.is_simulation_completed()) and not cli.does_task_miss_deadline()):
        
        # You may want to query the processor states
        for i in range(self.proc_count):
            proc_state = cli.query_processor_state(i)
            if proc_state[1] >= 2: continue
            scheduleFlag = False
            # Access the task following your priority rule
            for _j in range(self.task_count):
                if scheduleFlag: break
                # Query the task state and segment sate
                task_seg_states = cli.query_task_state(j)[1]
                for k, seg_state in enumerate(task_seg_states):
                    if (seg_state[0]!=proc_state[0] or seg_state[-1]<=0 or seg_state[2]!=1): continue
                    if (seg_state[1]>=0 and seg_state[1] <= 99999): continue
                    # The segment must be same affinity, ready, non-complete
                    if proc_state[1] ==0: scheduleFlag = True
                    else:
                        if prios[proc_state[2]] > prios[j]:
                            # preemption
                            scheduleFlag = True
                    if scheduleFlag:
                        cli.schedule_segment_on_processor(i, j, k)
                        break
        # upgrade to next slice
        cli.update_processor_and_task()

    return not cli.does_task_miss_deadline()
```

### Examples

You can refer to example codes in `app/benchmark/edf.py` and `app/benchmark/ratemonotonic.py`.

## Micro-Architecture Variations

First, you should add the compilation flags in `CMakeLists.txt`:

```cmake
# uncomment the following two lines if you want to simulate the execution variation
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -g")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -DVARI_PROC")
```

Recompile the C++ backend:

```bash
cmake -S . -B build
cd build
make
```

In the python client, the attributes `processorVariation` and `parallelFactor` can be configured by micro-architecture simulation statistics.

```python
for i in range(cpuCount + gpuCount):
    cli.set_processor_variation(i, 2)
    
cli.set_processor_parallel_factor("GPU", 2)
cli.set_processor_parallel_factor("CPU", 0)
```

<div class="admonition">
<p class="admonition-title">Explanation</p>
<p>
<ul>
<li>The first attribute simulates execution time variation caused by microarchitectural uncertainties such as cache misses. When <code>processorVariation</code> is set to <code>v</code>, the actual progress per time unit varies between <code>(100-v)%</code> to <code>100%</code> of the expected value.</li>
<li>The second attribute simulates performance degradation due to resource contention, including memory bandwidth saturation and instruction dispatch limitations. When <code>parallelFactor</code> is set to <code>f</code>, the execution efficiency scales by <code>(100 - p×f)%</code>, where <code>p</code> represents the number of processors computing in parallel concurrently.</li>
</ul>
</p>
</div>


## More Cases


Utilizing RTHeter, we present two application case studies, which facilitate real-time scheduling in modern heterogeneous architectures. These two case studies are difficult or extremely time-consuming without RTHeter.

- **Application 1**: Training reinforcement learning based static scheduling agent for heterogeneous computing platforms with both synthetic and vision transformer (ViT) tasks. 

- **Application 2**: Benchmarking different schedulers and identifying the dominating processors in the heterogeneous architecture with DAG tasks . 


Still confused what can be done with RTHeter? Navigate to the [Case Studies](./rl_synthetic.md)!

