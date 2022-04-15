import configparser
import re
import time
import subprocess as sp

config = configparser.ConfigParser()
config.read('config.ini')
# gets the specific settings from config for this module
loadLevel = config.get('default','loadLevel')
loadTime = config.get('default','loadTime')
processors = config.get('default','stressCores')

print("\n[\033[93m!\033[0m] Load amount: \033[91m{0}%\033[0m, Load time: \033[91m{1}\033[0m, Core amount: \033[91m{2}\033[0m".format(loadLevel, loadTime, processors))
print("-> (Load time will need to be set longer than the FIO testing time)")
# target the specific server that you want
server = input(str("\n[Enter] the server you want to target: "))

def main():
    print("[Alert] Running stress-ng")
    # lanuch stress on remove target server with config vars
    stressNg = "stress-ng -c {2} -l {0} -t {1} --times --syslog".format(loadLevel, loadTime, processors)
    sp.Popen(sshPass(psshCommand(stressNg, server)), shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    print("[Sleep][---] 10s to spawn cpu hogs")
    time.sleep(10)
    print("[Alert] Checking process is running")
    # checks to see if the stress command is running
    pgrepCommand = "pgrep stress-ng"
    run = sp.Popen(sshPass(psshCommand(pgrepCommand, server)), shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    out = run.communicate()[0].decode("utf-8")
    match = re.findall('\[SUCCESS\]', str(out))
    if len(match) != 0:
        print("-> Stress-ng executed on remote system, running for {} time. Ready for FIO testing!".format(loadTime))
    else:
        print("-> Stress-ng did not execute")

# pssh function for pushing values into
def psshCommand(item, server):
    psshCommand = "pssh -i -t 0 -H {0} -A -l root -x '-tt -q -o StrictHostKeyChecking=no -o GSSAPIAuthentication=no' '{1}'".format(server, item)
    return psshCommand

# sshpass function used to wrap psshCommand
def sshPass(item):
    sshPass = "sshpass -f sshpass {}".format(item)
    return sshPass

if __name__ == "__main__":
    main()