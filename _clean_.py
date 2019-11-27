

import os
import re
import shutil

this_dir = os.path.dirname(__file__)
black_list = []



for item in ["__pycache__", "log", "history.json"]:

    victim = os.path.join(this_dir, item)
    if os.path.exists(victim):

        black_list.append(victim)



for item in os.listdir(this_dir):

    for ext in ["pyc", "txt"]:
        if re.match(".*\.{}$".format(ext), item):

            victim = os.path.join(this_dir, item)
            if os.path.exists(victim):

                black_list.append(victim)




for victim in black_list:

    if os.path.isfile(victim):
        os.remove(victim)

    else:
        shutil.rmtree(victim)
