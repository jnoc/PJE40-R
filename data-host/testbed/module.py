import math
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

    num_lines = sum(1 for line in open('shutoff-hosts.txt'))

    global mp, name, Tfd, Tnf, Tf, file, sshPass, tnfTimeList, caughtErrors
    print("Inside module")

    sshPass = "sshpass -f sshpass "
    outputArray = export()
    caughtErrors = []    
    mp = outputArray[0]
    modeType = outputArray[1]
    tnfTimeList = outputArray[2]
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

    print("[Mode] {}".format(file))
    for i in range(12):
        try:
            run = sp.Popen("ls -la {}".format(mp), shell=True, stdout=sp.PIPE)
            out = run.communicate()[0].decode("utf-8")
            match = re.findall('error|Error', str(out))
            # try catch some linux errors 
            if len(match) != 0:
                #print(out)
                out = "```" + out + "```"
                out+= "\n`Mountpoint error, failed on iteration {} of module.py`".format(i+1)
                return out
            run = sp.Popen("df -h".format(mp), shell=True, stdout=sp.PIPE)
            out = run.communicate()[0].decode("utf-8")
            match = re.findall('{}'.format(mp), str(out))
            if len(match) == 0:
                #print(out)
                out = "```" + out + "```"
                out+= "\n`Cluster not mounted, failed on iteration {} of module.py`".format(i+1)
                return out

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
    output+= "\nMountpoint = {0}, Mode = {1}, Failures = {2}, Time = Msec, Output Mode = csv".format(mp, file, num_lines)
    output+= "\ntestType,min,avg,max"
    for i in range(len(commands)):
        results = open("fio-{0}-test-{1}.txt".format(name, commands[i][0]), 'r')
        match = re.findall("-(\d*)msec", results.read(), re.DOTALL)
        if len(match) != 0:
            match = list(map(float, match))
            output += "\n{0},{1},{2:.1f},{3}".format(commands[i][0], min(match), mean(match), max(match))
            print("{0}:\tmin/avg/max {1}msec/{2:.1f}msec/{3}msec".format(commands[i][0], min(match), mean(match), max(match)))
    output += "\nCaught Errors: {}".format(caughtErrors)
    output += "```"
    out = sp.Popen("echo '{0}' > fio-{1}-test-overview-{2}.csv".format(output, name, file), shell=True, stdout=sp.PIPE)
    out.wait()
    # tunr nodes back online at the end of the testing
    turnOnline()
    return output
    #return "\n\t\t`Script finished`"

    
