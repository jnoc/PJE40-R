## This is to be run fron proj-data (the client and data collection machine)
import subprocess as sp 
from datetime import datetime

print("[Alert] careful with this input! It needs to be the full path.")
mountpoint = str(input("[Enter] DFS mountpoint: "))

# commands
shutOffNodes = "pssh -i -h shutoff-hosts.txt -A -l root -x '-tt -q -o StrictHostKeyChecking=no -o GSSAPIAuthentication=no' 'hostname; sleep 1; init 0'"
telegrafStart = "pssh -i -h all-nodes.txt -A -l root -x '-tt -q -o StrictHostKeyChecking=no -o GSSAPIAuthentication=no' systemctl start telegraf"
telegrafStop = "pssh -i -h all-nodes.txt -A -l root -x '-tt -q -o StrictHostKeyChecking=no -o GSSAPIAuthentication=no' systemctl stop telegraf"
nodesOnline = "pssh -i -h all-nodes.txt -A -l root -x '-tt -q -o StrictHostKeyChecking=no -o GSSAPIAuthentication=no' hostname"

# fio commands                                                                                              change XXM
fioSetTestRead = "fio --randrepeat=1 --ioengine=libaio --direct=1 --name=setTest-{0} --filename={0}/test --bs=2M --size=100M --readwrite=randread --ramp_time=4 | tee -a fio-result.txt".format(mountpoint)
fioSetTestWrite = "fio --randrepeat=1 --ioengine=libaio --direct=1 --name=setTest-{0} --filename={0}/test --bs=2M --size=100M --readwrite=randwrite --ramp_time=4 | tee -a fio-result.txt".format(mountpoint)
fioSetTestRW = "fio --randrepeat=1 --ioengine=libaio --direct=1 --name=setTest-{0} --filename={0}/test --bs=2M --size=100M --readwrite=randrw --ramp_time=4 | tee -a fio-result.txt".format(mountpoint)

# fio benchmark
fioBenchRead = "bench-fio "
fioBenchWrite = ""
fioBenchRW = ""

# keep track
commands = [shutOffNodes, telegrafStart, telegrafStop, nodesOnline]
fioSetCommands = [fioSetTestRead, fioSetTestWrite, fioSetTestRW]
fioBenchCommands = []


# main program start
def main():
    set = ["1", "2", "3", "4", "5", "Q", "q"]
    print("\n[!] Files in use: shutoff-hosts.txt, all-nodes.txt")
    print("[!] Mountpoint set to: {}".format(mountpoint))
    while True:
        print('''
    [Menu]

    1 = Shut off nodes (shutoff-hosts.txt is used here)
    2 = Start telegraf across the cluster
    3 = Stop telegraf across the cluster
    4 = Check the amount of nodes online across the cluster
    5 = FIO command submenu

    Q = Exit program
    ''')
        try:
            option = str(input("[Enter] an option value: "))
            if option in set:
                if option == "Q" or option == "q":
                    print()
                    exit()
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
    set = ["1", "2", "E", "e", "Q", "q"]
    print('''
    [FIO Submenu]

    1 = Run FIO commands for fault tolerance testing
    2 = Run FIO benchmarking commands

    E = Back to menu
    Q = Exit program
    ''')
    while True:
        try:
            option = str(input("[Enter] an option value: "))
            if option in set:
                if option == "E" or option == "e":
                    break
                elif option == "Q" or option == "q":
                    print()
                    exit()
                else:
                    fioHandle(int(option))
            else:
                print("-> Invalid input please retry\n")
        except ValueError:
            print("-> Invalid input please retry\n")

def fioHandle(option):
    if str(option) == "1":
        # gets file 
        now = datetime.now()
        file = "fio-result-{}.txt".format(now.strftime("%d-%m-%Y--%H-%M-%S"))
        # makes file for results to tee into (built into the set command)
        sp.Popen("touch fio-result.txt", shell=True)
        sp.Popen("echo '{}\n\n\n' | tee -a fio-result.txt".format(file), stdout=sp.PIPE, shell=True)
        for i in range(len(fioSetCommands)):
            try:
                # run set FIO command (iterate through set commands list)
                main = sp.Popen(fioSetCommands[i], stdout=sp.PIPE, shell=True)
                # DEBUG (stdout, stderr) = main.communicate()
                exit_code = main.wait()
                # DEBUG print(stderr, exit_code)
                # format results to be readable
                sp.Popen("echo '\n\n\n' | tee -a fio-result.txt", stdout=sp.PIPE, shell=True)
                # cleans up the file created from FIO
                cleanup = sp.Popen("rm {}/test".format(mountpoint), stdout=sp.PIPE, shell=True)
                # DEBUG (stdout, stderr) = cleanup.communicate()
                exit_code = cleanup.wait()
                # DEBUG print(stderr, exit_code)
            except:
                print("-> Something went wrong with the command!")
                exit()
        # moves fio results to the date and time that was started from
        sp.Popen("mv fio-result.txt {}".format(file), shell=True)
        print("-> Results saved to {}\n".format(file))
    elif str(option) == "2":
        print("Elif")
    else:
        print("Else")

if __name__ == "__main__":
    main()