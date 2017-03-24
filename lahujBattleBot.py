#============[Imports]============

import discord
import asyncio
import os.path
from battleBot.settings import JSONSettings
from battleBot.stats import JSONStats
from battleBot.command import Command
from battleBot.timed_command import Timed_Command


SUCCESS = 0
NO_ARG_ERR = 1
NO_PERM_ERR = 2
NOT_COMMAND = 3
INVALID_ARGUMENTS = 4


prog_path = os.path.dirname(os.path.abspath(__file__))

#Load information
time_commands = Timed_Command()
settings = JSONSettings(prog_path)
stats = JSONStats(prog_path)

#Create new discord client
client = discord.Client()

bot_info = {
"settings":settings,
"stats":stats,
"client":client
}

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


#============[Events]============

#The events that are triggered when a message is sent
@client.event
async def on_message(message):

    if message.content[0] == "!":
        comm = Command(message, bot_info)
        comm_code = comm.run_command()
    else:
        comm_code = NOT_COMMAND

    if (comm_code != SUCCESS) and (comm_code != NOT_COMMAND):
        if comm_code == NO_PERM_ERR:
            print("Command failed ~ User lacks adequate permissions")    
        
        if comm_code == NO_ARG_ERR:
            print("Command failed ~ User did not enter an argument.")
        
        print("_________________________")


#============[Executed at Startup]============

#on_ready event, typically on login
@client.event
async def on_ready():
    print('Logged in as: ' + client.user.name + '[' + client.user.id + '].')


#============[Run Client]============

print("Logging in to bot...")

#Run client (connect and login) ~ Blocking (must be last) ~ This is an unabstracted version of client.run() to give more control
try:
    if (not settings.get_setting('discord_token')):
        print ("Please enter a discord bot token in 'settings.JSON' before running")
        time.sleep(3)
        sys.exit()
    else:
        client.loop.run_until_complete(client.start(settings.get_setting('discord_token')))
    
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
