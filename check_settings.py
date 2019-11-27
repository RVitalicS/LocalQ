

import json_manager

import os
import sys






if __name__ =='__main__':
    if len(sys.argv) > 1:

        file = sys.argv[1]
        if os.path.exists(file):
            if os.path.splitext(file)[-1] == '.json':


                data = json_manager.read(file)
                print(data)
                input()
                sys.exit()





# call settings data
settings_path = os.path.join(os.path.dirname(__file__), 'settings.json')
settings_data = json_manager.read(settings_path)


if settings_data:
    print('VALID SETTINGS')
