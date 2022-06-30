import json
import os

import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["DYNAMODB_TABLE"])


def getBlob(event, context):
    blob_id = event["pathParameters"]["blob_id"]

    response = table.get_item(Key={"blob_id": blob_id},
                              ProjectionExpression="labels")

    labels = response.get("Item")

    if not labels:
        return {"statusCode": 404, "body": json.dumps({"message": "Blob not found"})}

    body = {
        "blob_id": blob_id,
        "labels": json.loads(labels.get("labels"))
    }
    return {"statusCode": 200, "body": json.dumps(body)}
