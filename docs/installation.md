
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


To verify your installation, navigate to the [basic usage](basic_usage.md) tab.
