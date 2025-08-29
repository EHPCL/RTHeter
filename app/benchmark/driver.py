# 
# Copy Right. The EHPCL Authors.
#

from ratemonotonic import RateMonotonicScheduler
from argparse import ArgumentParser

def parse_args(description):
    parser = ArgumentParser(description=description)
    parser.add_argument("-n", type=int, default=5,
                        choices=(3,4,5,6,7,8,9,10,11,12,13,14),
                        help="The number of tasks")
    parser.add_argument("-c", type=int, default=2,
                        choices=(1,2,3,4,5),
                        help="number of cores")
    parser.add_argument("-e", type=int, default=2,
                        help="number of copy engines",
                        choices=(1,2,3,4,5))
    parser.add_argument("-g", type=int, default=2,
                        help="number of gpus",
                        choices=(1,2,3,4,5))
    parser.add_argument("-o", type=str, default="result.csv",
                        help="output filename")
    parser.add_argument("-run", type=int, default=1000,
                        help="number of runs")
    parser.add_argument("-u", type=int, required=True,
                        help="maximum utilization rate to simulate, ignore min and max")
    parser.add_argument("-l", type=int, default=5,
                        help="load time")
    parser.add_argument("-algo", type=str, required=True,
                        choices=("rm", "edf"),
                        help="Please DO INPUT scheduling algorithm name as prefix")
    
    args = parser.parse_args()
    filename: str = args.algo + "_" + args.o
    return args, filename

args, filename = parse_args("RM Schedule Simulator")

uti: float = args. u / 10.0

from tqdm import tqdm
file = open(filename, 'a+')
file.write(f"scheduling,CPU,DataCopy,GPU,Utilization,Count\n")

count = 0

for run in tqdm(range(args.run), desc=f"c{args.c}e{args.e}g{args.g}u{args.u}"):
    real_seed = (run*324201 + args.u*402631 + 480881*args.c + 976369*args.e + 236513*args.g ) % 8175383
    sche = RateMonotonicScheduler(real_seed, uti=uti,
                                  cpuCount=args.c, datacopy=args.e, gpuCount=args.g)
    success = sche.simulate()
    if success: count = count + 1

file.write(f"RM,{args.c},{args.e},{args.g},{args.u},{count}\n")
file.close()

