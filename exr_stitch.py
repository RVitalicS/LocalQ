

import subprocess
import shutil

import json_manager
import tile_manager
import home
import name_math

import os
import re
import sys





home_directory = home.get()

ExrTileStitch = os.path.join(home_directory, 'bin', 'exrtilestitch.exe')

if os.path.exists(ExrTileStitch):
    ExrTileStitch = '"{}"'.format(ExrTileStitch)

else: sys.exit()






def find_outputs (path):

    # if input path is katana scene
    if os.path.isfile(path):
        path = os.path.dirname(path)


    directories = []

    for file in os.listdir(path):
        directory = os.path.join(path, file)
        
        if os.path.isfile(directory):

            if re.match("tile_\d+_\d+\.", file):
                return path

        elif os.path.isdir(directory):
            directories.append(directory)

    for directory in directories:
        path = find_outputs(directory)

        if path:
            return path




def output_names (path):

    names = []

    for item in os.listdir(path):

        if re.match("^tile_\d+_\d+\..+\.exr$", item):

            item = re.sub("^tile_\d+_\d+\.", "", item)
            item = re.sub("\.exr", "", item)

            if item not in names:
                names.append(item)

    return names





def group_outputs (path):

    groups = []

    for name in output_names(path):
        outputs = []

        for file in os.listdir(path):

            if re.match('.+{}.+'.format(name), file):
                outputs.append(os.path.join(path, file))

        resolution = tile_manager.get_resolution()
        required_count = resolution[0] * resolution[1]

        if len(outputs) == required_count:

            groups.append({
                'xtiles': resolution[0],
                'ytiles': resolution[1],
                'output': os.path.join(path, '{}.exr'.format(name)),
                'outputs': outputs})

    return groups





def stitch_outputs (path):

    output_directory = find_outputs(path)
    outputs = []

    if output_directory:
        if os.path.exists(output_directory):


            backup_path = os.path.join(output_directory, 'backups')
            if not os.path.exists(backup_path):
                os.mkdir(backup_path)


            for group in group_outputs(output_directory):

                xtiles  = str(group['xtiles'])
                ytiles  = str(group['ytiles'])

                tile_outputs = group['outputs']
                tile_outputs = ['"{}"'.format(i) for i in tile_outputs]
                tile_outputs = ' '.join(tile_outputs)

                output  = group['output']
                output  = '"{}"'.format(output)

                arguments = [
                    ExrTileStitch,
                    xtiles,
                    ytiles,
                    tile_outputs,
                    output ]

                process = subprocess.Popen(' '.join(arguments))
                process.wait()

                outputs.append(group['output'])


                for file in group['outputs']:

                    base_name = os.path.basename(file)
                    base_name = re.sub('^tile','backup', base_name)
                    backup_file = os.path.join(backup_path, base_name)

                    shutil.move(file, backup_file)


    return outputs





if __name__ == "__main__":
    
    arguments = sys.argv
    if len(arguments)> 1:

        stitch_outputs(arguments[1])
