

import os
import json_manager


# get settings data
settings_path = os.path.join(os.path.dirname(__file__), "settings.json")
settings_data = json_manager.read(settings_path)


tileResolution = settings_data["tileResolution"]

raws    = tileResolution["raws"]
columns = tileResolution["columns"]



def get_resolution():
    return [columns, raws]





def get_next (data, vertical=True):

    if vertical:  return    vertical_order(data)
    else:         return  horizontal_order(data)





def horizontal_order (data):

    for raw in reversed(range(raws)):

        item_count = len(data[raw])
        if not item_count >= columns:

            for column in range(columns):
                if column not in data[raw]:

                    return [column, raw]



def vertical_order (data):

    for column in range(columns):

        for raw in reversed(range(raws)):
            if column not in data[raw]:

                item_count = len(data[raw])
                if not item_count >= columns:

                    return [column, raw]
