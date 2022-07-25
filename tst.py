import json
import codecs

with open('names.txt', encoding='utf-8') as file:
    con = file.readlines()

s = []

for el in con:
    s.append(el.strip())

with open('test.json', 'w', encoding='utf-8') as file_w:
    json.dump(s, file_w, indent=4, ensure_ascii=False)