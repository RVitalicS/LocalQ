

import os
import shutil

this_dir = os.path.dirname(__file__)



for item in ["__pycache__", "log", "history.json"]:

    target = os.path.join(this_dir, item)
    if os.path.exists(target):



        if os.path.isfile(target):
            os.remove(target)

        else:
            shutil.rmtree(target)
