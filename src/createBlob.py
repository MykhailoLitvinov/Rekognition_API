import json
import boto3
import os

import uuid
from botocore.client import Config

s3_bucket = os.environ['S3_BUCKET']
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])


def createBlob(event, context):
    event_body = event.get("body")
    if not event_body:
        return {'statusCode': 404, 'body': json.dumps({"message": "Body is empty"})}

    body = json.loads(event_body)
    callback_url = body.get("callback_url")

    if not callback_url:
        return {'statusCode': 404, 'body': json.dumps({"message": "Callback_url is required"})}

    blob_id = str(uuid.uuid1())
    item = {
        "blob_id": blob_id,
        "callback_url": callback_url
    }

    table.put_item(Item=item)

    s3 = boto3.client('s3', config=Config(signature_version='s3v4'),
                      aws_access_key_id=os.environ['ACCESS_KEY'],
                      aws_secret_access_key=os.environ['SECRET_KEY'])

    upload_url = s3.generate_presigned_url(
        ClientMethod='put_object',
        Params={'Bucket': s3_bucket, 'Key': blob_id},
        ExpiresIn=3600)

    response = {
        'statusCode': 201,
        'body': json.dumps({
            'blob_id': blob_id,
            'callback_url': callback_url,
            'upload_url': upload_url
        })
    }
    return response
