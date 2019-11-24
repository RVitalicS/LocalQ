

import subprocess
import shutil

import json_manager
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




def tile_resolution (output_list):

    tile_tags = []
    for output in output_list:

        tile = re.search('tile_\d+_\d+', output)
        if tile:
            tile = tile.group(0)
            if tile not in tile_tags:
                tile_tags.append(tile)

    xtiles = 1
    ytiles = 1

    for tag in tile_tags:

        x = re.sub('tile_', '', tag)
        x = re.sub('_\d+$', '', x)
        x = int(x) + 1
        if x > xtiles: xtiles = x

        y = re.sub('^tile_\d+_', '', tag)
        y = int(y) + 1
        if y > ytiles: ytiles = y

    return {'xtiles': xtiles, 'ytiles': ytiles}




def group_outputs (path):

    groups = []

    for name in output_names(path):
        outputs = []

        for file in os.listdir(path):

            if re.match('.+{}.+'.format(name), file):
                outputs.append(os.path.join(path, file))

        if outputs:

            resolution = tile_resolution(outputs)

            groups.append({
                **resolution,
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

                outputs = group['outputs']
                outputs = ['"{}"'.format(i) for i in outputs]
                outputs = ' '.join(outputs)

                output  = group['output']
                output  = '"{}"'.format(output)

                arguments = [
                    ExrTileStitch,
                    xtiles,
                    ytiles,
                    outputs,
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
