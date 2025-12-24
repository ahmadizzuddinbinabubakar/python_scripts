import csv
import json
import os

def make_json(csvFilePath, jsonFilePath):

    if os.path.exists(csvFilePath):
        with open(csvFilePath, encoding="utf8", newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            data = [row for row in reader]
    print("read csv ok")

    with open(jsonFilePath, 'w') as jsonfile:
            json.dump(data, jsonfile)
    print("convert to json ok")
# Decide the two file paths according to your 
# computer system
fileNamePrefix = '<fileNamePrefix>'
fileName = '<fileName>'
csvFilePath = '<csvFilePath>' + fileNamePrefix + fileName + '.csv'
jsonFilePath = '<jsonFilePath>' +fileName+ '.json'

# Call the make_json function
make_json(csvFilePath, jsonFilePath)
