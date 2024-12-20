# File: financial_analysis/config.py

# AWS Configuration
AWS_CONFIG = {
    'region': 'us-east-1',  # Change to your region
    'account_id': '387311887840',  # Replace with your AWS account ID
    'bucket_names': {
        'raw': 'financial-reports-raw-{account_id}',
        'processed': 'financial-reports-processed-{account_id}',
        'models': 'financial-models-{account_id}'
    },
    'lambda_role_arn': 'arn:aws:iam::387311887840:role/financial-analysis-lambda-role',
    'step_functions_role_arn': 'arn:aws:iam::387311887840:role/financial-analysis-step-functions-role'
}

# API Keys
API_KEYS = {
    'news_api': '93a0eaf13a844ef4b17dc8cb09e77e0e'  # Replace with your News API key
}

# Model Configuration
MODEL_CONFIG = {
    'model_id': 'ProsusAI/finbert',
    'instance_type': 'ml.g5.xlarge',
    'instance_count': 1,
    'transformers_version': '4.26',
    'pytorch_version': '1.13',
    'python_version': 'py39'
}

# DynamoDB Tables
DYNAMODB_CONFIG = {
    'tables': {
        'jobs': 'FinancialReportJobs',
        'results': 'FinancialAnalysisResults'
    }
}

# SQS Queues
SQS_CONFIG = {
    'queues': {
        'processing': 'financial-analysis-document-processing.fifo',
        'analysis': 'financial-analysis-analysis-jobs.fifo'
    }
}

# API Gateway
API_CONFIG = {
    'name': 'FinancialAnalysisAPI',
    'stage': 'prod'
}

# Step Functions
STEP_FUNCTIONS_CONFIG = {
    'name': 'FinancialAnalysisPipeline'
}