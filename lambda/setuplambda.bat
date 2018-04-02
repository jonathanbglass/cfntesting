call aws iam create-role --role-name IamCleanUpRole  --assume-role-policy-document file://assumepolicyroledoc.json
call aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/IAMFullAccess --role-name IamCleanUpRole
call timeout /t 5
call aws s3 cp lambda_users.zip s3://jonathanglass.cloud/files/
call aws --region us-east-1 lambda create-function --function-name IamCleanUp --code S3Bucket=jonathanglass.cloud,S3Key=files/lambda_users.zip --role arn:aws:iam::873168614656:role/IamCleanUpRole --handler lambda_function.lambda_handler --runtime python3.6
call aws --region us-east-1 events put-rule --schedule-expression "cron(*/2 * * * ? *)" --name IamCleanUpRule --description "Daily Check for Unused Accounts"
call aws lambda add-permission --statement-id IamCleanUpSId --action lambda:InvokeFunction --principal events.amazonaws.com --source-arn arn:aws:events:us-east-1:873168614656:rule/IamCleanUpRule --function-name IamCleanUp --region us-east-1
