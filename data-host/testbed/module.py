import subprocess as sp 
import time
import alive_progress as ap
import re
from statistics import mean
from knockknock import discord_sender
from datetime import datetime

from orchestra import export

webhook_url = "https://discord.com/api/webhooks/955584973103042600/bVoLZJewwADPVtCWz8b3ZGn1N3m4sIMO7z6RKkYlEU7RDStdDMB7NOQdk3ymCg59MUn-"

@discord_sender(webhook_url=webhook_url)


def module():
    global mp, name, Tfd, Tnf, Tf, file, sshPass
    print("Inside module")

    sshPass = "sshpass -f sshpass "
    outputArray = export()
        
    mp = outputArray[0]
    modeType = outputArray[1]
    name = re.match('^\/.*\/(.*)$', mp).group(1)
    Tfd = modeType[0]
    Tnf = modeType[1]
    Tf = modeType[2]

    if Tfd == True:
        file = "tfd"
    elif Tnf == True:
        file = "tnf"
    else:
        file = "tf"


    for i in range(12):
        try:
            print("Mode == " + file)
            # random and sequential                                                                                                                 ### need to change back to 100M for LOW
            lowRR =  ["low-rand-read-{0}".format(file), "fio --randrepeat=1 --ioengine=libaio --direct=1 --name=low-rand-read-{0} --filename={0}/test --bs=128k --size=100M --readwrite=randread --ramp_time=4 | tee -a fio-{2}-test-low-rand-read-{1}.txt".format(mp, file, name)]
            lowRW = ["low-rand-write-{0}".format(file), "fio --randrepeat=1 --ioengine=libaio --direct=1 --name=low-rand-write-{0} --filename={0}/test --bs=128k --size=100M --readwrite=randwrite --ramp_time=4 | tee -a fio-{2}-test-low-rand-write-{1}.txt".format(mp, file, name)]
            lowRRW = ["low-rand-rw-{0}".format(file), "fio --randrepeat=1 --ioengine=libaio --direct=1 --name=low-rand-rw-{0} --filename={0}/test --bs=128k --size=100M --readwrite=randrw --ramp_time=4 | tee -a fio-{2}-test-low-rand-rw-{1}.txt".format(mp, file, name)]

            lowSR = ["low-seq-read-{0}".format(file), "fio --randrepeat=1 --ioengine=libaio --direct=1 --name=low-seq-read-{0} --filename={0}/test --bs=128k --size=100M --readwrite=read --ramp_time=4 | tee -a fio-{2}-test-low-seq-read-{1}.txt".format(mp, file, name)]
            lowSW = ["low-seq-write-{0}".format(file), "fio --randrepeat=1 --ioengine=libaio --direct=1 --name=low-seq-write-{0} --filename={0}/test --bs=128k --size=100M --readwrite=write --ramp_time=4 | tee -a fio-{2}-test-low-seq-write-{1}.txt".format(mp, file, name)]
            lowSRW = ["low-seq-rw-{0}".format(file), "fio --randrepeat=1 --ioengine=libaio --direct=1 --name=low-seq-rw-{0} --filename={0}/test --bs=128k --size=100M --readwrite=rw --ramp_time=4 | tee -a fio-{2}-test-low-seq-rw-{1}.txt".format(mp, file, name)]

            ### Added if needed!
            highRR = ["high-rand-read-{0}".format(file), "fio --randrepeat=1 --ioengine=libaio --direct=1 --name=high-rand-read-{0} --filename={0}/test --bs=128k --size=10M --readwrite=randread --ramp_time=4 --numjobs=10 | tee -a fio-{2}-test-high-rand-read-{1}.txt".format(mp, file, name)]
            highRW = ["high-rand-write-{0}".format(file), "fio --randrepeat=1 --ioengine=libaio --direct=1 --name=high-rand-write-{0} --filename={0}/test --bs=128k --size=10M --readwrite=randwrite --ramp_time=4 --numjobs=10 | tee -a fio-{2}-test-high-rand-write-{1}.txt".format(mp, file, name)]
            highRRW = ["high-rand-rw-{0}".format(file), "fio --randrepeat=1 --ioengine=libaio --direct=1 --name=high-rand-rw-{0} --filename={0}/test --bs=128k --size=10M --readwrite=randrw --ramp_time=4 --numjobs=10 | tee -a fio-{2}-test-high-rand-rw-{1}.txt".format(mp, file, name)]

            highSR = ["high-seq-read-{0}".format(file), "fio --randrepeat=1 --ioengine=libaio --direct=1 --name=high-seq-read-{0} --filename={0}/test --bs=128k --size=10M --readwrite=read --ramp_time=4 --numjobs=10 | tee -a fio-{2}-test-high-seq-read-{1}.txt".format(mp, file, name)]
            highSW = ["high-seq-write-{0}".format(file), "fio --randrepeat=1 --ioengine=libaio --direct=1 --name=high-seq-write-{0} --filename={0}/test --bs=128k --size=10M --readwrite=write --ramp_time=4 --numjobs=10 | tee -a fio-{2}-test-high-seq-write-{1}.txt".format(mp, file, name)]
            highSRW = ["high-seq-rw-{0}".format(file), "fio --randrepeat=1 --ioengine=libaio --direct=1 --name=high-seq-rw-{0} --filename={0}/test --bs=128k --size=10M --readwrite=rw --ramp_time=4 --numjobs=10 | tee -a fio-{2}-test-high-seq-rw-{1}.txt".format(mp, file, name)]

            #allLow = [lowRW, lowRR, lowRRW, lowSW, lowSR, lowSRW]
            # rand write, then rand read and finally rand readwrite
            commands = [lowRW, lowRR, lowRRW, lowSW, lowSR, lowSRW, highRW, highRR, highRRW, highSR, highSW, highSRW]
            print("\n[Start] {}".format(commands[i][0]))
            func(i, commands, mp, name)
        except Exception as e:
            print(e)
            print("\n-> Something went wrong with the command!")
            return "\n\t\t`Something went wrong with the command!`"
    print()
    output = "```"
    output+= "\nMountpoint = {0}, Mode = {1}, Time = Msec, Output Mode = csv".format(mp, file)
    output+= "\ntestType,min,avg,max"
    for i in range(len(commands)):
        results = open("fio-{0}-test-{1}.txt".format(name, commands[i][0]), 'r')
        match = re.findall("-(\d*)msec", results.read(), re.DOTALL)
        match = list(map(float, match))
        output += "\n{0},{1},{2:.1f},{3}".format(commands[i][0], min(match), mean(match), max(match))
        print("{0}:\tmin/avg/max {1}msec/{2:.1f}msec/{3}msec".format(commands[i][0], min(match), mean(match), max(match)))
    output += "```"
    out = sp.Popen("echo '{0}' > fio-{1}-test-overview-{2}.csv".format(output, name, file), shell=True, stdout=sp.PIPE)
    out.wait()
    return output
    #return "\n\t\t`Script finished`"

    
