import os


def write (file_name, string_data):

    '''
        Appends input string data
        to the existing or new file with input name

        Args:
            file_name    <type 'str'>: name of the file to add data
            string_data  <type 'str'>: data to append
    '''


    file_path = os.path.join(os.path.dirname(__file__), "{}_{}.txt".format(file_name, os.getenv("COMPUTERNAME")))

    if not os.path.exists(file_path):
        file = open(file_path, "w")
        file.close()

    file = open(file_path, "r")
    file_data = file.read()
    file.close()

    if file_data: file_data += "\n"

    file_data += string_data

    success = False
    while not success:

        try:
            if os.path.exists(file_path):
                os.rename(file_path, file_path)

            file = open(file_path, "w")
            file.write(file_data)
            file.close()

            success = True

        except:
            time.sleep(random.randint(1, 5))
