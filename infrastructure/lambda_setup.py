import boto3
import os
import shutil
import subprocess

class LambdaSetup:
    def __init__(self):
        self.lambda_client = boto3.client('lambda')
        
    def create_deployment_package(self):
        # Create deployment directory
        os.makedirs('deployment_packages/document_processor', exist_ok=True)
        
        # Install requirements
        subprocess.check_call([
            'pip', 'install',
            '--target', 'deployment_packages/document_processor/',
            'boto3', 'pandas'
        ])
        
        # Create zip file
        shutil.make_archive(
            'deployment_packages/document_processor',
            'zip',
            'deployment_packages/document_processor'
        )
    
    def deploy_lambda(self, role_arn, queue_url):
        with open('deployment_packages/document_processor.zip', 'rb') as f:
            code_content = f.read()
        
        try:
            response = self.lambda_client.create_function(
                FunctionName='financial-document-processor',
                Runtime='python3.9',
                Role=role_arn,
                Handler='document_processor.lambda_handler',
                Code={'ZipFile': code_content},
                Timeout=300,
                MemorySize=1024,
                Environment={
                    'Variables': {
                        'PROCESSING_QUEUE_URL': queue_url,
                        'RESULTS_TABLE': 'FinancialAnalysisResults'
                    }
                }
            )
            print(f"Created Lambda function: {response['FunctionName']}")
        except Exception as e:
            print(f"Error creating Lambda function: {str(e)}")