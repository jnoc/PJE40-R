## This is to be run fron proj-data (the client and data collection machine)
from asyncio import subprocess
import subprocess as sp 
from datetime import datetime
import re
import alive_progress as ap
from statistics import mean
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

mountpoint = config.get('default','mountpoint')

print("[\033[93mAlert\033[0m] Make sure config.ini is up to-date!")
#mountpoint = str(input("[Enter] DFS mountpoint: "))
pointer = mountpoint

def export():    
    
    mountpoint = config.get('default','mountpoint')
    Tfd = eval(config.get('default','tfd'))
    Tnf = eval(config.get('default','tnf'))
    Tf = eval(config.get('default','tf'))
    
    modeType = [Tfd, Tnf, Tf]
    array = [mountpoint, modeType]

    return array

# commands
sshPass = "sshpass -f sshpass "

shutOffNodes = "pssh -i -h shutoff-hosts.txt -A -l root -x '-tt -q -o StrictHostKeyChecking=no -o GSSAPIAuthentication=no' 'hostname; sleep 1; init 0'"
telegrafStart = "pssh -i -h all-nodes.txt -A -l root -x '-tt -q -o StrictHostKeyChecking=no -o GSSAPIAuthentication=no' 'systemctl start telegraf; sleep 1; systemctl status telegraf | grep Active'"
telegrafStop = "pssh -i -h all-nodes.txt -A -l root -x '-tt -q -o StrictHostKeyChecking=no -o GSSAPIAuthentication=no' 'systemctl stop telegraf; sleep 1; systemctl status telegraf | grep Active'"
nodesOnline = "pssh -i -h all-nodes.txt -A -l root -x '-tt -q -o StrictHostKeyChecking=no -o GSSAPIAuthentication=no' 'echo online'"
pingHosts = "nmap -sn -iL all-nodes.txt"

# fio commands                                                                                              change XXM
# random r/w/rw
fioSetTestRRead = "fio --randrepeat=1 --ioengine=libaio --direct=1 --name=setTest-{0} --filename={0}/test --bs=128k --size=100M --readwrite=randread --ramp_time=4 | tee -a fio-result.txt".format(mountpoint)
fioSetTestRWrite = "fio --randrepeat=1 --ioengine=libaio --direct=1 --name=setTest-{0} --filename={0}/test --bs=128k --size=100M --readwrite=randwrite --ramp_time=4 | tee -a fio-result.txt".format(mountpoint)
fioSetTestRRW = "fio --randrepeat=1 --ioengine=libaio --direct=1 --name=setTest-{0} --filename={0}/test --bs=128k --size=100M --readwrite=randrw --ramp_time=4 | tee -a fio-result.txt".format(mountpoint)
# sequential r/w/rw
fioSetTestRead = "fio --randrepeat=1 --ioengine=libaio --direct=1 --name=setTest-{0} --filename={0}/test --bs=128k --size=100M --readwrite=read --ramp_time=4 | tee -a fio-result.txt".format(mountpoint)
fioSetTestWrite = "fio --randrepeat=1 --ioengine=libaio --direct=1 --name=setTest-{0} --filename={0}/test --bs=128k --size=100M --readwrite=write --ramp_time=4 | tee -a fio-result.txt".format(mountpoint)
fioSetTestRW = "fio --randrepeat=1 --ioengine=libaio --direct=1 --name=setTest-{0} --filename={0}/test --bs=128k --size=100M --readwrite=readwrite --ramp_time=4 | tee -a fio-result.txt".format(mountpoint)

# fio benchmark
# random r/w/rw                                                  change XXM
fioBenchRRead = "bench-fio --target {0} --type directory -b 4k --size 50M --mode randread".format(mountpoint) # --output directory
fioBenchRWrite = "bench-fio --target {0} --type directory -b 4k --size 50M --mode randwrite".format(mountpoint) # --output directory
fioBenchRRW = "bench-fio --target {0} --type directory -b 4k --size 50M --mode randrw --rwmixread 50".format(mountpoint) # --output directory

