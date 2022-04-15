import configparser
import math
import re
import time
import subprocess as sp

config = configparser.ConfigParser()
config.read('config.ini')
sshPass = "sshpass -f sshpass "

def main():
    # gets all the nodes currently offline
    nodesOnline = "pssh -i -h all-nodes.txt -A -l root -x '-tt -q -o StrictHostKeyChecking=no -o GSSAPIAuthentication=no' 'echo online'"
    proc = sp.Popen("{0}{1}".format(sshPass, nodesOnline), stdout=sp.PIPE, shell=True)
    out = proc.communicate()
    array = re.findall('\[FAILURE\]\W(node-\d\d|master-\d\d)', str(out))
    print(array)
    # if the found nodes (offline ones) then we need to turn them back on
    if len(array) != 0:
        for i in range(len(array)):
            var = re.match('master-(\d*)' ,array[i])
            # if master server type then directs here
            if var != None:
                turnOn = array[i]
                matchProj = "proj-man"
            # else we have storage servers so direct here
            else:
                node = int(re.search('-(\d*)' ,array[i]).group(1))
                if node % 2 == 0:
                    node = math.floor(node / 2)
                else:
                    node = math.floor((node + 1) / 2)
                
                if node < 10:
                    node = "0" + str(node)
                turnOn = array[i]
                matchProj = "proj-{}".format(node)
            # virtualbox start in headless mode
            command = "pssh -i -H {1} -A -l vm1 -x '-tt -q -o StrictHostKeyChecking=no -o GSSAPIAuthentication=no' 'VBoxManage startvm {0} --type headless'".format(turnOn, matchProj)
            print("turning on {0} hosted on {1}".format(turnOn, matchProj))
            run = sp.Popen("{0}{1}".format("sshpass -p localhost1 ", command), shell=True, stdout=sp.PIPE)
            # wait till finished
            run.wait()
    else:
        print("-> {} host(s) are offline".format(len(array)))
    # waits 60s by default to let the nodes turn back on or to re check that there are no nodes offline
    print("Sleeping 60 sec for catchup")
    time.sleep(60)
    print("checking hosts online again...")    
    nodesOnline = "pssh -i -h all-nodes.txt -A -l root -x '-tt -q -o StrictHostKeyChecking=no -o GSSAPIAuthentication=no' 'echo online'"
    proc = sp.Popen("{0}{1}".format(sshPass, nodesOnline), stdout=sp.PIPE, shell=True)
    out = proc.communicate()
    array = re.findall('\[FAILURE\]\W(node-\d\d|master-\d\d)', str(out))
    print("{} are offline".format(array))
        
if __name__ == "__main__":
    main()
