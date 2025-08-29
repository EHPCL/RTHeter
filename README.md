# Welcome to RTHeter's Documentation

Simulation platform for **runtime scheduling on heterogeneous computing architectures**.

- Documentation: [https://EHPCL.github.io/RTHeter](EHPCL.github.io/RTHeter)
- Video: [https://drive.google.com/file/d/1Od-y0OjT-ymzAAj475Tp-lAJj6Q0rcHj/view?usp=share_link](https://drive.google.com/file/d/1Od-y0OjT-ymzAAj475Tp-lAJj6Q0rcHj/view?usp=share_link)


# Installation

You can follow the commands in this section to install RTHeter.

## Code Download 

```bash
git clone https://github.com/EHPCL/RTHeter.git
```

## Build C++ Backend

```bash
cmake -S . -B build
cd build
make
```

## Install Python Dependencies

We recommend setting up a separte `conda` environment for using RTHeter. 

```bash
pip install numpy
pip install networkx
pip install tqdm
pip install py-dagviz
```

Optionally, you may need to install `torch` if you want to use the reinforcement learning features.

# Basic Usage


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


# Citation

If you use *RTHeter* in your work, please cite one of the following references:

```tex
@INPROCEEDINGS{ni2025rtheter,
  author={Ni, Yinchen and Zhu, Jiace and Jin, Yier and Zou, An},
  booktitle={2025 Design, Automation & Test in Europe Conference (DATE)}, 
  title={RTHeter: Simulating Real-Time Scheduling of Multiple Tasks on Heterogeneous Architectures}, 
  year={2025},
  volume={},
  number={},
  pages={1-7},
  doi={10.23919/DATE64628.2025.10992806}}
```

# Contributors

- <a href="https://hamham223.com" target="_blank">Yinchen Ni</a>
- Jiace Zhu
- An Zou (Advisor)