# sequential r/w/rw
fioBenchRead = "bench-fio --target {0} --type directory -b 4k --size 50M --mode read".format(mountpoint) # --output directory
fioBenchWrite = "bench-fio --target {0} --type directory -b 4k --size 50M --mode write".format(mountpoint) # --output directory
fioBenchRW = "bench-fio --target {0} --type directory -b 4k --size 50M --mode readwrite --rwmixread 50".format(mountpoint) # --output directory

# keep track
commands = [shutOffNodes, telegrafStart, telegrafStop, nodesOnline, nodesOnline, pingHosts]
fioSetRandCommands = [fioSetTestRRead, fioSetTestRWrite, fioSetTestRRW]
fioSetSeqCommands = [fioSetTestRead, fioSetTestWrite, fioSetTestRW]
fioBenchRandCommands = [fioBenchRRead, fioBenchRWrite, fioBenchRRW]
fioBenchSeqCommands = [fioBenchRead, fioBenchWrite, fioBenchRW]

# Array[Array]
fioAllSetCommands = [fioSetRandCommands, fioSetSeqCommands]
fioAllBenchCommands = [fioBenchRandCommands, fioBenchSeqCommands]

# main program start
def main():
    set = ["1", "2", "3", "4", "5", "6", "7", "Q", "q", "S", "s"]
    print("\n[\033[93m!\033[0m] Files in use: shutoff-hosts.txt, all-nodes.txt")
    print("[\033[93m!\033[0m] Mountpoint set to: \033[91m{}\033[0m".format(mountpoint))
    mainMenu()
    while True:
        try:
            option = str(input("\n[Enter] an option value: "))
            if option in set:
                if option == "Q" or option == "q":
                    print()
                    exit()
                elif option == "S" or option == "s":
                    mainMenu()
                elif option == "7":
                    fioScreen()
                else:
                    menuHandle(option)
            else:
                print("-> Invalid input please retry")
        except ValueError as e:
            print("-> Invalid input please retry")
            print(e)

def menuHandle(option):
    proc = sp.Popen("{0}{1}".format(sshPass, commands[(int(option) - 1)]), stdout=sp.PIPE, shell=True)
    out = proc.communicate()
    #print(out)
    if option == "1":
        num_lines = sum(1 for _ in open('shutoff-hosts.txt'))
        match = len(re.findall('closed by remote host', str(out)))
        if match == num_lines:
            print("-> {} host(s) have been shutoff".format(match))
        else:
            print("-> Only {0} host(s) have been shutoff out of {1}, further investigation needed".format(match, num_lines))
    elif option == "2":
        num_lines = sum(1 for _ in open('all-nodes.txt'))
        match = len(re.findall('Active: active', str(out)))
        if match == num_lines:
            print("-> All host(s) had telegraf agent started")
        else:
            print("-> Only {0} host(s) had telegraf agent started out of {1}, further investigation needed".format(match, num_lines))
    elif option == "3":
        num_lines = sum(1 for _ in open('all-nodes.txt'))
        match = len(re.findall('Active: inactive', str(out)))
        if match == num_lines:
            print("-> All host(s) had telegraf agent stopped")
        else:
            print("-> Only {0} host(s) had telegraf agent stopped out of {1}, further investigation needed".format(match, num_lines))
    elif option == "4":
        num_lines = sum(1 for _ in open('all-nodes.txt'))
        match = len(re.findall('online', str(out)))
        if match == num_lines:
            print("-> {} host(s) online".format(match))
        else:
            print("-> Only {0} host(s) online out of {1}, further investigation needed".format(match, num_lines))
    elif option == "5":
        match = re.findall('\[FAILURE\]\W(node-\d\d|master-\d\d)', str(out))
        if len(match) != 0:
            print("-> {} are offline".format(match))
        else:
            print("-> {} host(s) are offline".format(len(match)))
    elif option == "6":
        menuHandle("4")
        match = re.findall('\((\d*.\d*|\d*)s latency\)', str(out))
        match = list(map(float, match))
        print("-> Cluster latency, client <-> cluster \n-> min/avg/max {0:.5f}ms/{1:.5f}ms/{2:.5f}ms".format(min(match), mean(match), max(match)))
    else:
        print("Error")
        exit()


