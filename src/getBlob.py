import json
import os

import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])


def getBlob(event, context):
    blob_id = event["pathParameters"]["blob_id"]

    response = table.get_item(Key={'blob_id': blob_id},
                              ProjectionExpression="blob_info")

    blob_info = response.get("Item")

    if not blob_info:
        return {'statusCode': 404, 'body': json.dumps({"message": "Blob not found"})}

    body = {
        "blob_id": blob_id,
        "blob_info": json.loads(blob_info.get('blob_info'))
    }
    return {'statusCode': 200, 'body': json.dumps(body)}
