import json
import boto3
import random
import datetime
import time

# Stream名を指定
streamName = 'inputStream'

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
    data['accountId'] = '123'
    data['geoPointId'] = 'ASD'
    data['eventUniqueKey'] = '12345678901234567890123456789012'
    data['eventDiv'] = choise
    data['eventTime'] = str_now[0:19]
    return data
    
def getReferrer2():
    data = {}
    now = datetime.datetime.now()
    # str_now = now.isoformat()
    str_now = now.strftime("%Y-%m-%d %H:%M:%S.%L")
    choise = getChoise()
    data['accountId'] = '456'
    data['geoPointId'] = 'ASD'
    data['eventUniqueKey'] = '12345678901234567890123456789012'
    data['eventDiv'] = choise
    data['eventTime'] = str_now[0:19]
    return data

while True:
    data = json.dumps(getReferrer())
    print(data)
    kinesis.put_record(
    	StreamName=streamName,
        Data=data,
        PartitionKey="partitionkey")
    time.sleep(1)
    
    data2 = json.dumps(getReferrer2())
    print(data2)
    kinesis.put_record(
    	StreamName=streamName,
        Data=data2,
        PartitionKey="partitionkey")
    time.sleep(1)

