import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Employee')

def lambda_handler(event, context):
    email = event.get('queryStringParameters', {}).get('email')
    
    if not email:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing email parameter'})
        }

    try:
        response = table.get_item(Key={'Emial_employee': email})
        employee = response.get('Item')

        if not employee:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Employee not found'})
            }

        return {
            'statusCode': 200,
            'body': json.dumps({'name': employee.get('Name', '')})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f"Internal error: {str(e)}"})
        }
