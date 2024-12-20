# File: financial_analysis/infrastructure/step_functions_setup.py

import boto3
import json

class StepFunctionsSetup:
    def __init__(self):
        self.stepfunctions = boto3.client('stepfunctions')
    
    def setup_workflow(self, role_arn):
        # Read workflow definition
        with open('src/step_functions/workflow.json', 'r') as f:
            workflow_definition = f.read()
        
        try:
            response = self.stepfunctions.create_state_machine(
                name='FinancialAnalysisPipeline',
                definition=workflow_definition,
                roleArn=role_arn,
                type='STANDARD'
            )
            print(f"Created Step Functions workflow: {response['stateMachineArn']}")
        except Exception as e:
            print(f"Error creating Step Functions workflow: {str(e)}")