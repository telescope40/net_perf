
#wget https://install.speedtest.net/app/cli/ookla-speedtest-1.2.0-macosx-universal.tgz
# Windows via Powershell
@echo off
REM Create a temporary directory
if not exist "C:\temp" mkdir "C:\temp"

REM Download the Speedtest CLI
powershell -command "Invoke-WebRequest -Uri 'https://install.speedtest.net/app/cli/ookla-speedtest-1.0.0-win64.zip' -OutFile 'C:\temp\speedtest-cli.zip'"

REM Extract the downloaded ZIP file
powershell -command "Expand-Archive -Path 'C:\temp\speedtest-cli.zip' -DestinationPath 'C:\temp\speedtest-cli'"

REM Move the speedtest.exe to Program Files
move /Y "C:\temp\speedtest-cli\speedtest.exe" "C:\Program Files\speedtest.exe"

REM Add the Speedtest CLI to system PATH
setx PATH "%PATH%;C:\Program Files"

REM Accept the license and run Speedtest to confirm installation
"C:\Program Files\speedtest.exe" --accept-license

REM Optionally, clean up the temporary files
del "C:\temp\speedtest-cli.zip"
rmdir /S /Q "C:\temp\speedtest-cli"
