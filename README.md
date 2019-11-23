# LocalQ

**is a simple program that distribute render tasks for Foundry Katana program between machines where this program was launched**


### Help
1. share directory that this file is located
2. fill out settings.json
    * *"server"* - set this to computer name that stores render data and it would be turned off last when the calculations were over
    * *"shutdown"* - global switcher to turn off computers
    * *"katanaEnvironment"* - directory path to katanaBin.exe or \*.bat file with defined resources
    * *"tasks"* - fill out this list with *"taskItemTemplate"* > \[ \{\...}, \{\...}, ... \] \('var' is optional and could be an empty dictionary\)
3. run "QueManager.bat" on all computers
4. delete "log" folder and "history.json"


### Arguments for QueueManager.bat
**-shutdown**: keyword argument \(optional\) to turn off computer when the calculations were over \(depending on switch in settings.json file\)


### Required
python \*.\* \(used 3.7\)
