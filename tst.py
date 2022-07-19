import json

with open('results.json') as file:
    con = json.load(file)

x = []

for el in con:
    if el['Result'] == 'BadTwitter':
        x.append(el['Name'])

x.sort()

print(x)