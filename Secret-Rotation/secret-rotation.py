import boto3
import json
import pymysql
import time

def lambda_handler(event, context):
    arn = event['SecretId']
    token = event['ClientRequestToken']
    step = event['Step']

    print(step)
    print(token)

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

    # Now try to get the secret version, if that fails, put a new secret
    try:
        service_client.get_secret_value(SecretId=arn, VersionId=token, VersionStage="AWSPENDING")
    except service_client.exceptions.ResourceNotFoundException:
        # Generate a random password
        passwd = service_client.get_random_password(ExcludeCharacters='/@"\'\\')
        # Put the secret
        service_client.put_secret_value(SecretId=arn, ClientRequestToken=token, SecretString=passwd['RandomPassword'], VersionStages=['AWSPENDING'])


def set_secret(service_client, arn, token):
    # Retrieve the pending secret value
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


def test_secret(service_client, arn, token):
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
