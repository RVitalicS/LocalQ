

import os
import sys
import time

import json_manager
import tile_manager
import task_translator



# get settings data
settings_path = os.path.join(os.path.dirname(__file__), 'settings.json')
settings_data = json_manager.read(settings_path)





# get slave name
slave = os.getenv('COMPUTERNAME')


# exit point
if 'ALL' in settings_data['exit']: sys.exit()
if slave in settings_data['exit']: sys.exit()


# work on free hours only
if settings_data['timeException']:
    
    day     = time.localtime().tm_wday
    hours   = time.localtime().tm_hour
    minutes = time.localtime().tm_min

    if day < 4:

        current_time = hours * 60 + minutes

        morning =  7 * 60
        evening = 18 * 60

        if morning < current_time < evening:
            sys.exit()





# create history path
history_path = os.path.join(os.path.dirname(__file__), 'history.json')


# figure out next command
for task in settings_data['tasks']:


    # extract task data
    comments        = task['comments']
    katanaFile      = task['katanaFile']
    renderNode      = task['renderNode']
    var             = task['var']
    frameFrom       = task['frameFrom']
    frameTo         = task['frameTo']
    tileRender      = task['tileRender']
    allowedSlaves   = task['allowedSlaves']
    forbiddenSlaves = task['forbiddenSlaves']


    # define frame item
    frame_item = dict(
        frame=0,
        tiles=None,
        complete=False,
        time='',
        slaves=[slave],
        errors=[])

    tile=None
    if tileRender:
        tileResolution = settings_data['tileResolution']
        raws = tileResolution['raws']

        tile_structure = [ [] for i in range(raws) ]
        tile = tile_manager.get_next(tile_structure)
        
        column = tile[0]
        raw    = tile[1]
        
        tile_structure[raw].append(column) 
        frame_item['tiles'] = tile_structure


    # check permissions
    if len(allowedSlaves) > 0 and slave not in allowedSlaves:
        continue
    if slave in forbiddenSlaves:
        continue



    # for the same task
    match_file = False
    match_node = False
    match_vars = False

    complete = False


    history_data = json_manager.read(history_path)

    for history_task in history_data:

        history_katanaFile = history_task['katanaFile']
        history_renderNode = history_task['renderNode']
        history_var        = history_task['var']
        history_frames     = [i['frame'] for i in history_task['frames']]

        match_file = katanaFile==history_katanaFile
        match_node = renderNode==history_renderNode
        match_vars = var==history_var

        if match_file and match_node and match_vars:


            if tileRender:
                for history_frame in history_task['frames']:

                    if not history_frame['complete']:
                        history_tiles = history_frame['tiles']

                        next_tile = tile_manager.get_next(history_tiles)

                        if next_tile:
                            column = next_tile[0]
                            raw    = next_tile[1]

                            history_tiles[raw].append(column)
                            for raw in history_tiles: raw=raw.sort()

                            history_task['frames'] = sorted(history_task['frames'], key=lambda k: k['frame'])

                            if slave not in history_frame['slaves']:
                                history_frame['slaves'].append(slave)

                            render_frame = history_frame['frame']

                            json_manager.write(history_path, history_data)
                            print(task_translator.get_command(task, render_frame, tile=next_tile))

                            sys.exit()

            
            while frameFrom <= frameTo:
                if frameFrom not in history_frames:

                    frame_item['frame'] = frameFrom

                    history_task['frames'].append(frame_item)
                    history_task['frames'] = sorted(history_task['frames'], key=lambda k: k['frame'])

                    render_frame = frame_item['frame']

                    json_manager.write(history_path, history_data)
                    print(task_translator.get_command(task, render_frame, tile=tile))

                    sys.exit()

                frameFrom += 1

            complete = True

    if complete: continue




    # for new task or empty history
    frame_item['frame'] = frameFrom


    # define history item
    history_item = dict(
        katanaFile=katanaFile,
        renderNode=renderNode,
        frames=[frame_item],
        var=var,
        complete=False,
        reported=False,
        comments=comments)

    history_data.append(history_item)



    json_manager.write(history_path, history_data)
    print(task_translator.get_command(task, frameFrom, tile=tile))

    sys.exit()
