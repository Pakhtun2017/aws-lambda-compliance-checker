Python script that checks AWS Lambda functions for compliance with certain standards. It integrates this script into a GitHub Actions workflow. It uses Cron to automatically run the compliance checks every day at designated time. This ensures that any changes to Lambda functions or related AWS resources adhere to your compliance standards before they are merged into the main branch. 
1) Makes a list_functions() call to user's AWS account
2) Checks that the Lambda function(s) meet the following compliance requirements:
    a) function uses Python 3.8
    b) monitoring is enabled
    c) certain security layer is used
    For example, present code triggers the following 2 violations:
    1) monitoring violation because monitoring is not enabled in the existing lambda function in my AWS account, 's3_lambda2'
    2) security layer violation because my function does not use the security layer

