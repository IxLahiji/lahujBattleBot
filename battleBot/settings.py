import os.path
import sys
import time
from .json_ops import JSONReaderWriter


class JSONSettings:


    def __init__(self, program_path):
        #create settings reader, and check to make sure it exists
        self.settings = JSONReaderWriter(program_path + os.path.sep + 'settings.JSON')
        self.settings_chk()
        #read settings in loaded json file
        try:
            self.parsed_settings = self.settings.read()
        except:
            print ("Error: Invalid settings file. Please either fix or delete the JSON file!")
            time.sleep(3)
            sys.exit()


    def settings_chk(self):
        import json
        #Generate settings json if not present
        if not self.settings.exists():
            print("No settings file found. Generating a new settings JSON file...")
            #Defining keys for the JSON file, as well as configuring default values
            default_json = {"discord_token": "",
                                "default_stats":{"Level": 1,
                                        "Health": 10.0,
                                        "Max Health": 10.0,
                                        "Attack": 1.0,
                                        "M. Attack": 1.0,
                                        "Defense": 1.0,
                                        "M. Defense": 1.0,
                                        "Experience": 0.0,
                                        "Experience Needed": 10.0},
                                "Auto Regen Cooldown(h)": 5,
                                "Auto Regen Amount": 2.0,
                                "Message Regen Cooldown(m)": 10,
                                "Message Regen Amount": 0.1}
                       
            loaded_json = json.loads(default_json)
            self.settings.write(loaded_json)
            
            print("The settings file has been generated. Please add a token for your discord bot before the next execution.")
            time.sleep(3)
            sys.exit()

            
    def get_setting(self, setting):
        #Check to make sure requested item is present
        if (not (setting in self.parsed_settings)):
            print ("Error: Invalid settings file. Please either fix or delete the JSON file!")
            time.sleep(3)
            sys.exit()
        else:
            return self.parsed_settings[setting]
