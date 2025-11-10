import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('jobes')

def lambda_handler(event, context):
    try:
        response = table.scan()
        jobs = response.get('Items', [])

        return {
            'statusCode': 200,
            'body': json.dumps(jobs),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Methods': '*'
            }
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Methods': '*'
            }
        }
