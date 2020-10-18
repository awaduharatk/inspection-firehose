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
