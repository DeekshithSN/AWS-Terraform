import boto3
import datetime

def lambda_handler(event, context):
    ce = boto3.client('ce')
    sns = boto3.client('sns', region_name='us-east-1')  # Change region if needed

    # Get yesterday's date
    end = datetime.date.today()
    start = end - datetime.timedelta(days=1)

    # Fetch billing info for yesterday
    response = ce.get_cost_and_usage(
        TimePeriod={
            'Start': start.strftime('%Y-%m-%d'),
            'End': end.strftime('%Y-%m-%d')
        },
        Granularity='DAILY',
        Metrics=['UnblendedCost']
    )

    amount = response['ResultsByTime'][0]['Total']['UnblendedCost']['Amount']
    currency = response['ResultsByTime'][0]['Total']['UnblendedCost']['Unit']

    # Compose email
    subject = "AWS Daily Billing Report"
    body = f"Your AWS cost for {start} was {amount} {currency}."

    # Your SNS topic ARN (must have email subscription)
    topic_arn = 'arn'  # Replace with your SNS topic ARN

    # Publish the message to SNS
    sns.publish(
        TopicArn=topic_arn,
        Subject=subject,
        Message=body
    )

    print("Email sent via SNS!")
    return {"statusCode": 200, "body": "Email sent via SNS!"}
