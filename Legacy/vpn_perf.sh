#!/bin/zsh

# Define File Names with Region & Time Document City in Perf File

FILENAME="PerfResults.json"
SELECTED_SPEEDRESULTS="Selected_SpeedtestReport.json"
DEFAULT_SPEEDRESULTS="Default_SpeedtestReport.json"
SPEEDIMAGE="Speedtest_Graph.png"

echo Getting Closest Speedtest Server
STS="$(speedtest --list  | sed -n '2p' | awk -F')' '{print $1}')"


echo Repeat All Test 5 times
for i in {1..3}; do
  echo Starting Cycle $i
  echo Starting Speedtest to default  >> $DEFAULT_SPEEDRESULTS
  speedtest --simple --json  >> $DEFAULT_SPEEDRESULTS
  sleep 60s
  echo Starting Speedtest to server number $STS >> $SELECTED_SPEEDRESULTS
  speedtest --simple --json --server $STS  >> $SELECTED_SPEEDRESULTS
  echo Ending Cycle $i
  if [ $i -ne 3 ]; then
    sleep 1m
  fi
done

#echo Plot Speedtest into Graph
#python3 ./stplot.py $SPEEDRESULTS
#sleep 1m



#for i in {1..2}; do
#  echo Starting Cycle $i
#  python3 ping_script.py
#  if [ $i -ne 5 ]; then
#    sleep 1m
#  fi
#done


