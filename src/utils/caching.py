import boto3
import json

def get_cached_analysis(document_id):
    # Initialize clients
    elasticache = boto3.client('elasticache')
    dynamodb = boto3.client('dynamodb')
    
    try:
        cache_response = elasticache.get(document_id)
        if cache_response:
            return json.loads(cache_response)
    except:
        pass
    
    # If not in cache, get from DynamoDB
    response = dynamodb.get_item(
        TableName='FinancialAnalysisResults',
        Key={'DocumentId': {'S': document_id}}
    )
    
    # Store in cache for future requests
    if 'Item' in response:
        elasticache.set(
            document_id,
            json.dumps(response['Item']),
            ex=3600  # Cache for 1 hour
        )
        return response['Item']
    
    return None