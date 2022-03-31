import configparser
import json
import math
import re
from knockknock import discord_sender
import time
import subprocess as sp

#webhook_url = "https://discord.com/api/webhooks/955584973103042600/bVoLZJewwADPVtCWz8b3ZGn1N3m4sIMO7z6RKkYlEU7RDStdDMB7NOQdk3ymCg59MUn-"
#@discord_sender(webhook_url=webhook_url)
config = configparser.ConfigParser()
config.read('config.ini')

sshPass = "sshpass -f sshpass "

def main():
    """ output = "```"
    for i in range(10):
        output += "\nHello x{0}".format(i+1)
    time.sleep(5)
    output+= "```"
    return output # Optional return value """

    #test = str(input("\n[Enter] the time until until node(s) shutoff (Tfd): \n"))
    """ tnfTimeList = json.loads(config.get('default','tnfList'))
    print(tnfTimeList)
    print(type(tnfTimeList))
    specTime = ((tnfTimeList[0] / 4) / 1000) # avg Tnf / 4 
    print("{} <---- Tnf/4 time".format(specTime))
 """
    nodesOnline = "pssh -i -h all-nodes.txt -A -l root -x '-tt -q -o StrictHostKeyChecking=no -o GSSAPIAuthentication=no' 'echo online'"
    proc = sp.Popen("{0}{1}".format(sshPass, nodesOnline), stdout=sp.PIPE, shell=True)
    out = proc.communicate()
    array = re.findall('\[FAILURE\]\W(node-\d\d|master-\d\d)', str(out))
    print(array)
    if len(array) != 0:
        for i in range(len(array)):
            var = re.match('master-(\d*)' ,array[i])
            if var != None:
                #master = re.search('-(\d*)', var).group(1)
                print(True)
                turnOn = array[i]
                matchProj = "proj-man"
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
            command = "pssh -i -H {1} -A -l vm1 -x '-tt -q -o StrictHostKeyChecking=no -o GSSAPIAuthentication=no' 'VBoxManage startvm {0} --type headless'".format(turnOn, matchProj)
            print("turning on {0} hosted on {1}".format(turnOn, matchProj))
            run.wait()
    else:
        print("-> {} host(s) are offline".format(len(array)))
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
