import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Clintes')

def lambda_handler(event, context):
    try:
        response = table.scan()
        clients = response.get('Items', [])

        return {
            'statusCode': 200,
            'body': json.dumps(clients),
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
