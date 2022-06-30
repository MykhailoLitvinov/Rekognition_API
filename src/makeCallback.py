import requests

HEADERS = {'Content-Type': 'application/json'}


def makeCallback(event, context):
    try:
        for record in event.get('Records'):
            if record.get('eventName') != 'MODIFY':
                continue

            newImage = record.get('dynamodb').get('NewImage')
            blob_record = newImage.get('blob_info')

            if not blob_record:
                continue

            blob_info = blob_record.get('S')
            callback_url = newImage.get('callback_url').get('S')

            requests.post(url=callback_url, data=blob_info, headers=HEADERS)
    except Exception as e:
        return e
