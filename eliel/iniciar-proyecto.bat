@echo off
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found. Installing...
    @"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
    choco install -y python3
)
call %~dp0\env\Scripts\activate
cd %~dp0\
pip install -r requirements.txt
start http://127.0.0.1:8000/
python manage.py runserver
cmd /k
