import boto3

class APIGatewaySetup:
    def __init__(self):
        self.apigateway = boto3.client('apigateway')
    
    def setup_api(self):
        try:
            # Create API
            api = self.apigateway.create_rest_api(
                name='FinancialAnalysisAPI',
                description='API for financial report analysis'
            )
            
            # Get root resource
            resources = self.apigateway.get_resources(restApiId=api['id'])
            root_id = resources['items'][0]['id']
            
            # Create endpoints
            self.create_analyze_endpoint(api['id'], root_id)
            print(f"Created API Gateway: {api['id']}")
            return api['id']
        except Exception as e:
            print(f"Error setting up API Gateway: {str(e)}")
    
    def create_analyze_endpoint(self, api_id, root_id):
        resource = self.apigateway.create_resource(
            restApiId=api_id,
            parentId=root_id,
            pathPart='analyze'
        )
        
        self.apigateway.put_method(
            restApiId=api_id,
            resourceId=resource['id'],
            httpMethod='POST',
            authorizationType='NONE'
        )