{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "04b53cc1-8c90-45d7-bc1c-d6ae59cc8a97",
   "metadata": {},
   "outputs": [],
   "source": [
    "import boto3\n",
    "import json\n",
    "\n",
    "class StepFunctionsSetup:\n",
    "    def __init__(self):\n",
    "        self.stepfunctions = boto3.client('stepfunctions')\n",
    "    \n",
    "    def setup_workflow(self, role_arn):\n",
    "        # Read workflow definition\n",
    "        with open('src/step_functions/workflow.json', 'r') as f:\n",
    "            workflow_definition = f.read()\n",
    "        \n",
    "        try:\n",
    "            response = self.stepfunctions.create_state_machine(\n",
    "                name='FinancialAnalysisPipeline',\n",
    "                definition=workflow_definition,\n",
    "                roleArn=role_arn,\n",
    "                type='STANDARD'\n",
    "            )\n",
    "            print(f\"Created Step Functions workflow: {response['stateMachineArn']}\")\n",
    "        except Exception as e:\n",
    "            print(f\"Error creating Step Functions workflow: {str(e)}\")"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.11"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
