import os.path
import sys
import time
from .json_ops import JSONReaderWriter


class JSONStats:


    def __init__(self, program_path):
        #create settings reader, and check to make sure it exists
        self.stats = JSONReaderWriter(program_path + os.path.sep + 'stats.JSON')
        self.stats_chk()
        #read settings in loaded json file
        try:
            self.parsed_stats = self.stats.read()
        except:
            print ("Error: Invalid stats file. Please either fix or delete the JSON file!")
            time.sleep(3)
            sys.exit()
    
    
    def stats_chk(self):
        import json
        #Generate empty JSON file on start-up if not present
        if not self.stats.exists():
            print("No stats file found. Generating a new statistic JSON file...")
            #Defining keys for the JSON file, as well as configuring default values
            default_json = """{}
                       """
            loaded_json = json.loads(default_json)
            self.stats.write(loaded_json)
            
            print("A new empty stats file has been generated.")

	
    def generate_player_stats(self, player):
        print ("Creating stats for new user " + player.name)
        self.parsed_stats[player.id] = {"ID": player.id,
                                    "Level": 1,
                                    "Health": 10.0,
                                    "Max Health": 10.0,
                                    "Attack": 1.0,
                                    "M. Attack": 1.0,
                                    "Defense": 1.0,
                                    "M. Defense": 1.0,
                                    "Experience": 0.0,
                                    "Experience Needed": 10.0}
        self.stats.write(self.parsed_stats)
        
        
    def set_stat(self, player, stat, value):
        if (has_stats(player)):
            (self.parsed_stats[player.id]) [stat] = value
            self.stats.write(self.parsed_stats)
        else:
            generate_player_stats(player)
    
	
	def increment_health(self, player, amount):
		if (has_stats(player)):
			pass
    
	
    def has_stats(self, player):
        return (not (self.get_player_stats(player.id) is None))
    
    
    def get_player_stats(self, player):
        if (has_stats(player)):
            return self.parsed_stats[player.id]
        else:
            return None
    
    
    def get_leaderboard(self):
        temp_list = sorted(self.parsed_stats, key=lambda k:self.parsed_stats[k]['Level'], reverse=True)
        if (len(temp_list) < 3):
            return [self.parsed_stats[k] for k in temp_list]
        else:
            return [self.parsed_stats[k] for k in temp_list[:3]]

