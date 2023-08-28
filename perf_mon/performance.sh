#!/bin/zsh


# Get Public IPs
TESTER="$1"
FILENAME=testing_results.json
echo Getting Public IP and Provider
IP="$(curl ip.me >&1)"
URL="https://ipapi.co/$IP/json"
PROVIDER="$(curl $URL | jq ".org")"
CITY="$(curl $URL | jq ".city")"
echo "Public IP is: "$IP > $FILENAME
echo "Provider: "$PROVIDER >> $FILENAME
echo "Located in:"$CITY >> $FILENAME

#Insert headers to CSV File
echo Starting Speedtest
speedtest --csv-header >> $FILENAME
speedtest --json --secure --simple >> $FILENAME
echo Ending Speedtest

echo Starting Webpage Downloads
echo CNN Download >> $FILENAME
echo http_code  speed_download  size_download  time_total  time_connect  time_appconnect time_starttransfer >> $FILENAME
curl https://edition.cnn.com/ --output edition.json -w "%{http_code} %{speed_download} %{size_download} %{time_total} %{time_connect} %{time_appconnect} %{time_starttransfer}\n" >> $FILENAME
echo Window File Download >> $FILENAME
curl https://gemmei.ftp.acc.umu.se/pub/gimp/gimp/v2.10/windows/gimp-2.10.32-setup-1.exe --output gimp.exe -w "%{http_code} %{speed_download} %{size_download} %{time_total} %{time_connect} %{time_appconnect} %{time_starttransfer}\n" >> $FILENAME
echo Completed Webpage Downloads

echo Starting download files from s3
echo US EAST >> $FILENAME
echo http_code  speed_download  size_download  time_total  time_connect  time_appconnect time_starttransfer >> $FILENAME
curl https://mrbucket-us-east-1.s3.amazonaws.com/s3object.txt/ --output s3object_us.txt -w "%{http_code} %{speed_download} %{size_download} %{time_total} %{time_connect} %{time_appconnect} %{time_starttransfer}\n" >> $FILENAME
echo EU WEST >> $FILENAME
#curl  https://mrbucket-eu-west-2.s3.amazonaws.com/s3object.txt/ --output s3object_us.txt -w  "%{http_code} %{speed_download} %{size_download} %{time_total} %{time_connect} %{time_appconnect} %{time_starttransfer}\n" >> $FILENAME
echo AP SOUTH >> $FILENAME
#curl  https://mrbucket-ap-southeast-1.s3.amazonaws.com/s3object.txt/ --output s3object_us.txt -w  "%{http_code} %{speed_download} %{size_download} %{time_total} %{time_connect} %{time_appconnect} %{time_starttransfer}\n" >> $FILENAME
echo Completed download files from s3


echo Create Upload File to test of 250MB
file_path="up250mbfile.txt"
if [[ ! -f "$file_path" ]]; then
    truncate -s 250MB "$file_path"
    echo "File created."
else
    echo "File already exists."
fi

echo Starting Upload File to s3
echo http_code  speed_download  size_download  time_total  time_connect  time_appconnect time_starttransfer >> $FILENAME
curl -X PUT -T  up250mbfile.txt https://mrbucket-us-east-1.s3.amazonaws.com/up250mbfile.txt -output $FILENAME -w "%{http_code} %{speed_download} %{size_download} %{time_total} %{time_connect} %{time_appconnect} %{time_starttransfer}\n" >> $FILENAME
#curl -X PUT -T  up250mbfile.txt https://mrbucket-eu-west-2.s3.amazonaws.com/up250mbfile.txt -output upload_perf.txt 2>upload_perf_$TESTER.txt
#curl -X PUT -T  up250mbfile.txt https://mrbucket-ap-southeast-1.s3.amazonaws.com/up250mbfile.txt -output upload_perf.txt 2>upload_perf_$TESTER.txt
echo Completed Upload File to s3

echo Google Search
echo Google Search for Pizza near $CITY >> $FILENAME
python3 ./search_google.py >> $FILENAME

# Combine all result files into tar

# Upload All Releveant Files to s3

