
import gitlab
import boto3
import os
import requests
import pymysql

def lambda_handler(event, context):
    arn = event['SecretId']
    token = event['ClientRequestToken']
    step = event['Step']

    # Setup the client
    service_client = boto3.client('secretsmanager')

    # Fetch tags via list_tags_for_resource
    resp = service_client.describe_secret(SecretId=arn)
    tags = {tag['Key']: tag['Value'] for tag in resp.get('Tags', [])}
    tool = tags.get('tool')
    print(f"Tool tag found: {tool}")
    if not tool:
        print("❗ No 'tool' tag found—exiting")
        exit(1)

    # Make sure the version is staged correctly
    metadata = service_client.describe_secret(SecretId=arn)
    if not metadata['RotationEnabled']:
        raise ValueError("Secret %s is not enabled for rotation" % arn)
    
    if step == "createSecret":
        create_secret(service_client, arn, token, tool)

    elif step == "setSecret":
        set_secret(service_client, arn, token, tool)

    elif step == "testSecret":
        test_secret(service_client, arn, token, tool)

    elif step == "finishSecret":
        finish_secret(service_client, arn, token, tool)

    else:
        raise ValueError("Invalid step parameter")


def create_secret(service_client, arn, token, tool):

    if tool == "gitlab":
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
    elif tool == "database":
            service_client.get_secret_value(SecretId=arn, VersionStage="AWSCURRENT")

            # Now try to get the secret version, if that fails, put a new secret
            try:
                service_client.get_secret_value(SecretId=arn, VersionId=token, VersionStage="AWSPENDING")
            except service_client.exceptions.ResourceNotFoundException:
                # Generate a random password
                passwd = service_client.get_random_password(ExcludeCharacters='/@"\'\\')
                # Put the secret
                service_client.put_secret_value(SecretId=arn, ClientRequestToken=token, SecretString=passwd['RandomPassword'], VersionStages=['AWSPENDING'])

    

def set_secret(service_client, arn, token, tool):

    if tool == "database":
        pending_secret = service_client.get_secret_value(
            SecretId=arn,
            VersionId=token,
            VersionStage="AWSPENDING"
        )

        # Extract DB cluster identifier, username, and new password from the secret
        db_cluster_id = "database-1"
        db_password = pending_secret['SecretString']  # <-- plain text password

        print(db_password)

        # Update the Aurora MySQL master password using boto3
        rds_client = boto3.client('rds')
        rds_client.modify_db_cluster(
            DBClusterIdentifier=db_cluster_id,
            MasterUserPassword=db_password,
            ApplyImmediately=True
        )
        print(f"Updated Aurora cluster {db_cluster_id} master password.")
    else:
        print("No action in setting gitlab PAT secret, just storing the new token.")
    

def test_secret(service_client, arn, token, tool):
    if tool == "database":
        pending_secret = service_client.get_secret_value(
            SecretId=arn,
            VersionId=token,
            VersionStage="AWSPENDING"
        )
        db_password = pending_secret['SecretString']

        db_host = "database-1-instance-1.co3iwkw8u44p.us-east-1.rds.amazonaws.com"
        db_user = "admin"
        db_name = "jira_data"

        max_attempts = 5
        for attempt in range(max_attempts):
            try:
                conn = pymysql.connect(
                    host=db_host,
                    user=db_user,
                    password=db_password,
                    database=db_name,
                    connect_timeout=5
                )
                conn.close()
                print("Password test succeeded: able to connect to Aurora DB.")
                return
            except Exception as e:
                print(f"Attempt {attempt+1} failed: {e}")
                time.sleep(10)  # Wait before retrying
        raise ValueError("Failed to authenticate to Aurora DB with pending password after retries.")

    else:
        print("No action in testing gitlab PAT secret, just storing the new token.")
    

def finish_secret(service_client, arn, token, tool):
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
