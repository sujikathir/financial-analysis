import boto3
import json
import os
from datetime import datetime

# All AWS clients setup
s3 = boto3.client('s3')
dynamodb = boto3.client('dynamodb')
sqs = boto3.client('sqs')
lambda_client = boto3.client('lambda')
apigateway = boto3.client('apigateway')

class AWSResourceSetup:
    def __init__(self):
        self.account_id = boto3.client('sts').get_caller_identity()['Account']
        self.region = boto3.session.Session().region_name
    
    def setup_s3(self):
        buckets = {
            'raw': f'financial-reports-raw-{self.account_id}',
            'processed': f'financial-reports-processed-{self.account_id}',
            'models': f'financial-models-{self.account_id}'
        }
        
        for purpose, bucket_name in buckets.items():
            try:
                s3.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={
                        'LocationConstraint': self.region
                    }
                )
                print(f"Created bucket: {bucket_name}")
            except Exception as e:
                print(f"Error creating bucket {bucket_name}: {str(e)}")
    
    def setup_dynamodb(self):
        tables = {
            'FinancialReportJobs': {
                'key': 'JobId',
                'type': 'S'
            },
            'FinancialAnalysisResults': {
                'key': 'DocumentId',
                'type': 'S'
            }
        }
        
        for table_name, config in tables.items():
            try:
                dynamodb.create_table(
                    TableName=table_name,
                    KeySchema=[{'AttributeName': config['key'], 'KeyType': 'HASH'}],
                    AttributeDefinitions=[{'AttributeName': config['key'], 'AttributeType': config['type']}],
                    BillingMode='PAY_PER_REQUEST'
                )
                print(f"Created table: {table_name}")
            except Exception as e:
                print(f"Error creating table {table_name}: {str(e)}")
    
    def setup_sqs(self):
        queues = ['document-processing', 'analysis-jobs']
        
        for queue in queues:
            try:
                response = sqs.create_queue(
                    QueueName=f'financial-analysis-{queue}.fifo',
                    Attributes={
                        'FifoQueue': 'true',
                        'ContentBasedDeduplication': 'true'
                    }
                )
                print(f"Created queue: {response['QueueUrl']}")
            except Exception as e:
                print(f"Error creating queue {queue}: {str(e)}")