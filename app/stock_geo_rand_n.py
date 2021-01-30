import json
import boto3
import random
import datetime
import time
import string

# Stream名を指定
streamName = 'test'

kinesis = boto3.client('kinesis')

def getChoise():
    now = datetime.datetime.now()
    str_now = now.strftime("%Y-%m-%d %H:%M:%S.%L")
    str_new = str_now[15:16]
    while True:
        if (int(str_new) % 2) == 0:
            return '0'
        else:
            return '1'

def getReferrer():
    data = {}
    now = datetime.datetime.now()
    str_now = now.strftime("%Y-%m-%d %H:%M:%S.%L")
    choise = getChoise()
    data['accountId'] = randomname(12)
    data['geoPointId'] = 'ASD'
    data['eventUniqueKey'] = '12345678901234567890123456789012'
    data['eventDiv'] = '1'
    data['eventTime'] = str_now[0:19]
    return data
    
def getReferrer2():
    data = {}
    now = datetime.datetime.now()
    # str_now = now.isoformat()
    str_now = now.strftime("%Y-%m-%d %H:%M:%S.%L")
    choise = getChoise()
    data['accountId'] = randomname(12)
    data['geoPointId'] = 'ASD'
    data['eventUniqueKey'] = '12345678901234567890123456789012'
    data['eventDiv'] = '1'
    data['eventTime'] = str_now[0:19]
    return data

def randomname(n):
   return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

while True:
    data = json.dumps(getReferrer())
    # print(data)
    data = data + '\n'
    kinesis.put_record(
    	StreamName=streamName,
        Data=data,
        PartitionKey="partitionkey")
    # time.sleep(1)
    
    data2 = json.dumps(getReferrer2())
    # print(data2)
    data2 = data2 + '\n'
    kinesis.put_record(
    	StreamName=streamName,
        Data=data2,
        PartitionKey="partitionkey")
    # time.sleep(1)

