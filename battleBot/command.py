import discord
import asyncio


class Command:

    command_list = {
    }
    
    def __init__(self, message):
        split_command = message.content.split(" ")
        
        self.msg = message
        self.command_id = split_command[0][1:]
        try:
            self.args = split_command[1:]
        except:
            self.args = None
        self.author = message.author
        self.channel = message.channel
        self.serv = message.server
        self.timestamp = message.timestamp
        self.target_date_time = None
        self.message_id = message.id
        self.message_obj = message
        if message.channel.is_private == False:
            self.roles = [role.name for role in self.author.roles]

            
    def get_args(self, numArgs):
        if (self.args is not None) and (len(self.args) == numArgs):
            return self.args[0:numArgs]
    
    
    #Dictionary of functions, allows for modularity in "run_command"
    command_list = {
        
    }
    
    
    def run_command(self):
        #make sure command is a real command and is enabled
        if ((self.command_id in self.command_list) and ((parsed_settings['command_list'])[self.command_id] == "enabled")):
            #check if user has permission to perform command
            if (permission_chk(self.roles, self.command_id)):
                command_function = self.command_list[self.command_id]
                return command_function(self)
            else:
                return NO_PERM_ERR
        else:
            return NOT_COMMAND