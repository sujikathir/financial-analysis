import boto3
import json
from datetime import datetime

def lambda_handler(event, context):
    # Extract S3 event details
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    # Initialize clients
    textract = boto3.client('textract')
    dynamodb = boto3.client('dynamodb')
    sqs = boto3.client('sqs')
    
    # Extract text using Textract
    textract_response = textract.start_document_text_detection(
        DocumentLocation={'S3Object': {'Bucket': bucket, 'Name': key}}
    )
    
    # Store job ID in DynamoDB for tracking
    dynamodb.put_item(
        TableName='FinancialReportJobs',
        Item={
            'JobId': {'S': textract_response['JobId']},
            'Status': {'S': 'PROCESSING'},
            'Document': {'S': f's3://{bucket}/{key}'},
            'Timestamp': {'S': datetime.now().isoformat()}
        }
    )
    
    # Send message to SQS for further processing
    sqs.send_message(
        QueueUrl=os.environ['PROCESSING_QUEUE_URL'],
        MessageBody=json.dumps({
            'jobId': textract_response['JobId'],
            'document': f's3://{bucket}/{key}'
        })
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Document processing started')
    }