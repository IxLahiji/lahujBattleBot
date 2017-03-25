import discord
import asyncio
from battleBot.return_codes import *

class Command:

    command_list = {
    }
    
    def __init__(self, message, bot_info):
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
        self.bot_info = bot_info
        self.curr_stats = bot_info['stats']
        if (message.channel.is_private == False):
            self.roles = [role.name for role in self.author.roles]
    
    
    def get_args(self, numArgs):
        if (self.args is not None) and (len(self.args) == numArgs):
            return self.args[0:numArgs]
    
    
    async def pm_player(self, player, message):
        await self.bot_info['client'].send_message(player, message)
    
    
    def register_user(self):
        if (not self.curr_stats.has_stats(self.author)):
            self.curr_stats.generate_player_stats(self.author)
        else:
            print("User is already registered!")
    
    
    def get_stats(self):
        if (self.curr_stats.has_stats(self.author)):
            formatted_string = "```" + self.stats_to_string(self.curr_stats.get_player_stats(self.author)) + "```"
            asyncio.ensure_future(self.pm_player(self.author, formatted_string))
        else:
            print("User not registered!")
    
    
    def get_leaderboard(self):
        leaderboard = self.curr_stats.get_leaderboard()
        formatted_string = "``` --------LEADERBOARD--------\n"
        for stats in leaderboard:
            formatted_string += "\n" + self.stats_to_string(stats) + "\n"
            formatted_string += "---------------------------\n"
        formatted_string += "```"
        
        asyncio.ensure_future(self.pm_player(self.author, formatted_string))
    
    def stats_to_string(self, player_stats):
        player_name = self.message_obj.server.get_member(player_stats['ID']).name
        nick_name = (self.message_obj.server.get_member(player_stats['ID']).nick or player_name)
        formatted_string = "Player Name: " + player_name + "\n"
        formatted_string += "Player Nickname: " + nick_name + "\n"
        for key in player_stats.keys():
            if (key != "ID"):
                formatted_string += "\t" + key + ": " + str(player_stats[key]) + "\n"
        return formatted_string
    
    
    #Dictionary of functions, allows for modularity in "run_command"
    command_list = {
        "register" : register_user,
        "stats" : get_stats,
        "leaderboard" : get_leaderboard
    }
    
    
    def run_command(self):
        #make sure command is a real command and is enabled
        if (self.command_id in self.command_list):
            print("_________________________")
            print("Command issued: " + self.command_id)
            print("_________________________")
            command_function = self.command_list[self.command_id]
            return command_function(self)
        else:
            return NOT_COMMAND