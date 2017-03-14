#============[Imports]============

import discord
import asyncio
import json
import os.path
import sys
import time


SUCCESS = 0
NO_ARG_ERR = 1
NO_PERM_ERR = 2
NOT_COMMAND = 3
INVALID_ARGUMENTS = 4


#Program path
prog_path = os.path.dirname(os.path.abspath(__file__))
settings_path = prog_path + os.path.sep + 'settings.JSON'

#Create new discord client
client = discord.Client()

#Define the settings
parsed_settings = []

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


#============[Helper Functions]============

async def write_settings(settings):
    settings_file_w = open(settings_path, 'w')
    json.dump(settings, settings_file_w, indent=4, sort_keys=True)
    settings_file_w.close()


#============[Executed at Startup]============

#Generate credential and blacklist JSON files on startup
if not os.path.exists(settings_path):
    print("No settings file found. Generating a new settings JSON file...")
    new_settings_file = open(settings_path, 'w')

    #Defining keys for the JSON file, as well as configuring default values
    default_json = """{"discord_token": ""}
               """
    parsed_json = json.loads(default_json)
    json.dump(parsed_json, new_settings_file, indent=4, sort_keys=True)
    new_settings_file.close()
    
    time.sleep(1)
    print("The settings file has been generated. Please add a token for your discord bot before the next execution.")
    time.sleep(3)
    sys.exit()


#Open JSON credentials file for reading and parse
settings_file = open(settings_path, 'r')
parsed_settings = json.loads(settings_file.read())
settings_file.close()

#Re-writing to fix formatting issues that may be present after the user edits json file
asyncio.ensure_future(write_settings(parsed_settings))


#Check to make sure token is present
if (not parsed_settings['discord_token']):
    print ("Please enter a discord bot token in 'settings.JSON' before running")
    sys.exit()


#on_ready event, typically on login
@client.event
async def on_ready():
    print('Logged in as: ' + client.user.name + '[' + client.user.id + '].')

#============[Run Client]============

#Run client (connect and login) ~ Blocking (must be last) ~ This is an unabstracted version of client.run() to give more control
try:
    client.loop.run_until_complete(client.start(parsed_settings['discord_token']))
    
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
