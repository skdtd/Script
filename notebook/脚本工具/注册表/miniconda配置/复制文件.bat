@echo off
SET PSConfigFile=.\Microsoft.PowerShell_profile.ps1
SET PipFile=.\pip.ini
SET CondaFile=.\.condarc
SET PSGenFile=%HOMEPATH%\Documents\WindowsPowerShell
SET PipGenFile=%HOMEPATH%\pip
if not exist %PSConfigFile% (
	md %PSConfigFile%
)
if not exist %PipGenFile% (
	md %PipGenFile%
)
copy %PSConfigFile% %PSConfigFile%\Microsoft.PowerShell_profile.ps1
copy %PipFile% %PipGenFile%\pip.ini
copy %CondaFile% %HOMEPATH%\.condarc
pause