def fioScreen():
    global Tfd, Tnf, Tf
    Tfd = eval(config.get('default','tfd'))
    Tnf = eval(config.get('default','tnf'))
    Tf = eval(config.get('default','tf'))
    set = ["1", "2", "3", "4", "5", "6", "7", "E", "e", "D", "d", "Q", "q", "S", "s"]
    fioMenu()
    while True:
        try:
            option = str(input("\n[Enter] an option value: "))
            if option in set:
                if option == "E" or option == "e":
                    break
                elif option == "Q" or option == "q":
                    print()
                    exit()
                elif option == "S" or option == "s":
                    fioMenu()
                elif option == "D" or option == "d":
                    demo()
                elif option == "7":
                    #new()
                    run = sp.Popen(["python3", "module.py"])
                    run.wait()
                else:
                    fioHandle(option)
            else:
                print("-> Invalid input please retry")
        except ValueError as e:
            print("-> Invalid input please retry")
            #print(e)

def fioHandle(option):
    global Tnf, Tfd, Tf
    ## Set FIO Random r/w/rw commands
    if option == "1":
        fioSetCommandsHandle(fioAllSetCommands, 0)
    ## Set FIO r/w/rw commands
    elif option == "2":
        fioSetCommandsHandle(fioAllSetCommands, 1)
    elif option == "3":
        if Tnf == True:
            Tnf = config.set('default','tnf', "False")
            Tf = config.set('default','tf', "True") # makes sure Tf and Tnf are both not == true
            Tfd = config.set('default','tfd', "False")
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
            print("-> Failure execution (Tf) set")
        else:
            Tnf = config.set('default','tnf', "True")
            Tf = config.set('default','tf', "False")
            Tfd = config.set('default','tfd', "False")
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
            print("-> Normal execution (Tnf) set")
        Tfd = eval(config.get('default','tfd'))
        Tnf = eval(config.get('default','tnf'))
        Tf = eval(config.get('default','tf'))
        print("-> Tnf: {0}, Tf: {1}, Tfd: {2}".format(Tnf, Tf, Tfd))
    elif option == "4":
        if Tfd == False:
            Tfd = config.set('default','tfd', "True")
            Tnf = config.set('default','tnf', "False") # makes sure Tf and Tnf are both not == false
            Tf = config.set('default','tf', "False")
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
            print("-> Failure during (Tfd) set")
        else:
            Tfd = config.set('default','tfd', "False")
            Tnf = config.set('default','tnf', "True")
            Tf = config.set('default','tf', "False")
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
            print("-> Failure during (Tfd) disabled")
        Tfd = eval(config.get('default','tfd'))
        Tnf = eval(config.get('default','tnf'))
        Tf = eval(config.get('default','tf'))
        print("-> Tnf: {0}, Tf: {1}, Tfd: {2}".format(Tnf, Tf, Tfd))
    elif option == "5":
        # Set Bench commands random r/w/rw
        fioBenchHandle(fioAllBenchCommands, 0)
    elif option == "6":
        # Set Bench commands sequential r/w/rw
        fioBenchHandle(fioAllBenchCommands, 1)
    else:
        print("Error")
        exit()




