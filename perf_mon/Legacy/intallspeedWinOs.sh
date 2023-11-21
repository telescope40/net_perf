
#wget https://install.speedtest.net/app/cli/ookla-speedtest-1.2.0-macosx-universal.tgz
# Windows via Powershell
New-Item -Path C:\temp -ItemType Directory -Force
Set-Location C:\temp
Invoke-WebRequest -Uri "https://install.speedtest.net/app/cli/ookla-speedtest-1.0.0-win64.zip" -OutFile "speedtest-cli.zip"
Expand-Archive -Path "speedtest-cli.zip" -DestinationPath "C:\temp\speedtest-cli"
Move-Item -Path "C:\temp\speedtest-cli\speedtest.exe" -Destination "C:\Program Files\speedtest.exe"
$env:Path += ";C:\Program Files"
& "C:\Program Files\speedtest.exe" --accept-license
#https://install.speedtest.net/app/cli/ookla-speedtest-1.2.0-win64.zip
