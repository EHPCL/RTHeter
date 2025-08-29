
## Default Mode (client mode)

As a starting example, we provide one python script simulating the FIFO (first in first out) scheduler. The targeted platform has 2 CPUs and 2 GPUs, and there are 5 parallel tasks. To configure those task and processor settings, please refer to our [api](api.md).


```bash
cd src/python
python ./fifo.py
```

The simulation result will be displayed on the terminal:
```bash
(py38) ➜  python git:(main) ✗ python ./fifo.py 
Current Timestamp: 0
Task 0, period 25, state: ready, prog: 0/21
Task 1, period 40, state: ready, prog: 0/27
Task 2, period 125, state: ready, prog: 0/30
Task 3, period 200, state: ready, prog: 0/32
Task 4, period 1000, state: ready, prog: 0/33
CPU0 State: idle, Task , Segment
CPU1 State: idle, Task , Segment
GPU2 State: idle, Task , Segment
GPU3 State: idle, Task , Segment

Current Timestamp: 1
Task 0, period 25, state: ready, prog: 1/21
Task 1, period 40, state: ready, prog: 1/27
Task 2, period 125, state: ready, prog: 0/30
Task 3, period 200, state: ready, prog: 0/32
Task 4, period 1000, state: ready, prog: 0/33
CPU0 State: busy-preemptive, Task 0, Segment(0): 1/3
CPU1 State: idle, Task , Segment
GPU2 State: idle, Task , Segment
GPU3 State: idle, Task , Segment

Enter to continue...
```


## Manual Testing

You can also interact with the simulator manually:
```bash
(py38) ➜  build git:(main) ✗ ./main int
>>> createProcessor CPU 1
Created successfully
>>> createProcessor GPU 2
Created successfully
>>> printSimulatorState 
Current Timestamp: 0
CPU0 State: idle, Task , Segment
GPU1 State: idle, Task , Segment
GPU2 State: idle, Task , Segment

Simulator Status Printed
>>> 
```

Please refer to our [api](api.md) for more commands.


## Debug Mode

If you want to make extention on the existing C++ codes, you can test your implementation in `debug mode`.

First, you should uncomment the scheduler implementation in `test/main.cpp`.
```cpp
// uncomment to use the DEBUG MODE:
std::cout << "Start Testing...\n";
Scheduler scheduler;
scheduler.initializeSimulation();
bool res = scheduler.startScheduleLoop();
 
std::cout << "Schedule result: " << res << std::endl;

// default CLIENT MODE
// Interface interface(argc, argv);
// interface.readCommands();
```

Then, you can rebuild the project and verify your implementation
```bash
cd build
make 
./main
```

Remember to restore `test/main.cpp` if you want to use RTHeter in a default mannar.

