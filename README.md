# Serverless FootyApp Formulas Trigger

This is a fully serverless Discord Bot that deploys using the serverless framework and runs in AWS Lambda without needing an API Gateway.
It uses slash commands to interact with an existing dynamodb table deployed as part of the Serverless Footy app.

This function updates the formulas on a trigger.

To Deploy:

```
serverless plugin install -n serverless-iam-roles-per-function
sls deploy
```