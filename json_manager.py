import json
import time
import random




def save_string (file_name, string_data):

    '''
        Appends input string data
        to the existing or new file with input name

        Args:
            file_name    <type 'str'>: name of the file to add data
            string_data  <type 'str'>: data to append
    '''


    file_path = os.path.join(os.path.dirname(__file__), "{}.txt".format(file_name))

    if not os.path.exists(file_path):
        file = open(file_path, "w")
        file.close()

    file = open(file_path, "r")
    file_data = file.read()
    file.close()

    if file_data: file_data += "\n"

    file_data += append_data

    file = open(file_path, "w")
    file.write(file_data)
    file.close()




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

        except Exception as exception_message:
            save_string("exceptions_read", exception_message)
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

        except Exception as exception_message:
            save_string("exceptions_write", exception_message)
            time.sleep(random.randint(0, 30))

    return True
