

import os
import json_manager



# call settings data
settings_path = os.path.join(os.path.dirname(__file__), "settings.json")
settings_data = json_manager.read(settings_path)


if settings_data:
    print("VALID SETTINGS")
