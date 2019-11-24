

import os
import re
import sys

import task_translator
import json_manager
import tile_manager
import exr_stitch





'''

    FUTURE:    
    read log file area

        # create collector for data from log file
        log_data = dict( time=None, errors=[] )

        # load log
        log_file = open(sys.argv[1], "r")
        log_sheet = log_file.read()
        log_file.close()


'''




# get current task data
task_data = task_translator.get_task(sys.argv[2])

# get history data
history_path = os.path.join(os.path.dirname(__file__), "history.json")
history_data = json_manager.read(history_path)




# find match in history for current task
for history_task in history_data:

    match_file = task_data["katanaFile"]==history_task["katanaFile"]
    match_node = task_data["renderNode"]==history_task["renderNode"]
    match_vars = task_data["var"]==history_task["var"]

    if match_file and match_node and match_vars:


        for frame_item in history_task["frames"]:
            if frame_item["frame"] == task_data["frame"]:


                tiles = task_data["tiles"]
                if tiles and not frame_item["complete"]:

                    has_missed = tile_manager.get_next(tiles)
                    if has_missed: sys.exit()

                    scene_file = history_task["katanaFile"]
                    outputs = exr_stitch.stitch_outputs(scene_file)
                    if not outputs: sys.exit()


                # update history, change task state to completed
                frame_item["complete"] = True

                json_manager.write(history_path, history_data)
                sys.exit()
