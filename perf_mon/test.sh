#!/bin/zsh
FILENAME=testing_results.csv
IP="$(curl ip.me >&1)"
URL="https://ipapi.co/$IP/csv"
curl $URL >> $FILENAME

INSTALLED="$(./program_installed.sh speedtest >&1)"
echo $INSTALLED
if [ "$INSTALLED" != False]; then 
  ./testingspeeds.sh
else
  ./installspeedMacOs.sh
fi


GOOGLEURL="https://www.googleapis.com/customsearch/v1"
API_KEY="AIzaSyDcBLSh58b82rNL-IGc1_c_14TxBr0nK-4"
CSE_ID="7073d4974aede489d"
QUERY="Best Pizza near me"
./search_google.sh $API_KEY $CSE_ID $QUERY
