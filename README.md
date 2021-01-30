# inspection-firehose
Firehoseの学習

## 検証構成
Python → KDS → Firehose → S3

Python → KDS → Firehose → Lambda → S3

## ポイント

* Firehoseで出力するファイルサイズ  

* エラー時の動作


## 情報

### Firehose

* 出力先
  * S3の出力先を通常ルートとエラールートで指定可能
  * 出力先プレフィックスに日時の指定が可能(YYYY/MM/dd/HH)[参考](https://docs.aws.amazon.com/firehose/latest/dev/s3-prefixes.html)  
    指定しない場合は、一意の値がファイル名に含まれる

* 出力設定[参考](https://docs.aws.amazon.com/firehose/latest/dev/create-configure.html#buffer)  
  以下のどちらかに達するとファイルが作成される  
  * Bufferサイズ  
    1〜128 MiB
  * Buffer間隔  
    60~900s

* 出力ファイルの圧縮  
  * GZIP
  * Zip
  * Snappy

* エラー動作  
  エラーログをCloudWatchLogsに出力可能


### Lambda

設計図の`kinesis-firehose-process-record-python`から作成

```
from __future__ import print_function

import base64
import json as json2

def lambda_handler(event, context):
    output = []

    for record in event['records']:
        payload = base64.b64decode(record['data'])

        json_record = json2.loads(payload)
        json_record['status'] = 'processed'
        payload = json2.dumps(json_record)
        
        payload = payload + '\n'
        
        output_record = {
            'recordId': record['recordId'],
            'result': 'Ok',
            'data': base64.b64encode(payload)
        }

        output.append(output_record)

    return {'records': output}

```


## 検証メモ

### awscli docker
```
docker-compose up -d
docker exec -it development-aws /bin/bash
python ./app/stock.py
```



### KDS作成
```
aws kinesis create-stream --stream-name firehoseStream --shard-count 1
aws kinesis describe-stream --stream-name firehoseStream
```

### Firehose設定
  #### S3
  * Prefix  
    ```
    Firehose/no-processing/!{timestamp:yyyyMMdd}/file_!{timestamp:yyyyMMddHHmmss}_!{firehose:random-string}
    ```
  * Error prefix
    ```
    Firehose/error/processing/
    ```

### putレコード

```
{"accountId": "48Rl1ZxJOBxA", "geoPointId": "ASD", "eventUniqueKey": "12345678901234567890123456789012", "eventDiv": "1", "eventTime": "2020-10-18 19:12:21"}
```



# 検証まとめ


## Python → KDS → Firehose → S3

* デフォルトの設定だと改行コードが入らない。  
  ```
  {"record":"1"}{"record":"2"}{"record":"3"}
  ```
  以下のようになってほしい。。。
  ```
  {"record":"1"}
  {"record":"2"}
  {"record":"3"}
  ```

* ファイル名がUTCになっている？

出力ファイルはS3ディrクトリ参照


## filter検証
filterできるか検証  
`output_record`のdataを空にして返却することによって可能。  
他にも方法があるかも？  


#### pythonコード

accountIdが"123"のものだけにfilter
```
from __future__ import print_function

import base64
import json as json2

def lambda_handler(event, context):
    output = []

    for record in event['records']:
        payload = base64.b64decode(record['data'])
        print("start!!!")
        
        json_record = json2.loads(payload)
        print(json_record['accountId'])
        if json_record['accountId'] == '123':
            json_record['status'] = 'processed'
            payload = json2.dumps(json_record)
            payload = payload + '\n'
        
            output_record = {
                'recordId': record['recordId'],
                'result': 'Ok',
                'data': base64.b64encode(payload)
            }
        else:
            output_record = {
                'recordId': record['recordId'],
                'result': 'Ok',
                'data': ""
            }
        output.append(output_record)

    return {'records': output}

```


#### 流したデータ
stock_geo.pyを実行
```
{"accountId": "456", "geoPointId": "ASD", "eventUniqueKey": "12345678901234567890123456789012", "eventDiv": "0", "eventTime": "2021-01-30 17:38:07"}
{"accountId": "123", "geoPointId": "ASD", "eventUniqueKey": "12345678901234567890123456789012", "eventDiv": "0", "eventTime": "2021-01-30 17:38:08"}
{"accountId": "456", "geoPointId": "ASD", "eventUniqueKey": "12345678901234567890123456789012", "eventDiv": "0", "eventTime": "2021-01-30 17:38:09"}
{"accountId": "123", "geoPointId": "ASD", "eventUniqueKey": "12345678901234567890123456789012", "eventDiv": "0", "eventTime": "2021-01-30 17:38:10"}
{"accountId": "456", "geoPointId": "ASD", "eventUniqueKey": "12345678901234567890123456789012", "eventDiv": "0", 
```


#### 出力されたデータ
`s3/filter-test/file_20210130083525_KZGh33UsDLZfilter-test-2-2021-01-30-08-35-25-32dffac1-7abd-44cd-a619-b2e3b53b87bb`
```
{"status": "processed", "eventTime": "2021-01-30 17:35:25", "geoPointId": "ASD", "eventDiv": "1", "eventUniqueKey": "12345678901234567890123456789012", "accountId": "123"}
{"status": "processed", "eventTime": "2021-01-30 17:35:27", "geoPointId": "ASD", "eventDiv": "1", "eventUniqueKey": "12345678901234567890123456789012", "accountId": "123"}
{"status": "processed", "eventTime": "2021-01-30 17:35:29", "geoPointId": "ASD", "eventDiv": "1", "eventUniqueKey": "12345678901234567890123456789012", "accountId": "123"}
{"status": "processed", "eventTime": "2021-01-30 17:35:31", "geoPointId": "ASD", "eventDiv": "1", "eventUniqueKey": "12345678901234567890123456789012", "accountId": "123"}
{"status": "processed", "eventTime": "2021-01-30 17:35:33", "geoPointId": "ASD", "eventDiv": "1", "eventUniqueKey": "12345678901234567890123456789012", "accountId": "123"}
```



# Javaで動かしてみる


### Firehose設定
  #### S3
  * Prefix  
    ```
    Firehose/java-processing/!{timestamp:yyyyMMdd}/file_!{timestamp:yyyyMMddHHmmss}_!{firehose:random-string}
    ```
  * Error prefix
    ```
    Firehose/error/java-processing/
    ```

    