def fioSetCommandsHandle(value, index):
    # gets file 
    var = ["rand", "seq"]
    now = datetime.now()
    name = re.match('^\/.*\/(.*)$', mountpoint).group(1)
    if Tfd == True:
        file = "fio-result-{0}-{1}-{2}-{3}.txt".format(now.strftime("%d-%m-%Y--%H-%M-%S"), var[index], "tfd", name)
    elif Tnf == True:
        file = "fio-result-{0}-{1}-{2}-{3}.txt".format(now.strftime("%d-%m-%Y--%H-%M-%S"), var[index], "tnf", name)
    else:
        file = "fio-result-{0}-{1}-{2}-{3}.txt".format(now.strftime("%d-%m-%Y--%H-%M-%S"), var[index], "tf", name)
    # makes file for results to tee into (built into the set command)
    sp.Popen("touch fio-result.txt", shell=True)
    sp.Popen("echo '{}' | tee -a fio-result.txt".format(file), stdout=sp.PIPE, shell=True)
    if Tfd == True:
            print("-> Using shutoff-hosts.txt to turn off host(s) mid task.")
            print("-> You will be prompted to carry on the program when FIO has finished exectuing and you manually bring the node(s) back online.")
    if Tnf == False:
            print("-> Using shutoff-hosts.txt to turn off host(s) for FIO commands")
            command = "pssh -i -h shutoff-hosts.txt -A -l root -x '-tt -q -o StrictHostKeyChecking=no -o GSSAPIAuthentication=no' 'hostname; sleep 1; init 0'"
            sp.Popen("{0}{1}".format(sshPass,command), shell=True, stdout=sp.PIPE)
            print("-> Shutting off node(s)")
    items = range(len(value[index]))
    with ap.alive_bar(len(items), title="-> FIO Command", bar='classic2', spinner='classic', enrich_print=False) as bar:
        for item in items:
            try:
                if Tfd == True:
                    specTime = str(input("\n[Enter] the time until until node(s) shutoff (Tfd): "))
                    command = "pssh -i -h shutoff-hosts.txt -A -l root -x '-tt -q -o StrictHostKeyChecking=no -o GSSAPIAuthentication=no' 'hostname; sleep {}; init 0'".format(specTime)
                    sp.Popen("{0}{1}".format(sshPass,command), shell=True, stdout=sp.PIPE)
                    #start = time.process_time()
                    print("-> Shutting off node(s)")
                #end = time.process_time()
                target=sp.Popen("echo '\n\n{0}{1}\n\n' | tee -a fio-result.txt".format("Command: ",value[index][item]), stdout=sp.PIPE, shell=True)
                # run set FIO command (iterate through set commands list)
                main = sp.Popen(value[index][item], stdout=sp.PIPE, shell=True)
                # DEBUG (stdout, stderr) = main.communicate()
                exit_code = main.wait()
                #print(end - start)
                # DEBUG print(stderr, exit_code)
                # format results to be readable
                # cleans up the file created from FIO
                cleanup = sp.Popen("rm {}/test".format(mountpoint), stdout=sp.PIPE, shell=True)
                # DEBUG (stdout, stderr) = cleanup.communicate()
                exit_code = cleanup.wait()
                # DEBUG print(stderr, exit_code)
                if Tfd == True and item < (len(value[index]) - 1) :
                    input("[Enter] when ready to continue: ")
                bar()
            except:
                print("\n-> Something went wrong with the command!")
                sp.Popen("rm fio-result.txt", shell=True, stdout=sp.PIPE)
                return
    # moves fio results to the date and time that was started from
    sp.Popen("mv fio-result.txt {}".format(file), shell=True)
    print("-> Results saved to {}".format(file))    

