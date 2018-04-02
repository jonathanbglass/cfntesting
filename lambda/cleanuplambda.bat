call aws --region us-east-1 events delete-rule --name IamCleanUpRule
call aws --region us-east-1 lambda remove-permission --statement-id IamCleanUpSId --function-name IamCleanUp
call aws --region us-east-1 lambda delete-function --function-name IamCleanUp
call aws iam detach-role-policy --policy-arn arn:aws:iam::aws:policy/IAMFullAccess --role-name IamCleanUpRole
timeout /T 5
call aws iam delete-role --role-name IamCleanUpRole
