import boto3
import json
from datetime import datetime, timezone

def lambda_handler(event, context):
    iam = boto3.client('iam')
    response = iam.list_users()
    # handle "IsTruncated" variable in the future

    # checking for passsword last used
    for user in response['Users']:
        if 'PasswordLastUsed' in user:
            td=abs((datetime.now()-user['PasswordLastUsed']).days)
            if td > 180:
                print ("Delete Account: ", user['UserName'])
            elif td > 90:
                print ("Lock account: ", user['UserName'])
        # List access keys through the pagination interface.
        paginator = iam.get_paginator('list_access_keys')
        for keys in paginator.paginate(UserName=user['UserName']):
            keymeta = keys['AccessKeyMetadata'][0]
            if 'Active' in keymeta['Status']:
                keyused = iam.get_access_key_last_used (AccessKeyId=keymeta['AccessKeyId'])
                timedif = abs((datetime.now(timezone.utc)-keyused['AccessKeyLastUsed']['LastUsedDate']).days)
                if timedif > 180:
                    print ("Delete this user key: ", user['UserName'], keymeta['AccessKeyId'], timedif)
                elif timedif > 90:
                    print ("Deactivate this user key: ", user['UserName'], keymeta['AccessKeyId'], timedif)
    return 'Blah'
