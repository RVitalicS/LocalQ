import os
import sys
import task_translator



# create not existing subfolder
log_path = os.path.join(os.path.dirname(__file__), "log")
if not os.path.exists(log_path): os.makedirs(log_path)

# get current task settings
task = task_translator.get_task(sys.argv[1])



# define collector for names
name_list = []


# get name of "Katana" file
katanaFile = os.path.basename(task["katanaFile"])
katanaFile = os.path.splitext(katanaFile)[0]
name_list.append(katanaFile)

# get pairs of variables
var = task["var"]
var = [key + var[key][0].upper() + var[key][1:] for key in var]
var = "_".join(var)
if len(var) > 0: name_list.append(var)


frame = task["frame"]
name_list.append("frame{:04d}".format(frame))

tile = task["tile"]
if tile: name_list.append("tile{}{}".format(tile[0], tile[1]))

renderNode = task["renderNode"]
name_list.append(renderNode)


# create name of log file
name_string = "_".join(name_list) + ".txt"

# create path to log file
log_path = os.path.join(log_path, name_string)
log_path = os.path.normpath(log_path)



with open(log_path, 'w') as log_file:
    log_file.write('{}\n'.format(os.getenv('COMPUTERNAME')))


# share log file path
print(log_path)
