import json
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('jobes') 

def lambda_handler(event, context):
    data = json.loads(event['body'])

    job = {
        'j_Id': str(uuid.uuid4()),
        'Name_job': data['title'],
        'budget': data['budget'],
        'Description': data['description'],
        'Emial_client': data['client_email'],
        'Emial_employee': data['employee_email'],
        'status': data['status']
    }

    table.put_item(Item=job)

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({'message': 'Job created'})
    }
