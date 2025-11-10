import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Meetings')

def lambda_handler(event, context):
    email = event.get('queryStringParameters', {}).get('email')
    
    if not email:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing email parameter'})
        }

    try:
       
        response = table.query(
            IndexName='Emial_client-index', 
            KeyConditionExpression=Key('Emial_client').eq(email)
        )

        items = response.get('Items', [])

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(items)
        }

    except Exception as e:
        print('Error querying meetings:', e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Failed to retrieve meetings'})
        }
