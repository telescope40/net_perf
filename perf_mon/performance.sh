#!/bin/zsh

# Get Public IPs
# Install brew
# brew install speedtest-cli
# brew install coreuitils
# Install Speedtest
# Install jq
# pip3 install requests
# pip3 install json
# pip3 install sys
# import matplotlib.pyplot as plt


echo Getting Public IP and Provider
IP="$(curl --insecure ip.me >&1)"
URL="https://ipapi.co/$IP/json"
PROVIDER="$(curl --insecure $URL | jq -r ".org")"
CITY="$(curl --insecure $URL | jq -r ".city")"
FILENAME=$CITY"_Report.json"
SPEEDRESULTS=$CITY"_Speedtest.json"
WEBPAGELOAD="cnn_load.json"
MSFILEDOWN="ms_dl.json"
S3UPLOAD="s3upload.json"
S3DOWNLOAD="s3download.json"
SPEEDIMAGE=$CITY"_speedtest.png"
echo "Public IP is: "$IP > $FILENAME
echo "Provider: "$PROVIDER >> $FILENAME
echo "Located in:"$CITY >> $FILENAME

echo Getting Closest Speedtest Server
STS="$(speedtest --list | head -2 | cut -d ")" -f1)"
echo Starting Speedtest to server number $STS
speedtest --simple --json >> $FILENAME
sleep 1m
echo Ending Speedtest

echo Starting Webpage Downloads
echo CNN Download >> $FILENAME
echo http_code  speed_download  size_download  time_total  time_connect  time_appconnect time_starttransfer >> $FILENAME
curl --insecure https://edition.cnn.com/ --output edition.json -w "{\n\
  \"http_code\": %{http_code},\n\
  \"url\": \"%{url_effective}\",\n\
  \"size_download\": %{size_download},\n\
  \"speed_download\": %{speed_download}\n\
  \"total_time\": %{time_total},\n\
}\n" >> $FILENAME
sleep 1m
echo Window File Download >> $FILENAME
curl --insecure  https://gemmei.ftp.acc.umu.se/pub/gimp/gimp/v2.10/windows/gimp-2.10.32-setup-1.exe --output gimp.exe -w "{\n\
  \"http_code\": %{http_code},\n\
  \"url\": \"%{url_effective}\",\n\
  \"size_download\": %{size_download},\n\
  \"speed_download\": %{speed_download}\n\
  \"total_time\": %{time_total},\n\
}\n" >> $FILENAME
echo Completed Webpage Downloads

echo Starting download files from s3 250MB File
echo US EAST Download 250MB File >> $FILENAME
echo http_code  speed_download  size_download  time_total  time_connect  time_appconnect time_starttransfer >> $FILENAME
curl --insecure https://mrbucket-us-east-1.s3.amazonaws.com/s3object.txt --output s3object_us.txt -w "{\n\
  \"http_code\": %{http_code},\n\
  \"url\": \"%{url_effective}\",\n\
  \"size_download\": %{size_download},\n\
  \"speed_download\": %{speed_download}\n\
  \"total_time\": %{time_total},\n\
}\n" >> $FILENAME
echo EU WEST >> $FILENAME
#curl  --insecure https://mrbucket-eu-west-2.s3.amazonaws.com/s3object.txt --output s3object_us.txt -w  "%{http_code} %{speed_download} %{size_download} %{time_total} %{time_connect} %{time_appconnect} %{time_starttransfer}\n" >> $FILENAME
echo AP SOUTH >> $FILENAME
#curl  --insecure https://mrbucket-ap-southeast-1.s3.amazonaws.com/s3object.txt --output s3object_us.txt -w  "%{http_code} %{speed_download} %{size_download} %{time_total} %{time_connect} %{time_appconnect} %{time_starttransfer}\n" >> $FILENAME
echo Completed download files from s3


echo Create Upload File to test of 250MB
file_path="up250mbfile.txt"
if [[ ! -f "$file_path" ]]; then
    truncate -s 250MB "$file_path"
    echo "File created."
else
    echo "File already exists."
