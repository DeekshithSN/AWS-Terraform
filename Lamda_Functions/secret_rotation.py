import json
import boto3
import requests
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    arn = event['SecretId']
    token = event['ClientRequestToken']
    step = event['Step']
    GITHUB_API_URL = "https://api.github.com/authorizations"
    GITHUB_USERNAME = "your_github_username"

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

def create_new_github_pat():
    """
    Function to create a new GitHub PAT using the GitHub API.
    You can customize the scope and details as needed.
    """
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': f'Basic {GITHUB_USERNAME}:{CURRENT_GITHUB_PAT_TOKEN}'
    }
    
    payload = {
        "scopes": ["repo", "read:org"],  # Define your desired scopes
        "note": "New PAT Token created by Lambda"
    }
    
    response = requests.post(GITHUB_API_URL, headers=headers, data=json.dumps(payload))
    
    if response.status_code == 201:
        return response.json()['token']
    else:
        raise Exception(f"Failed to create a new GitHub token: {response.text}")

def list_gitlab_projects(NEW_GITHUB_PAT_TOKEN):
    """
    List all GitLab projects using the GitLab API and a Personal Access Token (PAT).
    """
    headers = {
        'Authorization': f'Bearer {GITLAB_PAT}'
    }

    params = {
        'membership': True,  # List only projects the user is a member of (optional)
        'per_page': 100      # Adjust as needed for pagination
    }

    response = requests.get(GITLAB_API_URL, headers=headers, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        projects = response.json()
        for project in projects:

def create_secret(service_client, arn, token):

    CURRENT_GITHUB_PAT_TOKEN = service_client.get_secret_value(SecretId=arn, VersionStage="AWSCURRENT")

    # Now try to get the secret version, if that fails, put a new secret
    try:
        service_client.get_secret_value(SecretId=arn, VersionId=token, VersionStage="AWSPENDING")
    except service_client.exceptions.ResourceNotFoundException:
        # Generate a random password
        passwd = create_new_github_pat(CURRENT_GITHUB_PAT_TOKEN)
        # Put the secret
        service_client.put_secret_value(SecretId=arn, ClientRequestToken=token, SecretString=passwd , VersionStages=['AWSPENDING'])


def set_secret(service_client, arn, token):
    print("No need to set jenkins credentails, as jenkins will read it from aws secrets itself ...")


def test_secret(service_client, arn, token):
        NEW_GITHUB_PAT_TOKEN = service_client.get_secret_value(SecretId=arn, VersionId=token, VersionStage="AWSPENDING")
        list_gitlab_projects(NEW_GITHUB_PAT_TOKEN)

def finish_secret(service_client, arn, token):
   
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