def func(index, commands, mp, name):
    now = datetime.now()
    date = now.strftime("%d-%m-%Y--%H-%M-%S")
    mkfile = sp.Popen("echo 'Started: {2}\n' > fio-{0}-test-{1}.txt".format(name,commands[index][0],date), shell=True, stdout=sp.PIPE)
    mkfile.wait()
    if Tfd == True:
            print("-> Using shutoff-hosts.txt to turn off host(s) mid task.")
            print("-> Nodes will be shut off Tnf/4 time each run and brought back online automatically.")
    if Tf == True:
            print("-> Using shutoff-hosts.txt to turn off host(s) for FIO commands")
            command = "pssh -i -h shutoff-hosts.txt -A -l root -x '-tt -q -o StrictHostKeyChecking=no -o GSSAPIAuthentication=no' 'hostname; sleep 1; init 0'"
            sp.Popen("{0}{1}".format(sshPass,command), shell=True, stdout=sp.PIPE)
            print("-> Shutting off node(s)")
            print("[Sleep][---] 60s to allow cluster catchup...")
            time.sleep(60)
    with ap.alive_bar(3, title="-> FIO {0} tests\t".format(commands[index][0]), bar='classic2', spinner='classic', enrich_print=False, elapsed=False) as tar:
        for j in range(3): # run each test 3 times
            if Tfd == True:
                #print("[Alert] turning off nodes Tnf / 4")
                specTime = ((tnfTimeList[index] / 4) / 1000) # (avg Tnf / 4) / 1000 for seconds
                #print("{} <---- Tnf/4 time".format(specTime))
                #specTime = str(input("\n[Enter] the time until until node(s) shutoff (Tfd):"))
                command = "pssh -i -h shutoff-hosts.txt -A -l root -x '-tt -q -o StrictHostKeyChecking=no -o GSSAPIAuthentication=no' 'hostname; sleep {}; init 0'".format(specTime)
                sp.Popen("{0}{1}".format(sshPass,command), shell=True, stdout=sp.PIPE)
                print("-> Shutting off node(s)")
            fioRun = sp.Popen("{0}".format(commands[index][1]), shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
            out = fioRun.communicate()[1].decode("utf-8")
            print(out)
            ## Endpoint is disconnected mid test or catch other fio error
            match = re.findall('error|error=|endpoint', str(out))
            if len(match) != 0:
                cE = "Iter:{0},Run:{1}".format(commands[index][0],j+1)
                caughtErrors.append(cE)
                mkfile = sp.Popen("echo '{0}, Error: {1}' | tee -a fio-errors.txt".format(cE, match), shell=True, stdout=sp.PIPE)
                mkfile.wait()
            fioRun.wait()
            fileCleanup = sp.Popen("rm {}/test".format(mp), stdout=sp.PIPE, shell=True)
            fileCleanup.wait()
            tar()
            if Tfd == True:
                print("[Alert] FIO iteration done, turning on offline nodes")
                turnOnline()

            print("[Sleep][{}/3] 60s to allow cluster catchup...".format(j+1))
            time.sleep(60)

def turnOnline():
    count = 0
    nodesOnline = "pssh -i -h all-nodes.txt -A -l root -x '-tt -q -o StrictHostKeyChecking=no -o GSSAPIAuthentication=no' 'echo online'"
    proc = sp.Popen("{0}{1}".format(sshPass, nodesOnline), stdout=sp.PIPE, shell=True)
    out = proc.communicate()
    match = re.findall('\[FAILURE\]\W(node-\d\d|master-\d\d)', str(out))
    # pssh bug error catch https://bugzilla.redhat.com/show_bug.cgi?id=1757957
    matchErr = re.findall('Error|error', str(out))
    if len(match) != 0:
        ## catch any nodes that do not turn on... exit module.py if fails
        if count != 0:
            print("[Alert] Some nodes didn't turn back on retrying")
        if count > 2:
            print("[Alert] Some nodes will not restart, further investigation needed...")
            print("-> {} are offline".format(match))
            exit()
        ## list of strings
        for i in range(len(match)):
            var = re.match('master-(\d*)' , match[i])
            if var != None:
                #master = re.search('-(\d*)', var).group(1)
                turnOn = match[i]
                matchProj = "proj-man"
            else:
                node = int(re.search('-(\d*)' , match[i]).group(1))
                if node % 2 == 0:
                    node = math.floor(node / 2)
                else:
                    node = math.floor((node + 1) / 2)
                
                if node < 10:
                    node = "0" + str(node)
                turnOn = match[i]
                matchProj = "proj-{}".format(node)
            command = "pssh -i -H {1} -A -l vm1 -x '-tt -q -o StrictHostKeyChecking=no -o GSSAPIAuthentication=no' 'VBoxManage startvm {0} --type headless'".format(turnOn, matchProj)
            #print("turning on {0} hosted on {1}".format(turnOn, matchProj))
            run.wait()
        #print("[Alert] turned on {} hosts".format(len(match)))
        count+= 1
        print("[Sleep][---] 120s to allow cluster catchup...")
        time.sleep(120)
        turnOnline()
    elif len(matchErr) != 0:
        print("Error caught outside")
        count+= 1
        turnOnline()
    else:
        print("-> Hosts are back online...")


if __name__ == "__main__":
    module()

