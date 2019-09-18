import os
import sys
import json_manager
import task_translator



# get settings data
settings_path = os.path.join(os.path.dirname(__file__), "settings.json")
settings_data = json_manager.read(settings_path)

# create history path
history_path = os.path.join(os.path.dirname(__file__), "history.json")



# define frame item
frame_item = dict(
    frame=0,
    complete=False,
    time="",
    slave="",
    errors=[])



# figure out next command
for task in settings_data["tasks"]:


    # extract task data
    comments        = task["comments"]
    katanaFile      = task["katanaFile"]
    renderNode      = task["renderNode"]
    var             = task["var"]
    frameFrom       = task["frameFrom"]
    frameTo         = task["frameTo"]
    allowedSlaves   = task["allowedSlaves"]
    forbiddenSlaves = task["forbiddenSlaves"]


    # check permissions
    slave = os.getenv("COMPUTERNAME")
    if len(allowedSlaves) > 0 and slave not in allowedSlaves:
        sys.exit()
    if slave in forbiddenSlaves:
        sys.exit()


    # get history data
    if not os.path.exists(history_path):
        json_manager.write(history_path, [])
    history_data = json_manager.read(history_path)



    # for the same task
    match_file = False
    match_node = False
    match_vars = False

    complete = False
    for history_task in history_data:

        history_katanaFile = history_task["katanaFile"]
        history_renderNode = history_task["renderNode"]
        history_var        = history_task["var"]
        history_frames     = [i["frame"] for i in history_task["frames"]]

        match_file = katanaFile==history_katanaFile
        match_node = renderNode==history_renderNode
        match_vars = var==history_var

        if match_file and match_node and match_vars:

            while frameFrom <= frameTo:
                if frameFrom not in history_frames:

                    frame_item["frame"] = frameFrom
                    frame_item["slave"] = slave

                    history_task["frames"].append(frame_item)
                    history_task["frames"] = sorted(history_task["frames"], key=lambda k: k["frame"])
                  
                    json_manager.write(history_path, history_data)
                    print(task_translator.get_command(task, frameFrom))

                    sys.exit()

                frameFrom += 1

            complete = True

    if complete: continue



    # for new task or empty history
    history_item = {}

    history_item["comments"]   = comments
    history_item["katanaFile"] = katanaFile
    history_item["renderNode"] = renderNode

    history_item["var"] = var

    frame_item["frame"] = frameFrom
    frame_item["slave"] = slave
    history_item["frames"] = [frame_item]

    history_data.append(history_item)
    
    json_manager.write(history_path, history_data)
    print(task_translator.get_command(task, frameFrom))

    sys.exit()
