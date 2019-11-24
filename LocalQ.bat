
:: HELP
::
:: 1. share directory that this file is located
:: 2. fill out settings.json
:: 3. run "LocalQ.bat" on all computers
:: 4. when job is done run "_clean_.py"


:: INPUT ARGUMENTS
::
:: -shutdown      - turn off computer when job is done
::                  (depending on switch in settings.json file)


:: REQUIRED
::
:: python *.* (used 3.7)



@ECHO OFF



:: check setting for typos and any other errors
CALL python "%~dp0check_settings.py" > SettingsState
SET /p SETTINGS_STATE=<SettingsState
DEL SettingsState

:: stop programm if settings isn't valid
IF "%SETTINGS_STATE%" NEQ "VALID SETTINGS" EXIT



:LOOP
SETLOCAL


:: get command to run "Katana" in batch mode
CALL python "%~dp0get_task.py" > KatanaCommand
SET /p KATANA_COMMAND=<KatanaCommand
DEL KatanaCommand

:: if there is no task then go to the exit
IF "%KATANA_COMMAND%" == "" GOTO DOOR



:: create log file to write rendering process output messages
CALL python "%~dp0unique_log.py" "%KATANA_COMMAND%" > LogPath
SET /p LOG=<LogPath
DEL LogPath


:: run calculations
:: check for errors and update task state
CALL %KATANA_COMMAND% >> "%LOG%" 2>&1
CALL python "%~dp0update_state.py" "%LOG%" "%KATANA_COMMAND%"


:: go to the beginning and get a new task
ENDLOCAL
GOTO LOOP




:DOOR
ENDLOCAL


:: turn off computer
SETLOCAL

CALL python "%~dp0shutdown_request.py" %* > ShutdownCommand
SET /p SHUTDOUWN_COMMAND=<ShutdownCommand
DEL ShutdownCommand
CALL %SHUTDOUWN_COMMAND%

ENDLOCAL
