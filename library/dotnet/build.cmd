cls
@echo off
cd /d %~dp0
dotnet publish -c Release -r win-x64 --self-contained --output ./lib/win.x64/ .\project\ERPro.NET.csproj
dotnet publish -c Release -r win-x86 --self-contained --output ./lib/win.x86/ .\project\ERPro.NET.csproj
dotnet publish -c Release -r linux-x64 --self-contained --output ./lib/linux.x64/ .\project\ERPro.NET.csproj
dotnet publish -c Release -r osx-x64 --self-contained --output ./lib/osx.x64/ .\project\ERPro.NET.csproj 
pause
:exit
