import json
import os.path
import sys
import time

class JSONSettings:

	settings_path = ""
	parsed_settings = {}

	def __init__(self, program_path):
		self.settings_path = program_path + os.path.sep + 'settings.JSON'
		self.settings_chk()
		self.read_settings()

		
	def write_settings(self, settings):
		#Open JSON credentials file for writing
		settings_file = open(self.settings_path, 'w')
		json.dump(settings, settings_file, indent=4, sort_keys=True)
		settings_file.close()


	def read_settings(self):
		#Open JSON credentials file for reading and parse
		settings_file = open(self.settings_path, 'r')
		self.parsed_settings = json.loads(settings_file.read())
		settings_file.close()


	def settings_chk(self):
		#Generate credential and blacklist JSON files on startup if not present
		if not os.path.exists(self.settings_path):
			print("No settings file found. Generating a new settings JSON file...")
			#Defining keys for the JSON file, as well as configuring default values
			default_json = """{"discord_token": ""}
					   """
			parsed_json = json.loads(default_json)
			self.write_settings(parsed_json)
			
			print("The settings file has been generated. Please add a token for your discord bot before the next execution.")
			time.sleep(3)
			sys.exit()

			
	def get_token(self):
		#Check to make sure token is present
		if (not ('discord_token' in self.parsed_settings)):
			print ("Invalid 'settings.JSON' file. Please delete the file, and restart application.")
			time.sleep(3)
			sys.exit()
		if (not self.parsed_settings['discord_token']):
			print ("Please enter a discord bot token in 'settings.JSON' before running")
			time.sleep(3)
			sys.exit()
		else:
			return self.parsed_settings['discord_token']
