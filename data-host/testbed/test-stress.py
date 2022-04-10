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
server = input(str("\n[Enter] the server you want to target: "))
print("[Alert] Load level set at {0}%, Load time set at {1} \n-> (this should be the total taken time from the tnf test)".format(loadLevel, loadTime))

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