import discord
import asyncio


class Command:

    command_list = {
    }
    
    def __init__(self, message, stats):
        split_command = message.content.split(" ")
        self.message_obj = message
        self.command_id = split_command[0][1:]
        try:
            self.args = split_command[1:]
        except:
            self.args = None
        self.author = message.author
        self.timestamp = message.timestamp
        self.target_date_time = None
        self.curr_stats = stats
        if (message.channel.is_private == False):
            self.roles = [role.name for role in self.author.roles]
    
    
    def get_args(self, numArgs):
        if (self.args is not None) and (len(self.args) == numArgs):
            return self.args[0:numArgs]
    
    
    @staticmethod
    async def pm_player(player, message):
        await client.send_message(player, message)
    
    
    def register_user(self):
        if (not self.curr_stats.has_stats(self.author)):
            self.curr_stats.generate_player_stats(self.author)
        else:
            print("User is already registered!")
    
    
    def get_stats(self):
        if (self.curr_stats.has_stats(self.author)):
            asyncio.ensure_future(self.pm_player(self.author, self.curr_stats.get_player_stats(self.author)))
        else:
            print("User not registered!")
    
    
    #Dictionary of functions, allows for modularity in "run_command"
    command_list = {
        "register" : register_user,
        "stats" : get_stats
    }
    
    
    def run_command(self):
        #make sure command is a real command and is enabled
        if (self.command_id in self.command_list):
            print("Command issued: " + self.command_id)
            command_function = self.command_list[self.command_id]
            return command_function(self)
        else:
            return NOT_COMMAND