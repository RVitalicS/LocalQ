

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
        log_file = open(sys.argv[1], 'r')
        log_sheet = log_file.read()
        log_file.close()


'''




# get current task data
task_data = task_translator.get_task(sys.argv[2])

# get history data
history_path = os.path.join(os.path.dirname(__file__), 'history.json')
history_data = json_manager.read(history_path)


# get settings data
settings_path = os.path.join(os.path.dirname(__file__), 'settings.json')
settings_data = json_manager.read(settings_path)




def find_task (input_data):

    input_file = input_data['katanaFile']
    input_node = input_data['renderNode']
    input_vars = input_data['var']

    for task in settings_data['tasks']:

        task_file = task['katanaFile']
        task_node = task['renderNode']
        task_vars = task['var']

        match_file = input_file==task_file
        match_node = input_node==task_node
        match_vars = input_vars==task_vars

        if match_file and match_node and match_vars:

            return task




# find match in history for current task
for history_task in history_data:

    match_file = task_data['katanaFile']==history_task['katanaFile']
    match_node = task_data['renderNode']==history_task['renderNode']
    match_vars = task_data['var']==history_task['var']

    if match_file and match_node and match_vars:

        data_changed = False

        for frame_item in history_task['frames']:
            if frame_item['frame'] == task_data['frame']:


                tiles = task_data['tiles']
                if tiles and not frame_item['complete']:

                    has_missed = tile_manager.get_next(tiles)
                    if has_missed: break

                    scene_file = history_task['katanaFile']
                    outputs = exr_stitch.stitch_outputs(scene_file)
                    if not outputs: break


                # update history, change frame state to completed
                frame_item['complete'] = True
                data_changed = True
                break




        # check task state
        settings_task = find_task(task_data)

        frameFrom = settings_task['frameFrom']
        frameTo   = settings_task['frameTo']

        frames_count = frameTo - frameFrom + 1

        complete_count = 0
        for frame_item in history_task['frames']:
            if frame_item['complete']:
                complete_count +=1

        if frames_count == complete_count:
            history_task['complete'] = True
            data_changed = True




        if data_changed:
            json_manager.write(history_path, history_data)
            sys.exit()
