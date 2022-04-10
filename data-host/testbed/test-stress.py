import configparser
import json
import math
import re
#from knockknock import discord_sender
import time
import subprocess as sp

config = configparser.ConfigParser()
config.read('config.ini')

#mp = config.get('default','mountpoint')


loadLevel = config.get('default','loadLevel')
loadTime = config.get('default','loadTime')
processors = config.get('default','stressCores')

print("\n[\033[93m!\033[0m] Load amount: \033[91m{0}%\033[0m, Load time: \033[91m{1}\033[0m, Core amount: \033[91m{2}\033[0m".format(loadLevel, loadTime, processors))
print("-> (Load time will need to be set longer than the FIO testing time)")
server = input(str("\n[Enter] the server you want to target: "))

def main():
    print("[Alert] Running stress-ng")
    stressNg = "stress-ng -c {2} -l {0} -t {1}".format(loadLevel, loadTime, processors)
    sp.Popen(sshPass(psshCommand(stressNg, server)), shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    print("[Sleep][---] 10s to spawn cpu hogs")
    time.sleep(10)
    print("[Alert] Checking process is running")
    pgrepCommand = "pgrep stress-ng"
    run = sp.Popen(sshPass(psshCommand(pgrepCommand, server)), shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    out = run.communicate()[0].decode("utf-8")
    match = re.findall('\[SUCCESS\]', str(out))
    if len(match) != 0:
        print("-> Stress-ng executed on remote system, running for {} time. Ready for FIO testing!".format(loadTime))
    else:
        print("-> Stress-ng did not execute")

def psshCommand(item, server):
    psshCommand = "pssh -i -H {0} -A -l root -x '-tt -q -o StrictHostKeyChecking=no -o GSSAPIAuthentication=no' '{1}'".format(server, item)
    return psshCommand

def sshPass(item):
    sshPass = "sshpass -f sshpass {}".format(item)
    return sshPass

if __name__ == "__main__":
    main()