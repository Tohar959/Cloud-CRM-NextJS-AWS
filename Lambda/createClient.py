import json
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Clintes')
cognito = boto3.client('cognito-idp')
ses = boto3.client('ses', region_name='us-east-2') 

USER_POOL_ID = 'us-east-2_qRGxu5KmM'
DEFAULT_TEMP_PASSWORD = 'Temp123!'
CLIENT_GROUP = 'clients'

def lambda_handler(event, context):
    print("Event received:", event)

    data = json.loads(event.get('body', '{}'))
    print("Parsed data:", data)

    email = data.get('email')
    name = data.get('name')
    phone = data.get('phone')
    image_url = data.get('image_url', '')
    temp_password = data.get('tempPassword', DEFAULT_TEMP_PASSWORD)

    if not email or not name:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing required fields: email and/or name'})
        }

    customer = {
        'Emial_client': email,
        'name': name,
        'phone': phone,
        'Creation_Date': datetime.utcnow().isoformat()
    }

    if image_url:
        customer['image_url'] = image_url

    try:
        print("Creating Cognito user...")
        cognito.admin_create_user(
            UserPoolId=USER_POOL_ID,
            Username=email,
            UserAttributes=[
                {'Name': 'email', 'Value': email},
                {'Name': 'name', 'Value': name}
            ],
            TemporaryPassword=temp_password
        )

        print("Adding user to group...")
        cognito.admin_add_user_to_group(
            UserPoolId=USER_POOL_ID,
            Username=email,
            GroupName=CLIENT_GROUP
        )

        print("Saving customer to DynamoDB...")
        table.put_item(Item=customer)

        print("Sending SES email verification request...")
        ses.verify_email_identity(EmailAddress=email)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Customer created. SES verification email sent.',
                'image_url': image_url
            })
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Failed: {str(e)}'})
        }
