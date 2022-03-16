import re
import subprocess as sp 

print('''[!] This must be done within the graphs diectory inside of the DFS-results folder
.
├── 1-node-failure
├── 2-node-failure
├── 3-node-failure
├── fio-bench
│   ├── fio-bench-*-rand-dfs
│   │   ├── randread
│   │   │   └── dfs
│   │   │       └── 4k
│   │   ├── randrw
│   │   │   └── dfs
│   │   │       └── randrw50
│   │   │           └── 4k
│   │   └── randwrite
│   │       └── dfs
│   │           └── 4k
│   └── fio-bench-*-seq-dfs
│       ├── seqread
│       │   └── dfs
│       │       └── 4k
│       ├── seqrw
│       │   └── dfs
│       │       └── readwrite50
│       │           └── 4k
│       └── seqwrite
│           └── dfs
│               └── 4k
└── graphs

Read above!
''')

mountpoint = str(input("[Enter] DFS mountpoint: "))
pathname = re.match('^\/.*\/(.*)$', mountpoint).group(1)
name = str(input("[Enter] result name: "))
typePath = str(input("[Enter] rand/seq name: "))
typeResult = ""

if typePath == "rand":
    typeResult = "random"
    rValue = "rand"
else:
    typeResult = "sequential"
    rValue = ""

