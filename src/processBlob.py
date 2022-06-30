import json

import boto3
import os

bucket = os.environ['S3_BUCKET']
blobTable = os.environ['DYNAMODB_TABLE']
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])


def startBlob(event, context):

    blob_id = event['Records'][0]['s3']['object']['key']

    filesUploaded = event['Records']
    for file in filesUploaded:
        fileName = file['s3']['object']['key']
        rekognitionClient = boto3.client('rekognition')
        response = rekognitionClient.detect_labels(
            Image={
                'S3Object': {
                    'Bucket': bucket,
                    'Name': fileName}
            },
            MaxLabels=5
        )
        imageLabels = []

        for label in response['Labels']:
            imageLabels.append(label['Name'].lower())

        imageLabels_data = json.dumps(imageLabels)

        table.update_item(
            Key={'blob_id': blob_id},
            UpdateExpression='SET blob_info = :blob_info',
            ExpressionAttributeValues={
                ":blob_info": imageLabels_data
            }
        )
        return imageLabels