def fioBenchHandle(value, index):
    var = [["randread", "randwrite","randrw"],["seqread","seqwrite","seqrw"]]
    var2 = ["rand", "seq"]
    now = datetime.now()
    name = re.match('^\/.*\/(.*)$', mountpoint).group(1)
    """ for i in range(len(value[index])):
        try:
            print("-> Starting FIO task {}".format(i + 1))
            path = "./fio-bench-{0}/{1}-{2}".format(now.strftime("%d-%m-%Y--%H-%M-%S"), var[index][i], name)
            sp.Popen("{0}{1}{2}{3}".format(value[index][i], " --output ", path, " --dry-run"), shell=True, stdout=sp.PIPE)
        except:
            print("\n-> Something went wrong with the command!")
            return """
    items = range(len(value[index]))
    with ap.alive_bar(len(items), title="-> FIO Benchmarking ", bar='classic2', spinner='classic') as bar:
        for item in items:
            try:
                path = "./fio-bench-{0}-{1}-{2}/{3}".format(now.strftime("%d-%m-%Y--%H-%M-%S"), var2[index], name, var[index][item])
                bench = sp.Popen("{0}{1}{2}".format(value[index][item], " --output ", path), shell=True, stdout=sp.PIPE)
                bench.wait()
                # remove bechfiles for fair test
                cleanup = sp.Popen("rm {}/i*".format(mountpoint), stdout=sp.PIPE, shell=True)
                cleanup.wait()
                bar()
            except:
                print("\n-> Something went wrong with the command!")
                return
    print()            


def demo():
    print("\n[Demo] Running 4k byte block size / 10MB file size FIO sequential read then write workload...\n")
    run = sp.Popen("echo '' > 'fio-result-demo.txt'", shell=True, stdout=sp.PIPE)
    run.wait()
    commands = [
        "fio --randrepeat=1 --ioengine=libaio --direct=1 --name=setTest-{0} --filename={0}/test --bs=4k --size=10M --readwrite=read --ramp_time=4 | tee -a fio-result-demo.txt".format(mountpoint),
        "fio --randrepeat=1 --ioengine=libaio --direct=1 --name=setTest-{0} --filename={0}/test --bs=4k --size=10M --readwrite=write --ramp_time=4 | tee -a fio-result-demo.txt".format(mountpoint)
    ]
    items = range(len(commands))
    with ap.alive_bar(len(items), title="-> FIO Demo ", bar='classic2', spinner='classic') as bar:
        for item in items:
            try:
                target=sp.Popen("echo '\n\n{0}{1}\n\n' | tee -a fio-result-demo.txt".format("Command: ", commands[item]), stdout=sp.PIPE, shell=True)
                target.wait()
                run = sp.Popen("{0}{1}".format(sshPass,commands[item]), shell=True, stdout=sp.PIPE)
                run.wait()
                cleanup = sp.Popen("rm {}/test".format(mountpoint), stdout=sp.PIPE, shell=True)
                cleanup.wait()
                bar()
            except:
                print("\n-> Something went wrong with the command!")
                return
    print("\n[Demo] Printing sample output collected result")
    run = sp.Popen("cat fio-result-demo.txt", shell=True)
    run.wait()
    print()

def mainMenu():
    print('''
    [\033[95mMenu\033[0m]

    1 = Shut off nodes (shutoff-hosts.txt is used here)
    2 = Start telegraf across the cluster
    3 = Stop telegraf across the cluster
    4 = Check the amount of nodes online across the cluster
    5 = Check the amount of nodes offline across the cluster
    6 = Measure average latency of client to cluster
    7 = FIO command submenu

    S = Print this menu
    Q = Exit program
    ''')

def fioMenu():
    print('''
    [\033[93m!\033[0m] Tnf: {0}, Tf: {1}, Tfd: {2}

    [\033[95mFIO Submenu\033[0m]

    1 = Run FIO commands for mixed random r/w/rw
    2 = Run FIO commands for sequential r/w/rw
    3 = Set mode to Tnf or Tf during FIO commands
    4 = Set mode to failure during (Tfd) FIO commands mode
    5 = Run FIO benchmarking for mixed random r/w/rw
    6 = Run FIO benchmarking for sequential r/w/rw
    D = Run FIO showcase demo

    S = Print this submenu
    E = Back to menu
    Q = Exit program
    '''.format(Tnf, Tf, Tfd))

if __name__ == "__main__":
    #new()
    main()