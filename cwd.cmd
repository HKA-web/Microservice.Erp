cls
@echo off
cd /d %~dp0
:setup
set path=%path%;%~dp0bin\gettext\bin\
set path=%path%;%~dp0bin\redis\
set path=%path%;%~dp0bin\ffmpeg\bin\
set path=%path%;%~dp0bin\wkhtmltopdf\bin\
set path=%path%;%~dp0bin\nodejs\
set path=%path%;%~dp0bin\git\bin\
set path=%path%;%~dp0bin\cargo\bin\
set path=%path%;%~dp0bin\erlang\bin\
set path=%path%;%~dp0bin\rabbitmq\bin\
set path=%path%;%~dp0bin\zip\
if exist %~dp0env ( goto :activate ) else (
	echo Virtual env do not exists. Run virtualenv env first
	echo.
	goto :cmd
)
:activate
call %~dp0env\scripts\activate.bat
if [%~1]==[] goto :cmd
if [%~1]==[-m] goto :module
if [%~1]==[clean] goto :clean
:manage
setlocal enabledelayedexpansion
set argument=manage.py
goto :cwd
:module
setlocal enabledelayedexpansion
set argument=
goto :cwd
:cwd
for %%a in (%*) do set argument=!argument! %%a
echo Run : python -Xutf8 %argument%
python -Xutf8 %argument%
goto :exit
:clean
echo Management command to clean .pyc files and __pycache__ directories
pyclean .
goto :exit
:cmd
cmd
goto :exit
:exit
