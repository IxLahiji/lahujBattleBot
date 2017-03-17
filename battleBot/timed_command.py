import discord
import asyncio
import sys
import datetime
import copy
from threading import Lock
from battleBot.list import My_List

class Timed_Command:

    timed_commands = My_List()
    timed_list_mutex = Lock()
    
    def __init__(self):
        pass
    
        
    async def timed_command_chk():
        while True:
            temp_list = timed_commands.get_elements()
            #loop through copy of list
            for command in temp_list:
                if (command.target_date_time is None):
                    timed_commands.remove_from_list(command)
                    continue
                if ((datetime.datetime.now() - command.target_date_time).days >= 0):
                    command.run_command()
                    timed_commands.remove_from_list(command)
            await asyncio.sleep(30)