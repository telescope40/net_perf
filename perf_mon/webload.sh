#!/bin/zsh
TIME=$(date +%m%d_%H%M )
FILENAME="cnnresult.json"

echo Repeat All Test 5 times
for i in {1..50}; do
  echo Starting Cycle $i
  curl --insecure https://edition.cnn.com/ --output edition.json -w "{\"http_code\": %{http_code},\"url\": \"%{url_effective}\",\"time_connect\": \"%{time_connect}\",\"size_download\": %{size_download},\"speed_download\": %{speed_download},\"total_time\": %{time_total}}\n" >> $FILENAME
  if [ $i -ne 50 ]; then
    sleep 1m
  fi
done

