import os
import sys
import time
import json_manager


# get history path
history_path = os.path.join(os.path.dirname(__file__), "history.json")

# get settings data
settings_path = os.path.join(os.path.dirname(__file__), "settings.json")
settings_data = json_manager.read(settings_path)



# check for shutdown switch in settings
if settings_data["shutdown"]:


    # find right key to turn off computer
    for argument in sys.argv:
        if argument == "-shutdown":


            shutdown_command = "SHUTDOWN /s /f /t 0"


            # for all except server turn off without questions
            if os.getenv("COMPUTERNAME") != settings_data["server"]:
                print(shutdown_command)
                sys.exit()


            # for server machine
            # check history that every task is completed
            else:

                job_done = False
                while not job_done:

                    job_done = True

                    for history_task in json_manager.read(history_path):
                        for frame_item in history_task["frames"]:

                            if not frame_item["complete"]:
                                job_done = False

                    if not job_done:
                        time.sleep(60)


                # then turn off
                print(shutdown_command)
                sys.exit()
