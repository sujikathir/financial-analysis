import boto3
import json
import uuid
import os

def lambda_handler(event, context):
    # Initialize clients
    s3 = boto3.client('s3')
    dynamodb = boto3.client('dynamodb')
    
    path = event['path']
    method = event['httpMethod']
    
    if path == '/analyze' and method == 'POST':
        # Get presigned URL for S3 upload
        presigned_url = s3.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': os.environ['UPLOAD_BUCKET'],
                'Key': f'uploads/{uuid.uuid4()}'
            },
            ExpiresIn=3600
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({'uploadUrl': presigned_url})
        }
    
    elif path == '/status' and method == 'GET':
        # Check job status
        job_id = event['queryStringParameters']['jobId']
        
        response = dynamodb.get_item(
            TableName='FinancialReportJobs',
            Key={'JobId': {'S': job_id}}
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps(response['Item'])
        }