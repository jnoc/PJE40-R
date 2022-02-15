## This is to be run fron proj-data (the client and data collection machine)

import os

# commands
shutOffNodes = "pssh -i -h shut_hosts.txt -A -l root -x '-tt' init 0"
telegrafStop = "pssh -i -h all-nodes.txt -A -l root -x '-tt' systemctl stop telegraf"
telegrafStart = "pssh -i -h all-nodes.txt -A -l root -x '-tt' systemctl start telegraf"
nodesOnline = "pssh -i -h all-nodes.txt -A -l root hostname"

# keep track
commands = [shutOffNodes, telegrafStop, telegrafStart, nodesOnline]

# main program start
def main():
    os.system()

# take inputs in via a CLI GUI
def input():
    print()