import os
import re
import json_manager


# get settings data
settings_path = os.path.join(os.path.dirname(__file__), "settings.json")
settings_data = json_manager.read(settings_path)




def get_command (task_dictionary, frame_target):

    '''
        Creates string command for "Command Prompt"
        that runs "Katana" programm in batch mode
        
        Args:
            task_dictionary <type 'dict'>: settings for creating rendering task
            frame_target     <type 'int'>: frame to calculate

        Return:
            <type 'str'>: command to run "Katana" in batch mode
    '''


    join_list = []

    join_list.append(settings_data["katanaEnvironment"])
    join_list.append("--batch")

    katanaFile = r'--katana-file="{}"'.format( task_dictionary["katanaFile"] )
    join_list.append(katanaFile)


    for key in task_dictionary["var"]:

        var_key = key
        var_val = task_dictionary["var"][key]

        var = "--var {}={}".format( var_key, var_val )
        join_list.append(var)


    renderNode = r'--render-node={}'.format( task_dictionary["renderNode"] )
    threads3d = r'--threads3d={}'.format( task_dictionary["threads3d"] )
    join_list.append(renderNode)
    join_list.append(threads3d)

    frame = "-t {}".format(frame_target)
    join_list.append(frame)

    command_string = " ".join(join_list)

    return command_string




def get_task (task_string):

    '''
        Parse string command that runs "Katana" program in batch mode
        and converts it back to settings like data
        
        Args:
            task_string <type 'str'>: "Command Prompt" command

        Return:
            <type 'dict'>: settings data for current rendering task
    '''


    task = {}

    katanaFile = re.search(r"\s--katana-file[^\s]+\s", task_string)
    if katanaFile:
        katanaFile = re.sub(" ", "", katanaFile.group(0))
        katanaFile = re.sub("--katana-file=", "", katanaFile)
        task["katanaFile"] = katanaFile

    var = {}
    variables = re.findall(r"--var\s[^\s]+", task_string)
    if variables:
        variables = [re.sub("--var ", "", i).split("=") for i in variables]
        for variable in variables:
            var[variable[0]] = variable[1]
    task["var"] = var

    threads3d = re.search(r"--threads3d=\d+", task_string)
    if threads3d:
        threads3d = re.sub("--threads3d=", "", threads3d.group(0))
        if threads3d.isdigit():
            task["threads3d"] = int(threads3d)

    renderNode = re.search(r"--render-node=[^\s]+", task_string)
    if renderNode:
        renderNode = re.sub("--render-node=", "", renderNode.group(0))
        task["renderNode"] = renderNode

    frame = re.search(r"-t\s\d+", task_string)
    if frame:
        frame = re.sub("-t ", "", frame.group(0))
        if frame.isdigit():
            task["frame"] = int(frame)

    return task
