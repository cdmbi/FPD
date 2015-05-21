'''convert data in csv format to json file'''

import csv
import json
import sys

csvfile = open(sys.argv[1])

fieldnames = csvfile.readline().strip('\n').split(',')
reader = csv.DictReader(csvfile, fieldnames)
data = []
for row in reader:
    data.append(row)

json.dump(data, sys.stdout, indent=4)
