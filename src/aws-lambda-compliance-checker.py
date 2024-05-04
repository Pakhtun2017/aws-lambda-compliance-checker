import json
import boto3
from botocore.exceptions import BotoCoreError, ClientError

def fetch_lambda_functions():
    client = boto3.client('lambda')
    try:
        response = client.list_functions()
        return response['Functions']
    except (BotoCoreError, ClientError) as e:
        print(f"Failed to fetch Lambda functions: {str(e)}")
        return []  # Return an empty list to handle gracefully in downstream processing

def check_compliance(lambda_function):
    compliant_layer = "arn:aws:lambda:us-east-1:123456789012:layer:common-utilities"
    try:
        compliance_details = {
            'runtime': lambda_function.get('Runtime') == 'python3.8',
            'monitoring': lambda_function.get('Environment', {}).get('Variables', {}).get("MONITORING") == "ENABLED",
            'security layer': compliant_layer in lambda_function.get('Layers', [])
        }
        compliance_json = json.dumps(compliance_details) # serializes compliance_details dictionary into json string
        return compliance_json
    except TypeError as e:
        print(f"Error serializing compliance details: {str(e)}")
        return json.dumps({})  # Return empty compliance details as JSON

def evaluate_compliance(func):
    try:
        compliance_result = json.loads(check_compliance(func)) # deserializes json string output of check_compliance(func) into Python dictionary
        is_compliant = all(compliance_result.values())
        return compliance_result, is_compliant
    except json.JSONDecodeError as e:
        print(f"Error decoding compliance JSON: {str(e)}")
        return {}, False  # Assume non-compliance if data cannot be decoded, 
        # returns an empty dictionary for compliance_result and False for is_compliant

def get_lambda_with_violations():
    lambda_functions = fetch_lambda_functions()
    return [
        {
            "function_name": func.get('FunctionName'),
            "runtime": func.get('Runtime'),
            "compliance": compliance_result
        }
        for func in lambda_functions
        for compliance_result, is_compliant in [evaluate_compliance(func)]
        if not is_compliant
    ]

def format_report(lambda_with_violations):
    if not lambda_with_violations:
        print("All Lambda functions are compliant.")
        return
    print("Lambda functions with violations:")
    for func in lambda_with_violations:
        print(f"Function Name: {func['function_name']}, Runtime: {func['runtime']}")
        violations = ', '.join(key for key, value in func['compliance'].items() if not value)
        print(f"Non-compliance violations: {violations}")
        print("------")

# Assuming Boto3 and AWS configuration are set up
lambda_with_violations = get_lambda_with_violations()
format_report(lambda_with_violations)
