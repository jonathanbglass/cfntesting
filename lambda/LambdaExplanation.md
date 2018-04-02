Compliance LAMBDA explanation
=====
## Requirements
Lambda should be able to
* detect and automatically disable accounts	not	used or	logged into for	90 days
* delete accounts	not	used or	logged into for	180	days

## Assumed Requirements
* Because the LAMBDA will be making changes, it needs at a minimum IAM Admin rights

## Solution process (write a script to do the following tasks)
1. Create a role for LAMBDA to use to test against the account with IAM Admin Rights
2. Write a Python Lambda function that queries IAM and finds out-of-date or unused accounts
3. Have the python code disable accounts > 90 days & delete > 180 days
4. Fire off the LAMBDA function daily via scheduled events (for testing purposes I'm using every 2 minutes)

# Conclusion
* I had a functioning LAMBDA script in about 90 minutes
* I spent 3 hours perfecting the launch and tear-down scripts and testing everything repeatedly
