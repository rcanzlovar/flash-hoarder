# makejson.py = create the stub of the file 
import json


data = {}
data['settings'] = {}
data['settings']['batch'] = 20
data['settings']['keywords'] = 'cheney'
data['settings']['dbname'] = 'example.db'


with open('settings.json', 'w') as outfile:
    json.dump(data, outfile)