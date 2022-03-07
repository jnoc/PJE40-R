## This is to be run fron proj-data (the client and data collection machine)
import time
import subprocess as sp 
from datetime import datetime
import threading
import re
import alive_progress as ap

print("[\033[93mAlert\033[0m] careful with this input! It needs to be the full path.")
mountpoint = str(input("[Enter] DFS mountpoint: "))
Tfd = False
Tnf = True
Tf = False

# commands
sshPass = "sshpass -f sshpass "

shutOffNodes = "pssh -i -h shutoff-hosts.txt -A -l root -x '-tt -q -o StrictHostKeyChecking=no -o GSSAPIAuthentication=no' 'hostname; sleep 1; init 0'"
telegrafStart = "pssh -i -h all-nodes.txt -A -l root -x '-tt -q -o StrictHostKeyChecking=no -o GSSAPIAuthentication=no' systemctl start telegraf"
telegrafStop = "pssh -i -h all-nodes.txt -A -l root -x '-tt -q -o StrictHostKeyChecking=no -o GSSAPIAuthentication=no' systemctl stop telegraf"
nodesOnline = "pssh -i -h all-nodes.txt -A -l root -x '-tt -q -o StrictHostKeyChecking=no -o GSSAPIAuthentication=no' hostname"

# fio commands                                                                                              change XXM
# random r/w/rw
fioSetTestRRead = "fio --randrepeat=1 --ioengine=libaio --direct=1 --name=setTest-{0} --filename={0}/test --bs=2M --size=100M --readwrite=randread --ramp_time=4 | tee -a fio-result.txt".format(mountpoint)
fioSetTestRWrite = "fio --randrepeat=1 --ioengine=libaio --direct=1 --name=setTest-{0} --filename={0}/test --bs=2M --size=100M --readwrite=randwrite --ramp_time=4 | tee -a fio-result.txt".format(mountpoint)
fioSetTestRRW = "fio --randrepeat=1 --ioengine=libaio --direct=1 --name=setTest-{0} --filename={0}/test --bs=2M --size=100M --readwrite=randrw --ramp_time=4 | tee -a fio-result.txt".format(mountpoint)
# sequential r/w/rw
fioSetTestRead = "fio --randrepeat=1 --ioengine=libaio --direct=1 --name=setTest-{0} --filename={0}/test --bs=2M --size=100M --readwrite=read --ramp_time=4 | tee -a fio-result.txt".format(mountpoint)
fioSetTestWrite = "fio --randrepeat=1 --ioengine=libaio --direct=1 --name=setTest-{0} --filename={0}/test --bs=2M --size=100M --readwrite=write --ramp_time=4 | tee -a fio-result.txt".format(mountpoint)
fioSetTestRW = "fio --randrepeat=1 --ioengine=libaio --direct=1 --name=setTest-{0} --filename={0}/test --bs=2M --size=100M --readwrite=readwrite --ramp_time=4 | tee -a fio-result.txt".format(mountpoint)

# fio benchmark
# random r/w/rw                                                  change XXM
fioBenchRRead = "bench-fio --target /mnt/mfs --type directory -b 2M --size 4M --mode randread" # --output directory
fioBenchRWrite = "bench-fio --target /mnt/mfs --type directory -b 2M --size 4M --mode randwrite" # --output directory
fioBenchRRW = "bench-fio --target /mnt/mfs --type directory -b 2M --size 4M --mode randrw --rwmixread 50" # --output directory

# sequential r/w/rw
fioBenchRead = "bench-fio --target /mnt/mfs --type directory -b 2M --size 4M --mode read" # --output directory
fioBenchWrite = "bench-fio --target /mnt/mfs --type directory -b 2M --size 4M --mode write" # --output directory
fioBenchRW = "bench-fio --target /mnt/mfs --type directory -b 2M --size 4M --mode readwrite --rwmixread 50" # --output directory


# keep track
commands = [shutOffNodes, telegrafStart, telegrafStop, nodesOnline]
fioSetRandCommands = [fioSetTestRRead, fioSetTestRWrite, fioSetTestRRW]
fioSetSeqCommands = [fioSetTestRead, fioSetTestWrite, fioSetTestRW]
fioBenchRandCommands = [fioBenchRRead, fioBenchRWrite, fioBenchRRW]
fioBenchSeqCommands = [fioBenchRead, fioBenchWrite, fioBenchRW]

# Array[Array]
fioAllSetCommands = [fioSetRandCommands, fioSetSeqCommands]
fioAllBenchCommands = [fioBenchRandCommands, fioBenchSeqCommands]

# main program start
def main():
    set = ["1", "2", "3", "4", "5", "Q", "q", "S", "s"]
    print("\n[\033[93m!\033[0m] Files in use: shutoff-hosts.txt, all-nodes.txt")
    print("[\033[93m!\033[0m] Mountpoint set to: \033[91m{}\033[0m".format(mountpoint))
    mainMenu()
    while True:
        try:
            option = str(input("[Enter] an option value: "))
            if option in set:
                if option == "Q" or option == "q":
                    print()
                    exit()
                elif option == "S" or option == "s":
                    mainMenu()
                elif option == "5":
                    fioScreen()
                else:
                    menuHandle(int(option))
            else:
                print("-> Invalid input please retry\n")
        except ValueError:
            print("-> Invalid input please retry\n")

def menuHandle(option):
    proc = sp.Popen(commands[(option - 1)], stdout=sp.PIPE, shell=True)
    out = proc.communicate()
    print(out)

    #print(err)

