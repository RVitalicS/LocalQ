import json
import time
import random



def read (path_in):

    '''
        Read data from json file
        
        Args:
            path_in <type 'str'>: Path to json file

        Return:
            <type 'dict'|'list'>: Data from json file
    '''

    data = None

    success = False
    while not success:

        try:
            with open(path_in, 'r') as file_in:
                data = json.load(file_in)
            success = True

        except:
            time.sleep(random.randint(0, 30))
    
    return data




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
            with open(path_in, 'w') as file_in:
                json.dump(data, file_in, indent=4)
            success = True

        except:
            time.sleep(random.randint(0, 30))

    return True
