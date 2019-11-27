import os
import json
import time
import random
import bug_log





def write (path_in, data):

    '''
        Write list or dictionary data to json file
    
        Args:
            path_in <type 'str'>: Path to json file
            data <type 'dict'|'list'>: Data that will be saved to json file

        Return:
            <type 'bool'>: Success of a record
    '''

    success = False
    while not success:

        try:
            if os.path.exists(path_in):
                os.rename(path_in, path_in)

            with open(path_in, 'w') as file_write:
                json.dump(data, file_write, indent=4)

            success = True

        except Exception as exception_message:
            bug_log.write(__name__, str(exception_message))
            time.sleep(random.randint(0, 30))

    return True





def read (path_in):

    '''
        Read data from json file
        
        Args:
            path_in <type 'str'>: Path to json file

        Return:
            <type 'dict'|'list'>: Data from json file
    '''

    if not os.path.exists(path_in):
        write(path_in, [])

    data = None

    with open(path_in, 'r') as file_read:
        data = json.load(file_read)
    
    return data
