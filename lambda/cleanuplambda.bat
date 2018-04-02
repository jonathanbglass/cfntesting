call aws events delete-rule --name IamCleanUpRule
call aws lambda delete-function --region us-east-1 --function-name IamCleanUp 
call aws lambda remove-permission --statement-id IamCleanUpSId --function-name IamCleanUp --region us-east-1