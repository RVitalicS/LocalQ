# LocalQ

**is a simple program to distribute render tasks of Foundry Katana program**


### Help
1. share directory that this file is located
2. fill out settings.json
    * *"server"* - set this to computer name that stores render data and that might be turned off last when the calculations were over
    * *"shutdown"* - global switcher to turn off computers
    * *"katanaEnvironment"* - directory path to \*.bat file with defined resources (or just katanaBin.exe)
    * *"tasks"* - fill out this list with *"taskItemTemplate"* > \[ \{\...}, \{\...}, ... \] \('var' is optional and could be an empty dictionary\)
3. run "LocalQ.bat" on all computers
4. when job is done delete "history.json" and "log" folder


### Arguments for LocalQ.bat
**-shutdown**: keyword argument \(optional\) to turn off computer when the calculations were over \(depending on switch in settings.json file\)


### Required
python \*.\* \(used 3.7\)