def func(index, commands, mp, name):
    now = datetime.now()
    date = now.strftime("%d-%m-%Y--%H-%M-%S")
    mkfile = sp.Popen("echo 'Started: {2}\n' > fio-{0}-test-{1}.txt".format(name,commands[index][0],date), shell=True, stdout=sp.PIPE)
    mkfile.wait()
    if Tfd == True:
            print("-> Using shutoff-hosts.txt to turn off host(s) mid task.")
            print("-> You will be prompted to carry on the program when FIO has finished exectuing and you manually bring the node(s) back online.")
    if Tf == True:
            print("-> Using shutoff-hosts.txt to turn off host(s) for FIO commands")
            command = "pssh -i -h shutoff-hosts.txt -A -l root -x '-tt -q -o StrictHostKeyChecking=no -o GSSAPIAuthentication=no' 'hostname; sleep 1; init 0'"
            sp.Popen("{0}{1}".format(sshPass,command), shell=True, stdout=sp.PIPE)
            print("-> Shutting off node(s)")
            print("[Sleep] 60s to allow cluster catchup...")
            time.sleep(60)
    with ap.alive_bar(3, title="-> FIO {0} tests\t".format(commands[index][0]), bar='classic2', spinner='classic', enrich_print=False, elapsed=False) as tar:
        for j in range(3): # run each test 3 times
            if Tfd == True:
                    specTime = str(input("\n[Enter] the time until until node(s) shutoff (Tfd):"))
                    command = "pssh -i -h shutoff-hosts.txt -A -l root -x '-tt -q -o StrictHostKeyChecking=no -o GSSAPIAuthentication=no' 'hostname; sleep {}; init 0'".format(specTime)
                    sp.Popen("{0}{1}".format(sshPass,command), shell=True, stdout=sp.PIPE)
                    print("-> Shutting off node(s)")
            fioRun = sp.Popen("{0}".format(commands[index][1]), shell=True, stdout=sp.PIPE)
            fioRun.wait()
            fileCleanup = sp.Popen("rm {}/test".format(mp), stdout=sp.PIPE, shell=True)
            fileCleanup.wait()
            tar()
            print("[Sleep][{}/3] 60s to allow cluster catchup...".format(j+1))
            time.sleep(60)

if __name__ == "__main__":
    module()