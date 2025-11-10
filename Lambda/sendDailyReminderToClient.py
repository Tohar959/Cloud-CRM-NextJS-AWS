import json
import boto3
from datetime import datetime, timedelta

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Meetings')
ses = boto3.client('ses', region_name='us-east-2')

SENDER = "serverside67@gmail.com"

def lambda_handler(event, context):
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    print("🔁 Starting reminder check for:", tomorrow)

    response = table.scan()
    meetings = response['Items']
    print(f"📋 Found {len(meetings)} meetings")

    for meeting in meetings:
        print("➡️ Checking meeting:", meeting)
        if meeting.get('Date') == tomorrow:
            recipient = meeting.get('Emial_client')
            time = meeting.get('Time')
            topic = meeting.get('topic_of_the_meeting', 'No topic')

            print(f"📨 Sending to {recipient}, topic: {topic} at {time}")

            try:
                ses.send_email(
                    Source=SENDER,
                    Destination={'ToAddresses': [recipient]},
                    Message={
                        'Subject': {'Data': "📅 Reminder: Meeting Tomorrow"},
                        'Body': {'Text': {'Data': f"Reminder: You have a meeting tomorrow at {time} about: {topic}."}}
                    }
                )
                print(f"✅ Email sent to: {recipient}")
            except Exception as e:
                print(f"❌ Failed to send email to {recipient}: {e}")

    return {
        'statusCode': 200,
        'body': json.dumps('Reminder emails sent to clients')
    }
