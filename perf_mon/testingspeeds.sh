#!/bin/zsh

speedtest --csv-header >> speedtest_results.csv
speedtest -–csv --secure >> speedtest_results.csv
