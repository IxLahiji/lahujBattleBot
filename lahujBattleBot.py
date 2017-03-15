#============[Imports]============

import discord
import asyncio
import json
import os.path
import sys
import time
from battleBot.settings import JSONSettings
from battleBot.stats import JSONStats


SUCCESS = 0
NO_ARG_ERR = 1
NO_PERM_ERR = 2
NOT_COMMAND = 3
INVALID_ARGUMENTS = 4


prog_path = os.path.dirname(os.path.abspath(__file__))

#Load information
settings = JSONSettings(prog_path)
stats = JSONStats(prog_path)

#Create new discord client
client = discord.Client()


#============[KeyboardInterrupt Handling]============

#Create wakeup task workaround for KeyboardInterrupt handling in Windows
exit_flag = False

#Wakeup function to allow exiting of program in Windows (CTRL+C)
async def wakeup():
    while True:
        await asyncio.sleep(1)
        if(exit_flag):
            break

client.loop.create_task(wakeup())





#============[Executed at Startup]============

#on_ready event, typically on login
@client.event
async def on_ready():
    print('Logged in as: ' + client.user.name + '[' + client.user.id + '].')

#============[Run Client]============

print("Logging in to bot...")

#Run client (connect and login) ~ Blocking (must be last) ~ This is an unabstracted version of client.run() to give more control
try:
    client.loop.run_until_complete(client.start(settings.get_token()))
    
except KeyboardInterrupt:
    #Set exit flag to allow wakeup() to close properly
    exit_flag = True

    client.loop.run_until_complete(client.logout())
    pending = asyncio.Task.all_tasks()
    gathered = asyncio.gather(*pending)
    try:
        gathered.cancel()
        client.loop.run_until_complete(gathered)
        gathered.exception()
    except:
        pass
finally:
    client.loop.close()
