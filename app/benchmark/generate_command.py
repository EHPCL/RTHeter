# 
# Copy Right. The EHPCL Authors.
#

print("#!/usr/bin/bash")
command = "python ./driver.py -algo rm "
default_args = ["-c 2 ", "-e 2 ", "-g 2 "]

class Counter:
    # only use 120 cpus at most time
    static_var = 0

    @classmethod
    def increment(cls):
        cls.static_var += 1
        return cls.static_var
    
    @classmethod
    def returnEnd(cls):
        if (cls.increment()%108==0):
            return ""
        return "& \\"

for cpu in range(1,6):
    for uti in range(15, 35):
        args = f"-u {uti} "
        for arg in default_args:
            if arg!= "-c 2 ": args += arg
            else: args += f"-c {cpu} "
        args += f"-o c{cpu}e2g2u{uti}.csv "
        
        print(command + args + Counter.returnEnd())
        
for engine in range(1,6):
    if engine ==2 : continue
    for uti in range(15, 35):
        args = f"-u {uti} "
        for arg in default_args:
            if arg!= "-e 2 ": args += arg
            else: args += f"-e {engine} "
        args += f"-o c2e{engine}g2u{uti}.csv "
        
        print(command + args + Counter.returnEnd())
        
for gpu in range(1,6):
    if gpu ==2 : continue
    for uti in range(15, 35):
        args = f"-u {uti} "
        for arg in default_args:
            if arg!= "-g 2 ": args += arg
            else: args += f"-g {gpu} "
        args += f"-o c2e2g{gpu}u{uti}.csv "
        
        print(command + args + Counter.returnEnd())
        
print("echo \"Lanuched successfully!\"")

print("wait")
