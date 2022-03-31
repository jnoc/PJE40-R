import configparser
import json
from knockknock import discord_sender
import time

#webhook_url = "https://discord.com/api/webhooks/955584973103042600/bVoLZJewwADPVtCWz8b3ZGn1N3m4sIMO7z6RKkYlEU7RDStdDMB7NOQdk3ymCg59MUn-"
#@discord_sender(webhook_url=webhook_url)
config = configparser.ConfigParser()
config.read('config.ini')

def main():
    """ output = "```"
    for i in range(10):
        output += "\nHello x{0}".format(i+1)
    time.sleep(5)
    output+= "```"
    return output # Optional return value """

    #test = str(input("\n[Enter] the time until until node(s) shutoff (Tfd): \n"))
    tnfTimeList = json.loads(config.get('default','tnfList'))
    print(tnfTimeList)
    print(type(tnfTimeList))
    specTime = ((tnfTimeList[0] / 4) / 1000) # avg Tnf / 4 
    print("{} <---- Tnf/4 time".format(specTime))

if __name__ == "__main__":
    main()
