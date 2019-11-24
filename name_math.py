
import re
import os
import sys




def string_intersections ( tester, testee ):

    index=0
    intersection = ""
    intersections = []
    inword = False

    for character in tester:

        while index < len(testee):

            if character == testee[index]:
                intersection += character
                index += 1
                inword = True
                break

            elif inword:
                if intersection and len(intersection)>1:
                    intersections.append(intersection)
                inword = False
                index=0
                intersection = ""

            else:
                index += 1

        else:
            if intersection and len(intersection)>1:
                intersections.append(intersection)
            inword = False
            index=0
            intersection = ""

    return intersections





def get_base ( *args ):

    base_name = ""
    if len(args) > 1:


        names = []
        for item in args:
            if os.path.exists(item):
                item = os.path.basename(item)
                item = re.sub("tile_\d+_\d+\.", "", item)
                item = re.sub("\.exr$", "", item)
                names.append(item)
            else:
                names.append(item)

        if names:


            intersections = []
            for tester in names:
                for testee in names:

                    intersection = string_intersections(tester, testee)
                    for name in intersection:
                        if name not in intersections:
                            intersections.append(name)


            base_names = []
            for name in intersections:
                all_has = True

                for input_name in args:
                    if os.path.exists(input_name):
                        input_name = os.path.basename(input_name)
                    if not re.match(".*{}.*".format(name), input_name):
                        all_has = False

                if all_has:
                    base_names.append(name)


            base_name = ""
            for name in base_names:
                if name > base_name:
                    base_name = name

            base_name = re.sub("^_*", "", base_name)
            base_name = re.sub("_*$", "", base_name)

            return base_name


    else: return ""





if __name__ == "__main__":

    arguments = sys.argv
    if len(arguments)> 1:

        print( get_base(*arguments[1:]) )
        input()
