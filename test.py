import json

with open('saves/test.txt', 'r') as test:
    data = json.load(test)
    print(type(data))
    data2 = json.loads(data)
    print(type(data2))
