# Louis DeVictoria
# create a dictinonary structure frome csv
import csv

dict_from_csv = {}

with open('spine.csv', mode='r') as inp:
    reader = csv.reader(inp)
    headers = next(reader)[1:]
    for row in reader:
        dict_from_csv[row[0]] = {key : str(value) for key, value in zip(headers, row[1:])}

for key , value in dict_from_csv.items():
    print(key , value)
#print(dict_from_csv)
