@echo off
SET SourceFile=.\Microsoft.PowerShell_profile.ps1
SET GenFile=%HOMEPATH%\Documents\WindowsPowerShell
 
if not exist %GenFile% (
	md %GenFile%
)

copy %SourceFile% %GenFile%\Microsoft.PowerShell_profile.ps1