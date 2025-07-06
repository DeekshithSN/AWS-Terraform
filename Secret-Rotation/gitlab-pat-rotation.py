
import gitlab
import boto3
import os
import requests

def lambda_handler(event, context):
    arn = event['SecretId']
    token = event['ClientRequestToken']
    step = event['Step']

    # Setup the client
    service_client = boto3.client('secretsmanager')

    # Make sure the version is staged correctly
    metadata = service_client.describe_secret(SecretId=arn)
    if not metadata['RotationEnabled']:
        raise ValueError("Secret %s is not enabled for rotation" % arn)
    
    if step == "createSecret":
        create_secret(service_client, arn, token)

    elif step == "setSecret":
        set_secret(service_client, arn, token)

    elif step == "testSecret":
        test_secret(service_client, arn, token)

    elif step == "finishSecret":
        finish_secret(service_client, arn, token)

    else:
        raise ValueError("Invalid step parameter")


def create_secret(service_client, arn, token):
    print("Creating new gitlab PAT secret...")
    
    try:
        # Fetch current secret (PAT) from Secrets Manager
        resp = service_client.get_secret_value(SecretId=arn, VersionStage="AWSCURRENT")
        current_pat = resp["SecretString"]
        print("Current PAT:", current_pat)

        resp = requests.get("https://gitlab.com/", timeout=10)
        print("Status:", resp.status_code)
        
        # Rotate the PAT via GitLab
        gl = gitlab.Gitlab("https://gitlab.com", private_token=current_pat)
        token_obj = gl.personal_access_tokens.get("self", lazy=True)
        token_obj.rotate()
        new_pat = token_obj.token
        print("New PAT:", new_pat)
        
        # Store new token as AWSPENDING version
        service_client.put_secret_value(
            SecretId=arn,
            ClientRequestToken=token,
            SecretString=new_pat,
            VersionStages=["AWSPENDING"]
        )
    except Exception as e:
        print(f"Password test failed: {e}")
    

def set_secret(service_client, arn, token):
    print("No action in setting gitlab PAT secret, just storing the new token.")
    

def test_secret(service_client, arn, token):
    print("No action in testing gitlab PAT secret, just storing the new token.")
    

def finish_secret(service_client, arn, token):
    print("Finishing secret rotation...")
    # First describe the secret to get the current version
    metadata = service_client.describe_secret(SecretId=arn)

    for version in metadata["VersionIdsToStages"]:
        if "AWSCURRENT" in metadata["VersionIdsToStages"][version]:
            if version == token:
                # The correct version is already marked as current, return
                return

            # Finalize by staging the secret version current
            service_client.update_secret_version_stage(SecretId=arn, VersionStage="AWSCURRENT", MoveToVersionId=token, RemoveFromVersionId=version)
            break



