import boto3
import json
from datetime import datetime, timezone

def delete_user(USERNAME, iam):
    # Remove the keys
    disable_user_profile(USERNAME, iam)
    remove_accesskeys(USERNAME, iam)
    remove_groups(USERNAME, iam)
    remove_policies(USERNAME, iam)
    remove_mfa(USERNAME, iam)
    remove_useracct(USERNAME, iam)
    return

def disable_user_profile(USERNAME, iam):
    """Change the login profile to disable the account"""
    try:
        response = iam.delete_login_profile(UserName=USERNAME)
    except Exception as err:
        print ('Login Profile Error: ' + str(err))
    return

def remove_accesskeys(USERNAME, iam):
    """Removes all access keys from an account"""
    kiam = boto3.resource('iam')
    paginator = iam.get_paginator('list_access_keys')
    for keys in paginator.paginate(UserName=USERNAME):
        if len(keys['AccessKeyMetadata']) > 0:
            print (len(keys['AccessKeyMetadata']))
            print (keys['AccessKeyMetadata'])
            for acckey in keys['AccessKeyMetadata']:
                access_key = kiam.AccessKey(USERNAME,acckey['AccessKeyId'])
                print (access_key)
                access_key.delete()
    return

def remove_groups(USERNAME, iam):
    # Get groups information
    giam = boto3.resource('iam')
    groupdata = iam.list_groups_for_user(UserName=USERNAME)
    groupmetadata = groupdata['Groups']
    if len(groupmetadata) == 0:
        print ("No Groups Assinged")
    else:
        # print (groupmetadata)
        for grpkeys in groupmetadata:
            group = giam.Group(grpkeys['GroupName'])
            grpresp = group.remove_user(UserName=USERNAME)
    return

def remove_policies(USERNAME,iam):
    # Get attached policy information
    piam = boto3.resource('iam')
    policydata = iam.list_attached_user_policies(UserName=USERNAME)
    policymetadata = policydata['AttachedPolicies']
    if len(policymetadata) == 0:
        print ("Assigned Policy: None")
    else:
        #print (policymetadata)
        for polkeys in policymetadata:
            policy = piam.Policy(polkeys['PolicyArn'])
            polresp = policy.detach_user(UserName=USERNAME)
            #print (polresp)
    return

def remove_mfa(USERNAME, iam):
    # Get MFA device status
    miam = boto3.resource('iam')
    mfadata = iam.list_mfa_devices(UserName=USERNAME)
    if len(mfadata['MFADevices']) == 0:
        print ("MFA Devices: None")
    else:
        mfa_device = miam.MfaDevice(USERNAME,mfadata['MFADevices'][0]['SerialNumber'])
        mfaresp = mfa_device.disassociate()
        print(mfaresp)
    return

def remove_useracct(USERNAME, iam):
    # Get MFA device status
    uiam = boto3.resource('iam')
    user = uiam.User(USERNAME)
    # print ("Remove ", USERNAME, " Account")
    try:
        userresp = user.delete()
    except Exception as err:
        print ('Error: ' + str(err))
    return

def lambda_handler(event, context):
    iam = boto3.client('iam')
    response = iam.list_users()
    # handle "IsTruncated" variable in the future
    # checking for passsword last used
    for user in response['Users']:
        print ("Found User: ", user['UserName'])
        if 'PasswordLastUsed' in user:
            td=abs((datetime.now()-user['PasswordLastUsed']).days)
            if td > 180:
                delete_user(user['UserName'],iam)
                print ("Deleted Account: ", user['UserName'])
            elif td > 90:
                disableresponse = disable_user_profile(['UserName'],iam)
                print ("Disabled Account: ", user['UserName'], ", Disable Response: ", disableresponse)
    return True

'''
# for running this manually for cfntesting
USERNAME='steve'
iam = boto3.client('iam')
response = iam.list_users()
for user in response['Users']:
    #print (user['UserName'])
    policydata = iam.list_attached_user_policies(UserName=user['UserName'])
    policymetadata = policydata['AttachedPolicies']
    if len(policymetadata) == 0:
        print ("Assigned Policy: None, UserName: ", user['UserName'])
    else:
        for k, v in enumerate(policymetadata):
            print (user['UserName'], v['PolicyName'])
    if USERNAME in user['UserName']:
        delete_user(user['UserName'],iam)
exit()
'''
