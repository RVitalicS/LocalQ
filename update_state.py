import os
import re
import sys
import time
import task_translator
import json_manager



# create collector for data from log file
log_data = dict( time=None, errors=[] )

# load log
log_file = open(sys.argv[1], "r")
log_sheet = log_file.read()
log_file.close()



# find final string that declares completed task and append time to collector
complete_state = re.search(r"\[INFO.*\]: Frame \d+ completed in .*", log_sheet)
if complete_state:
    complete_in = re.search(r"(?<=in\s).*", complete_state.group(0))
    if complete_in:
        log_data["time"] = complete_in.group(0)


# find errors and append those to collector
error_pattern = re.compile(".*[Ee][Rr][Rr][Oo][Rr].*")
error_result  = error_pattern.findall(log_sheet)
for error_item in error_result:

    # pass "Traktor" errors (temporarily)
    error_match = re.match(".*QT4FormWidgets.*", error_item)
    if error_match:
        continue

    # append the rest
    else: log_data["errors"].append(error_item)



# if final string (time) was not found then just move on
if not isinstance(log_data["time"], str): sys.exit()





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


                # update history, change task state to completed
                frame_item["complete"] = True
                frame_item["time"]     = log_data["time"]
                frame_item["errors"]   = log_data["errors"]

                json_manager.write(history_path, history_data)
                sys.exit()
