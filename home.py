

import os
import re
import json_manager



def get():

    home_dir = os.getenv("KATANA_HOME", "")
    if not home_dir:

        settings_path = os.path.join(os.path.dirname(__file__), "settings.json")
        settings_data = json_manager.read(settings_path)

        bat_path = settings_data["katanaEnvironment"]

        if os.path.splitext(bat_path)[-1] == ".bat":
            if os.path.exists(bat_path):

                with open(bat_path, "r") as file:

                    bat_data = file.readlines()
                    for line in bat_data:

                        home_data = re.match("^SET.*KATANA_HOME=.*", line)
                        if home_data:
                            home_data = home_data.group(0)
                            home_data = re.sub("'", "", home_data)
                            home_data = re.sub('"', "", home_data)
                            home_data = re.sub("^.*\=", "", home_data)
                            
                            home_dir = home_data

    return home_dir