# -N, --latency-iops-2d-nj
#                        This graph type is like the latency-iops-2d-qd
#                        barchart but instead of plotting queue depths for a
#                        particular numjobs value, it plots numjobs values for
#                        a particular queue depth.
#
commands = [
"fio-plot -i ../../fio-bench/fio-bench-*-{0}-{1}/{0}read/{1}/4k/ --title '{2} IOPS/Latency per amount of jobs ({3} reads)' -r {4}read -N --disable-fio-version -s 'UP896692'".format(typePath, pathname, name, typeResult, rValue),
"fio-plot -i ../../fio-bench/fio-bench-*-{0}-{1}/{0}write/{1}/4k/ --title '{2} IOPS/Latency per amount of jobs ({3} writes)' -r {4}write -N --disable-fio-version -s 'UP896692'".format(typePath, pathname, name, typeResult, rValue),


#"fio-plot -i ../../fio-bench/fio-bench-*-rand-dfs/seqread/dfs/4k/ --title 'MooseFS IOPS/Latency per amount of jobs (reads)' -r read -N --disable-fio-version -s 'UP896692'",
#"fio-plot -i ../../fio-bench/fio-bench-*-rand-dfs/seqwrite/dfs/4k/ --title 'MooseFS IOPS/Latency per amount of jobs (writes)' -r write -N --disable-fio-version -s 'UP896692'",


#-l, --latency-iops-2d-qd
#                        Generates a 2D barchart of IOPs and latency for all
#                        queue depths given a particular numjobs value.
"fio-plot -i ../../fio-bench/fio-bench-*-{0}-{1}/{0}read/{1}/4k/ --title 'MooseFS IOPS/Latency per amount of queue depths ({3} reads)' -r {4}read -l --disable-fio-version -s 'UP896692'".format(typePath, pathname, name, typeResult, rValue),
"fio-plot -i ../../fio-bench/fio-bench-*-{0}-{1}/{0}write/{1}/4k/ --title 'MooseFS IOPS/Latency per amount of queue depths ({3} writes)' -r {4}write -l --disable-fio-version -s 'UP896692'".format(typePath, pathname, name, typeResult, rValue),
#-L, --iodepth-numjobs-3d
#                        Generates a 3D-chart with iodepth and numjobs on x/y
#                        axis and iops or latency on the z-axis.

"fio-plot -i ../../fio-bench/fio-bench-*-{0}-{1}/{0}read/{1}/4k/ --title 'MooseFS IOPS per users and queue depths ({3} reads)' -r {4}read -L -t iops -f read --disable-fio-version -s 'UP896692'".format(typePath, pathname, name, typeResult, rValue),
"fio-plot -i ../../fio-bench/fio-bench-*-{0}-{1}/{0}write/{1}/4k/ --title 'MooseFS IOPS per users and queue depths ({3} writes)' -r {4}write -L -t iops -f write --disable-fio-version -s 'UP896692'".format(typePath, pathname, name, typeResult, rValue),

"fio-plot -i ../../fio-bench/fio-bench-*-{0}-{1}/{0}read/{1}/4k/ --title 'MooseFS Latency per users and queue depths ({3} reads)' -r {4}read -L -t lat -f read --disable-fio-version -s 'UP896692'".format(typePath, pathname, name, typeResult, rValue),
"fio-plot -i ../../fio-bench/fio-bench-*-{0}-{1}/{0}write/{1}/4k/ --title 'MooseFS Latency per users and queue depths ({3} writes)' -r {4}write -L -t lat -f write --disable-fio-version -s 'UP896692'".format(typePath, pathname, name, typeResult, rValue),


#"fio-plot -i ../../fio-bench/fio-bench-*-{0}-{1}/seqread/{1}/4k/ --title 'MooseFS IOPS per users and queue depths (reads)' -r read -L -t iops -f read --disable-fio-version -s 'UP896692'".format(typePath, pathname, name, typeResult, rValue),
#"fio-plot -i ../../fio-bench/fio-bench-*-{0}-{1}/seqwrite/{1}/4k/ --title 'MooseFS IOPS per users and queue depths (writes)' -r write -L -t iops -f write --disable-fio-version -s 'UP896692'".format(typePath, pathname, name, typeResult, rValue),

#"fio-plot -i ../../fio-bench/fio-bench-*-{0}-{1}/seqread/{1}/4k/ --title 'MooseFS Latency per users and queue depths (reads)' -r read -L -t lat -f read --disable-fio-version -s 'UP896692'".format(typePath, pathname, name, typeResult, rValue),
#"fio-plot -i ../../fio-bench/fio-bench-*-{0}-{1}/seqwrite/{1}/4k/ --title 'MooseFS Latency per users and queue depths (writes)' -r write -L -t lat -f write --disable-fio-version -s 'UP896692'".format(typePath, pathname, name, typeResult, rValue),

# -g, --loggraph        This option generates a 2D graph of the log data
#                        recorded by FIO.

# latency over 60s of number of jobs
"fio-plot -i ../../fio-bench/fio-bench-*-{0}-{1}/{0}read/{1}/4k/ --title 'MooseFS Latency against number of jobs ({3} reads)' -g -r {4}read -f read -t lat -n 1 2 4 8 32 64 --disable-fio-version --enable-markers -s 'UP896692'".format(typePath, pathname, name, typeResult, rValue),
"fio-plot -i ../../fio-bench/fio-bench-*-{0}-{1}/{0}write/{1}/4k/ --title 'MooseFS Latency against number of jobs ({3} writes)' -g -r {4}write -f write -t lat -n 1 2 4 8 32 64 --disable-fio-version --enable-markers -s 'UP896692'".format(typePath, pathname, name, typeResult, rValue),

"fio-plot -i ../../fio-bench/fio-bench-*-{0}-{1}/{0}read/{1}/4k/ --title 'MooseFS Latency against queue depths ({3} reads)' -g -r {4}read -f read -t lat -d 1 2 4 8 32 64 --disable-fio-version --enable-markers -s 'UP896692'".format(typePath, pathname, name, typeResult, rValue),
"fio-plot -i ../../fio-bench/fio-bench-*-{0}-{1}/{0}write/{1}/4k/ --title 'MooseFS Latency against queue depths ({3} writes)' -g -r {4}write -f write -t lat -d 1 2 4 8 32 64 --disable-fio-version --enable-markers -s 'UP896692'".format(typePath, pathname, name, typeResult, rValue)
]

##### Compare command

#fio-plots -i <folder_a> <folder_b> <folder_c> -T 'Test' -C -r randwrite -d 8 
#fio-plots -i --title 'MooseFS vs '


print()
proc = sp.Popen("mkdir {0}".format(typePath), stdout=sp.PIPE, shell=True)
proc.wait()
for i in commands:
    proc = sp.Popen(i, cwd="./{0}".format(typePath), stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
    #out = proc.communicate()
    #print(i)
    #print(out)
    proc.wait()

print("Dirty scripting done")
print("Output in ./{0}".format(typePath))