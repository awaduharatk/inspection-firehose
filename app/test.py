import json as json2

data = '{"accountId": "48Rl1ZxJOBxA", "geoPointId": "ASD", "eventUniqueKey": "12345678901234567890123456789012", "eventDiv": "1", "eventTime": "2020-10-18 19:12:21"}'

json = json2.loads(data)

json['test'] = 'aaa'

new = json2.dumps(json)

print(json)
