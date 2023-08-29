#!/bin/zsh

# Get Public IPs
# Install brew
# brew install speedtest-cli
# brew install coreuitils
# Install Speedtest
# Install jq
# pip3 install requests


echo Getting Public IP and Provider
IP="$(curl --insecure ip.me >&1)"
URL="https://ipapi.co/$IP/json"
PROVIDER="$(curl --insecure $URL | jq -r ".org")"
CITY="$(curl --insecure $URL | jq -r ".city")"
FILENAME=$CITY"_Report.json"
SPEEDRESULTS=$CITY"_Speedtest.json"
echo "Public IP is: "$IP > $FILENAME
echo "Provider: "$PROVIDER >> $FILENAME
echo "Located in:"$CITY >> $FILENAME

echo Getting Closest Speedtest Server
STS="$(speedtest --list | head -2 | cut -d ")" -f1)"
echo Starting Speedtest to server number $STS
speedtest --simple --json >> $FILENAME
sleep 1m
for i in {1..10}; do
  speedtest --json >> $SPEEDRESULTS
  if [ $i -ne 10 ]; then
    sleep 2m
  fi
done
echo Ending Speedtest

echo Starting Webpage Downloads
echo CNN Download >> $FILENAME
echo http_code  speed_download  size_download  time_total  time_connect  time_appconnect time_starttransfer >> $FILENAME
curl --insecure https://edition.cnn.com/ --output edition.json -w "%{http_code} %{speed_download} %{size_download} %{time_total} %{time_connect} %{time_appconnect} %{time_starttransfer}\n" >> $FILENAME
sleep 1m
echo Window File Download >> $FILENAME
curl --insecure  https://gemmei.ftp.acc.umu.se/pub/gimp/gimp/v2.10/windows/gimp-2.10.32-setup-1.exe --output gimp.exe -w "%{http_code} %{speed_download} %{size_download} %{time_total} %{time_connect} %{time_appconnect} %{time_starttransfer}\n" >> $FILENAME
echo Completed Webpage Downloads

echo Starting download files from s3 250MB File
echo US EAST Download 250MB File >> $FILENAME
echo http_code  speed_download  size_download  time_total  time_connect  time_appconnect time_starttransfer >> $FILENAME
curl --insecure https://mrbucket-us-east-1.s3.amazonaws.com/s3object.txt --output s3object_us.txt -w "%{http_code} %{speed_download} %{size_download} %{time_total} %{time_connect} %{time_appconnect} %{time_starttransfer}\n" >> $FILENAME
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
curl -X PUT -T  up250mbfile.txt https://mrbucket-us-east-1.s3.amazonaws.com/up250mbfile.txt -output $FILENAME -w "%{http_code} %{speed_download} %{size_download} %{time_total} %{time_connect} %{time_appconnect} %{time_starttransfer}\n" >> $FILENAME
#curl -X PUT -T  up250mbfile.txt https://mrbucket-eu-west-2.s3.amazonaws.com/up250mbfile.txt -output $FILENAME -w "%{http_code} %{speed_download} %{size_download} %{time_total} %{time_connect} %{time_appconnect} %{time_starttransfer}\n" >> $FILENAME
#curl -X PUT -T  up250mbfile.txt https://mrbucket-ap-southeast-1.s3.amazonaws.com/up250mbfile.txt -output $FILENAME -w "%{http_code} %{speed_download} %{size_download} %{time_total} %{time_connect} %{time_appconnect} %{time_starttransfer}\n" >> $FILENAME
echo Completed Upload File to s3
sleep 30s

echo Google Search
echo Google Search for Pizza near $CITY >> $FILENAME
python3 ./search_google.py >> $FILENAME

echo Upload Results to bucket
echo Upload Results to bucket >> $FILENAME
curl -X PUT -T $FILENAME https://mrbucket-us-east-1.s3.amazonaws.com/$FILENAME -output finalpush
curl -X PUT -T $SPEEDRESULTS https://mrbucket-us-east-1.s3.amazonaws.com/$SPEEDRESULTS -output finalpush

