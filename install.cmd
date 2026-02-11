@echo off
set "params=%*"
cd /d "%~dp0" && ( if exist "%temp%\getadmin.vbs" del "%temp%\getadmin.vbs" ) && fsutil dirty query %systemdrive% 1>nul 2>nul || (  echo Set UAC = CreateObject^("Shell.Application"^) : UAC.ShellExecute "cmd.exe", "/k cd ""%~sdp0"" && %~s0 %params%", "", "runas", 1 >> "%temp%\getadmin.vbs" && "%temp%\getadmin.vbs" && exit /B )

if /i "%PROCESSOR_ARCHITECTURE%" equ "X86" (
if /i "%PROCESSOR_ARCHITEW6432%" equ "AMD64" (
set OSARCH=x64
echo This is a 64-bit architecture running in 32-bit mode.
) else (
set OSARCH=x86
echo This is a 32-bit architecture running in 32-bit mode.
)
) else (
set OSARCH=x64
echo This is a 64-bit architecture running in 64-bit mode.
)
if [%~1]==[] goto :cmd
if [%~1]==[-m] goto :manual
if [%~1]==[-a] goto :automatic
echo
:manual
set /p APPLICATION="Enter Application To Install (like: Redis, Huey, Interface, WhatsApp.Api, etc...): "
set /p UNIQUE="Enter %APPLICATION% Unique Identifier (like: SNI, NUSA, NBI, CNI, NJRM, NMI, PNJ, ANJ, etc...): "
choice /C:YN /M:"Initial and replace old service ?? [YN]"
if errorlevel ==1 goto :processmanual
if errorlevel ==2 goto :exit
echo
:processmanual
echo bin\service\%OSARCH%\service remove %UNIQUE%.%APPLICATION% confirm
bin\service\%OSARCH%\service remove %UNIQUE%.%APPLICATION% confirm
bin\service\%OSARCH%\service install %UNIQUE%.%APPLICATION% %~dp0cwd.cmd
bin\service\%OSARCH%\service set %UNIQUE%.%APPLICATION% AppDirectory %~dp0
bin\service\%OSARCH%\service set %UNIQUE%.%APPLICATION% DisplayName %UNIQUE%.%APPLICATION%.Service
bin\service\%OSARCH%\service set %UNIQUE%.%APPLICATION% Description "Management Schedular %UNIQUE%.%APPLICATION%"
bin\service\%OSARCH%\service set %UNIQUE%.%APPLICATION% AppStdout "%~dp0data\log\%UNIQUE%.%APPLICATION%.Output.log"
bin\service\%OSARCH%\service set %UNIQUE%.%APPLICATION% AppStderr "%~dp0data\log\%UNIQUE%.%APPLICATION%.Error.log"
bin\service\%OSARCH%\service set %UNIQUE%.%APPLICATION% AppStdoutCreationDisposition 1
bin\service\%OSARCH%\service set %UNIQUE%.%APPLICATION% AppStderrCreationDisposition 1
echo Edit And Correct Manual %UNIQUE%.%APPLICATION%
bin\service\%OSARCH%\service edit %UNIQUE%.%APPLICATION%
choice /C:YN /M:"Initial other service ?? [YN]"
if errorlevel ==1 goto :manual
if errorlevel ==2 goto :exit
echo
:automatic
set APPLICATION=ERPro
set /p UNIQUE="Enter %APPLICATION% Unique Identifier (like: SNI, NUSA, NBI, CNI, NJRM, NMI, PNJ, ANJ, etc...): "
set APPLICATION=Redis
bin\service\%OSARCH%\service remove %UNIQUE%.%APPLICATION% confirm
bin\service\%OSARCH%\service install %UNIQUE%.%APPLICATION% %~dp0cwd.cmd
bin\service\%OSARCH%\service set %UNIQUE%.%APPLICATION% AppDirectory %~dp0
bin\service\%OSARCH%\service set %UNIQUE%.%APPLICATION% AppParameters runredis
bin\service\%OSARCH%\service set %UNIQUE%.%APPLICATION% DisplayName %UNIQUE%.%APPLICATION%.Service
bin\service\%OSARCH%\service set %UNIQUE%.%APPLICATION% Description "Management Schedular %UNIQUE%.%APPLICATION%"
bin\service\%OSARCH%\service set %UNIQUE%.%APPLICATION% AppStdout "%~dp0data\log\%UNIQUE%.%APPLICATION%.Output.log"
bin\service\%OSARCH%\service set %UNIQUE%.%APPLICATION% AppStderr "%~dp0data\log\%UNIQUE%.%APPLICATION%.Error.log"
bin\service\%OSARCH%\service set %UNIQUE%.%APPLICATION% AppStdoutCreationDisposition 1
bin\service\%OSARCH%\service set %UNIQUE%.%APPLICATION% AppStderrCreationDisposition 1
echo Edit And Correct Manual %UNIQUE%.%APPLICATION%
bin\service\%OSARCH%\service edit %UNIQUE%.%APPLICATION%
set APPLICATION=Huey
bin\service\%OSARCH%\service remove %UNIQUE%.%APPLICATION% confirm
bin\service\%OSARCH%\service install %UNIQUE%.%APPLICATION% %~dp0cwd.cmd
bin\service\%OSARCH%\service set %UNIQUE%.%APPLICATION% AppDirectory %~dp0
bin\service\%OSARCH%\service set %UNIQUE%.%APPLICATION% AppParameters runhuey
bin\service\%OSARCH%\service set %UNIQUE%.%APPLICATION% DisplayName %UNIQUE%.%APPLICATION%.Service
bin\service\%OSARCH%\service set %UNIQUE%.%APPLICATION% Description "Management Schedular %UNIQUE%.%APPLICATION%"
bin\service\%OSARCH%\service set %UNIQUE%.%APPLICATION% DependOnService %UNIQUE%.Redis
bin\service\%OSARCH%\service set %UNIQUE%.%APPLICATION% AppStdout "%~dp0data\log\%UNIQUE%.%APPLICATION%.Output.log"
bin\service\%OSARCH%\service set %UNIQUE%.%APPLICATION% AppStderr "%~dp0data\log\%UNIQUE%.%APPLICATION%.Error.log"
bin\service\%OSARCH%\service set %UNIQUE%.%APPLICATION% AppStdoutCreationDisposition 1
bin\service\%OSARCH%\service set %UNIQUE%.%APPLICATION% AppStderrCreationDisposition 1
echo Edit And Correct Manual %UNIQUE%.%APPLICATION%
bin\service\%OSARCH%\service edit %UNIQUE%.%APPLICATION%
set APPLICATION=Interface
bin\service\%OSARCH%\service remove %UNIQUE%.%APPLICATION% confirm
bin\service\%OSARCH%\service install %UNIQUE%.%APPLICATION% %~dp0cwd.cmd
bin\service\%OSARCH%\service set %UNIQUE%.%APPLICATION% AppDirectory %~dp0
bin\service\%OSARCH%\service set %UNIQUE%.%APPLICATION% AppParameters rundaphne
bin\service\%OSARCH%\service set %UNIQUE%.%APPLICATION% DisplayName %UNIQUE%.%APPLICATION%.Service
bin\service\%OSARCH%\service set %UNIQUE%.%APPLICATION% Description "Management Schedular %UNIQUE%.%APPLICATION%"
bin\service\%OSARCH%\service set %UNIQUE%.%APPLICATION% DependOnService %UNIQUE%.Huey
bin\service\%OSARCH%\service set %UNIQUE%.%APPLICATION% AppStdout "%~dp0data\log\%UNIQUE%.%APPLICATION%.Output.log"
bin\service\%OSARCH%\service set %UNIQUE%.%APPLICATION% AppStderr "%~dp0data\log\%UNIQUE%.%APPLICATION%.Error.log"
bin\service\%OSARCH%\service set %UNIQUE%.%APPLICATION% AppStdoutCreationDisposition 1
bin\service\%OSARCH%\service set %UNIQUE%.%APPLICATION% AppStderrCreationDisposition 1
echo Edit And Correct Manual %UNIQUE%.%APPLICATION%
bin\service\%OSARCH%\service edit %UNIQUE%.%APPLICATION%
set APPLICATION=WhatsApp.Api
bin\service\%OSARCH%\service remove %UNIQUE%.%APPLICATION% confirm
bin\service\%OSARCH%\service install %UNIQUE%.%APPLICATION% %~dp0cwd.cmd
bin\service\%OSARCH%\service set %UNIQUE%.%APPLICATION% AppDirectory %~dp0
bin\service\%OSARCH%\service set %UNIQUE%.%APPLICATION% AppParameters runwhatsapp
bin\service\%OSARCH%\service set %UNIQUE%.%APPLICATION% DisplayName %UNIQUE%.%APPLICATION%.Service
bin\service\%OSARCH%\service set %UNIQUE%.%APPLICATION% Description "Management Schedular %UNIQUE%.%APPLICATION%"
bin\service\%OSARCH%\service set %UNIQUE%.%APPLICATION% DependOnService %UNIQUE%.Interface
bin\service\%OSARCH%\service set %UNIQUE%.%APPLICATION% AppStdout "%~dp0data\log\%UNIQUE%.%APPLICATION%.Output.log"
bin\service\%OSARCH%\service set %UNIQUE%.%APPLICATION% AppStderr "%~dp0data\log\%UNIQUE%.%APPLICATION%.Error.log"
bin\service\%OSARCH%\service set %UNIQUE%.%APPLICATION% AppStdoutCreationDisposition 1
bin\service\%OSARCH%\service set %UNIQUE%.%APPLICATION% AppStderrCreationDisposition 1
echo Edit And Correct Manual %UNIQUE%.%APPLICATION%
bin\service\%OSARCH%\service edit %UNIQUE%.%APPLICATION%
goto :exit
:cmd
cmd
:exit
pause
