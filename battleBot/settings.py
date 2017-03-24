import json
import os.path
import sys
import time


class JSONSettings:


    def __init__(self, program_path):
        self.settings = JSONReaderWriter(program_path + os.path.sep + 'settings.JSON')
        self.settings_chk()
        self.parsed_settings = self.read_settings()


    def settings_chk(self):
        #Generate credential and blacklist JSON files on startup if not present
        if not settings.exists():
            print("No settings file found. Generating a new settings JSON file...")
            #Defining keys for the JSON file, as well as configuring default values
            default_json = """{"discord_token": ""}
                       """
            loaded_json = json.loads(default_json)
            self.settings.write(loaded_json)
            
            print("The settings file has been generated. Please add a token for your discord bot before the next execution.")
            time.sleep(3)
            sys.exit()

            
    def get_setting(self, setting):
        #Check to make sure requested item is present
        if (not (setting in self.parsed_settings)):
            print ("Invalid 'settings.JSON' file. Please delete the file, and restart application.")
            time.sleep(3)
            sys.exit()
        else:
            return self.parsed_settings[setting]
