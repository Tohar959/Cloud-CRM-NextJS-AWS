import json
import boto3
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('jobes')

def lambda_handler(event, context):
    try:
        params = event.get('queryStringParameters') or {}
        email = params.get('email')

        if not email:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing required query parameter: email'}),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }
            }
        response = table.scan(
            FilterExpression=Attr('Emial_client').eq(email)
        )

        jobs = response.get('Items', [])

        return {
            'statusCode': 200,
            'body': json.dumps(jobs),
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
