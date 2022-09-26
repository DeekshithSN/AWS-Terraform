import boto3
client = boto3.client('sns')

def lambda_handler(event, context):
    Instance_id = event['detail']['instance-id']
    topic_arn = 'arn_of_sns_alerts'
    message = 'your server ' + Instance_id + 'is down'
    client.publish(TopicArn=topic_arn,Message=message)
