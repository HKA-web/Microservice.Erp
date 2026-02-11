cls
@echo off
cd /d %~dp0
set /p version="Enter Version To Update: "
cd %~dp0%version%
git fetch
git reset --hard origin/master
xcopy %~dp0%version%\*.exe %~dp0 /c /i /e /h /y
pause