def fioScreen():
    set = ["1", "2", "3", "4", "5", "6", "E", "e", "Q", "q", "S", "s"]
    fioMenu()
    while True:
        try:
            option = str(input("[Enter] an option value: "))
            if option in set:
                if option == "E" or option == "e":
                    break
                elif option == "Q" or option == "q":
                    print()
                    exit()
                elif option == "S" or option == "s":
                    fioMenu()
                else:
                    fioHandle(option)
            else:
                print("-> Invalid input please retry\n")
        except ValueError as e:
            print("-> Invalid input please retry\n")
            print(e)

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
            Tnf = False
            Tf = True # makes sure Tf and Tnf are both not == true
            Tfd = False
            print("-> Failure execution (Tf) set")
        else:
            Tnf = True
            Tf = False
            Tfd = False
            print("-> Normal execution (Tnf) set")
        print("-> Tnf: {0}, Tf: {1}, Tfd: {2}\n".format(Tnf, Tf, Tfd))
    elif option == "4":
        if Tfd == False:
            Tfd = True
            Tnf = False # makes sure Tf and Tnf are both not == false
            Tf = False
            print("-> Failure during (Tfd) Enabled")
        else:
            Tfd = False
            Tnf = True
            Tf = False
            print("-> Failure during (Tfd) Disabled")
        print("-> Tnf: {0}, Tf: {1}, Tfd: {2}\n".format(Tnf, Tf, Tfd))
    elif option == "5":
        # Set Bench commands random r/w/rw
        fioBenchHandle(fioAllBenchCommands, 0)
    elif option == "6":
        # Set Bench commands sequential r/w/rw
        fioBenchHandle(fioAllBenchCommands, 1)
    else:
        print("Else")

def fioSetCommandsHandle(value, index):
    # gets file 
    var = ["rand", "seq"]
    now = datetime.now()
    if Tfd == True:
        file = "fio-result-{0}-{1}-{2}.txt".format(now.strftime("%d-%m-%Y--%H-%M-%S"), var[index], "tfd")
    elif Tnf == True:
        file = "fio-result-{0}-{1}-{2}.txt".format(now.strftime("%d-%m-%Y--%H-%M-%S"), var[index], "tnf")
    else:
        file = "fio-result-{0}-{1}-{2}.txt".format(now.strftime("%d-%m-%Y--%H-%M-%S"), var[index], "tf")
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
    """ for i in range(len(value[index])):
        try:
            if Tfd == True:
                specTime = str(input("\n[Enter] the time until until node(s) shutoff (Tfd): "))
                command = "pssh -i -h shutoff-hosts.txt -A -l root -x '-tt -q -o StrictHostKeyChecking=no -o GSSAPIAuthentication=no' 'hostname; sleep {}; init 0'".format(specTime)
                sp.Popen("{0}{1}".format(sshPass,command), shell=True, stdout=sp.PIPE)
                #start = time.process_time()
                print("-> Shutting off node(s)")
            print("-> Starting FIO task {}".format(i + 1))
            #end = time.process_time()
            target=sp.Popen("echo '\n\n{0}{1}\n\n' | tee -a fio-result.txt".format("Command: ",value[index][i]), stdout=sp.PIPE, shell=True)
            # run set FIO command (iterate through set commands list)
            main = sp.Popen(value[index][i], stdout=sp.PIPE, shell=True)
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
            if Tfd == True and i < (len(value[index]) - 1) :
                input("[Enter] when ready to continue: ")
        except:
            print("\n-> Something went wrong with the command!")
            sp.Popen("rm fio-result.txt", shell=True, stdout=sp.PIPE)
            return """
    items = range(len(value[index]))
    print()
    with ap.alive_bar(len(items), title="FIO Command", bar='classic2', spinner='classic', enrich_print=False) as bar:
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
    print("-> Results saved to {}\n".format(file))    

def fioBenchHandle(value, index):
    var = [["randread", "randwrite","randrw"],["seqread","seqwrite","seqrw"]]
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
    with ap.alive_bar(len(items), title="FIO Benchmarking ", bar='classic2', spinner='classic') as bar:
        for item in items:
            try:
                path = "./fio-bench-{0}/{1}-{2}".format(now.strftime("%d-%m-%Y--%H-%M-%S"), var[index][item], name)
                sp.Popen("{0}{1}{2}{3}".format(value[index][item], " --output ", path, " --dry-run"), shell=True, stdout=sp.PIPE)
                bar()
            except:
                print("\n-> Something went wrong with the command!")
                return
    print()
                

def mainMenu():
    print('''
    [\033[95mMenu\033[0m]

    1 = Shut off nodes (shutoff-hosts.txt is used here)
    2 = Start telegraf across the cluster
    3 = Stop telegraf across the cluster
    4 = Check the amount of nodes online across the cluster
    5 = FIO command submenu

    S = Print this menu
    Q = Exit program
    ''')

def fioMenu():
    print('''
    \n[\033[93m!\033[0m] Tnf: {0}, Tf: {1}, Tfd: {2}

    [\033[95mFIO Submenu\033[0m]

    1 = Run FIO commands for mixed random r/w/rw
    2 = Run FIO commands for sequential r/w/rw
    3 = Set mode to Tnf or Tf during FIO commands
    4 = Set mode to failure during (Tfd) FIO commands mode
    5 = Run FIO benchmarking for mixed random r/w/rw
    6 = Run FIO benchmarking for sequential r/w/rw

    S = Print this submenu
    E = Back to menu
    Q = Exit program
    '''.format(Tnf, Tf, Tfd))

if __name__ == "__main__":
    main()