fi

echo Starting Upload File to s3 250MB File
echo http_code  speed_download  size_download  time_total  time_connect  time_appconnect time_starttransfer >> $FILENAME
echo US EAST Upload 250MB File >> $FILENAME
curl -X PUT -T  up250mbfile.txt https://mrbucket-us-east-1.s3.amazonaws.com/up250mbfile.txt -output $FILENAME  -w "{\n\
  \"http_code\": %{http_code},\n\
  \"url\": \"%{url_effective}\",\n\
  \"size_upload\": %{size_upload},\n\
  \"speed_download\": %{speed_upload}\n\
  \"total_time\": %{time_total},\n\
}\n" >> $FILENAME
#curl -X PUT -T  up250mbfile.txt https://mrbucket-eu-west-2.s3.amazonaws.com/up250mbfile.txt -output $FILENAME -w "%{http_code} %{speed_download} %{size_download} %{time_total} %{time_connect} %{time_appconnect} %{time_starttransfer}\n" >> $FILENAME
#curl -X PUT -T  up250mbfile.txt https://mrbucket-ap-southeast-1.s3.amazonaws.com/up250mbfile.txt -output $FILENAME -w "%{http_code} %{speed_download} %{size_download} %{time_total} %{time_connect} %{time_appconnect} %{time_starttransfer}\n" >> $FILENAME
echo Completed Upload File to s3
sleep 30s

echo Repeat All Test 5 times
for i in {1..5}; do
  echo Starting Cycle $i
  speedtest --json > $SPEEDRESULTS
  sleep 10s
  curl --insecure https://edition.cnn.com/ --output edition.json -w "{\"http_code\": %{http_code},\"url\": \"%{url_effective}\",\"size_download\": %{size_download},\"speed_download\": %{speed_download},\"total_time\": %{time_total}}\n" >> $WEBPAGELOAD
  sleep 10s
  curl --insecure  https://gemmei.ftp.acc.umu.se/pub/gimp/gimp/v2.10/windows/gimp-2.10.32-setup-1.exe --output gimp.exe -w "{\"http_code\": %{http_code},\"url\": \"%{url_effective}\",\"size_download\": %{size_download},\"speed_download\": %{speed_download},\"total_time\": %{time_total}}\n" >> $MSFILEDOWN
  sleep 10s
  curl -X PUT -T up250mbfile.txt https://mrbucket-us-east-1.s3.amazonaws.com/up250mbfile.txt --output up250mbfile.txt -w "{\"http_code\": %{http_code},\"url\": \"%{url_effective}\",\"size_upload\": %{size_upload},\"speed_download\": %{speed_upload},\"total_time\": %{time_total}}\n" >> $S3UPLOAD
  sleep 10s
  curl --insecure https://mrbucket-us-east-1.s3.amazonaws.com/s3object.txt --output s3object_us.txt -w "{\"http_code\": %{http_code},\"url\": \"%{url_effective}\",\"size_download\": %{size_download},\"speed_download\": %{speed_download},\"total_time\": %{time_total}}\n" >> $S3DOWNLOAD
  echo Ending Cycle $i
  if [ $i -ne 5 ]; then
    sleep 1m
  fi
done

echo Google Search for Pizza near $CITY
echo Google Search for Pizza near $CITY >> $FILENAME
python3 ./search_google.py >> $FILENAME
sleep 1m
echo Plot Speedtest into Graph
python3 ./stpar.py $SPEEDRESULTS

echo Upload Results to bucket
echo Upload Results to bucket >> $FILENAME
curl -X PUT -T $FILENAME https://mrbucket-us-east-1.s3.amazonaws.com/results/$FILENAME
curl -X PUT -T $SPEEDRESULTS https://mrbucket-us-east-1.s3.amazonaws.com/results/$SPEEDRESULTS
curl -X PUT -T speedtest_graph.png https://mrbucket-us-east-1.s3.amazonaws.com/results/$SPEEDIMAGE

echo Clean Up Directory
rm -rf gimp.exe
rm -rf edition.json

