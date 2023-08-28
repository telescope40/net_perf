#!/bin/zsh
#Download speedtest
#MacOs
curl -o speedtest-macos.tgz "https://install.speedtest.net/app/cli/ookla-speedtest-1.0.0-macos-x86_64.tgz"
tar xf speedtest-macos.tgz
sudo mv speedtest /usr/local/bin/
sudo chmod +x /usr/local/bin/speedtest
speedtest --accept-license
