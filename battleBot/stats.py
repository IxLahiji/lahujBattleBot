import json
import os.path
import sys
import time

class JSONStats:

	stats_path = ""
	parsed_stats = {}

	def __init__(self, program_path):
		self.stats_path = program_path + os.path.sep + 'stats.JSON'
		self.stats_chk()
		self.read_stats()

		
	def write_stats(self, settings):
		#Open JSON credentials file for writing
		stats_file = open(self.stats_path, 'w')
		json.dump(settings, stats_file, indent=4, sort_keys=True)
		stats_file.close()


	def read_stats(self):
		#Open JSON credentials file for reading and parse
		stats_file = open(self.stats_path, 'r')
		self.parsed_stats = json.loads(stats_file.read())
		stats_file.close()


	def stats_chk(self):
		#Generate empty JSON file on start-up if not present
		if not os.path.exists(self.stats_path):
			print("No stats file found. Generating a new statistic JSON file...")
			#Defining keys for the JSON file, as well as configuring default values
			default_json = """{}
					   """
			parsed_json = json.loads(default_json)
			self.write_stats(parsed_json)
			
			print("A new empty stats file has been generated.")

	def generate_player_stats(self, player):
		self.parsed_stats[player.id] = {"Name": player.name,
									"Health": 10.0,
									"Max Health": 10.0}
		
		
	def set_stat(self, player, stat, value):
		if (player.id in self.parsed_stats):
			(self.parsed_stats[player.id]) [stat] = value
		else:
			generate_player_stats(player)
		
		
	def get_player_stats(self, player): #TODO
		pass


