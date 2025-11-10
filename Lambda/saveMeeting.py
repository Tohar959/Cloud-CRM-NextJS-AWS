import json
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Meetings')

def lambda_handler(event, context):
    try:
        data = json.loads(event['body'])

        meeting = {
            'M_Id': str(uuid.uuid4()),
            'Date': data['date'],
            'Time': data['Time'],
            'Emial_client': data['Emial_client'],
            'Emial_employee': data['Emial_employee'],
            'location': data['location'],
            'topic_of_the_meeting': data.get('topic_of_the_meeting')
        }

        table.put_item(Item=meeting)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'The meeting is saved',
                'meeting_id': meeting['M_Id']
            }),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }
