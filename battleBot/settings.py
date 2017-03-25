import os.path
import sys
import time
import json
from .json_ops import JSONReaderWriter


class JSONSettings:


    def __init__(self, program_path):
        #create settings reader, and check to make sure it exists
        self.settings = JSONReaderWriter(program_path + os.path.sep + 'settings.JSON')
        self.settings_chk()
        #read settings in loaded json file
        self.parsed_settings = self.settings.read()


    def settings_chk(self):
        #Generate settings json if not present
        if not self.settings.exists():
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
