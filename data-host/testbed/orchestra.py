## This is to be run fron proj-data (the client and data collection machine)
import subprocess

# commands
shutOffNodes = "pssh -i -h shut-hosts.txt -A -l root -x '-tt -q -o StrictHostKeyChecking=no -o GSSAPIAuthentication=no' 'hostname; sleep 1; init 0'"
telegrafStart = "pssh -i -h all-nodes.txt -A -l root -x '-tt -q -o StrictHostKeyChecking=no -o GSSAPIAuthentication=no' systemctl start telegraf"
telegrafStop = "pssh -i -h all-nodes.txt -A -l root -x '-tt -q -o StrictHostKeyChecking=no -o GSSAPIAuthentication=no' systemctl stop telegraf"
nodesOnline = "pssh -i -h all-nodes.txt -A -l root -x '-tt -q -o StrictHostKeyChecking=no -o GSSAPIAuthentication=no' hostname"

# keep track
commands = [shutOffNodes, telegrafStart, telegrafStop, nodesOnline]

# main program start
def main():
    set = ["1", "2", "3", "4", "Q", "q"]
    print("Files in use: shut-hosts.txt, all-nodes.txt")
    print('''
    1 = Shut off nodes (shut_hosts.txt is used here)
    2 = Start telegraf across the cluster
    3 = Stop telegraf across the cluster
    4 = Check the amount of nodes online across the cluster
    5 = Open Grafana in Chrome
    Q = Exit program
    ''')
    while True:
        try:
            option = input("[Enter] an option value: ")
            if str(option) in set:
                if str(option) == "Q" or str(option) == "q":
                    break
                else:
                    handle(option)
            else:
                print("-> Invalid input please retry\n")
        except ValueError:
            print("-> Invalid input please retry\n")

def handle(option):
    proc = subprocess.Popen(commands[(int(option) - 1)], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    print(out)
    #print(err)

if __name__ == "__main__":
    main()