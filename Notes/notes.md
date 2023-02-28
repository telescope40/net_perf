
#### Import Yaml Files to Python Dictionary 
If you want to import yaml data into python 
You need to ensure the Loader is listed 

import yaml
with open('./path/filename.yml') as info:
      info_dict = yaml.load(info, Loader=yaml.FullLoader)
    print(info_dict)

***
#### Load a function from directory name Underlay
from Underlay.alldevices import data

for i in data:
    print(yaml.dump(yaml.load(i,  Loader=yaml.FullLoader),default_flow_style=False))

for i in data:
    print(yaml.dump(i))

### Import CSV to YAML 
### csv_yml.py
import csv
dict_from_csv = {}
with open('filename.csv', mode='r') as inp:
    reader = csv.reader(inp)
    headers = next(reader)[1:]
    for row in reader:
        dict_from_csv[row[0]] = {key : str(value) for key, value in zip(headers, row[1:])}
for key , value in dict_from_csv.items():
    print(key , value)
#print(dict_from_csv)



print(yaml.dump(yaml.load(document), default_flow_style=False))`
>> Result: `a: 1 b:   c: 3   d: 4`
