import json
import boto3
import uuid

s3 = boto3.client('s3')
BUCKET_NAME = 'crm-customer-files'

EXTENSION_TO_MIME = {
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'png': 'image/png',
    'gif': 'image/gif',
    'webp': 'image/webp',
}

def lambda_handler(event, context):
    body = json.loads(event['body'])
    
    customer_name = body.get('name', 'unknown').replace(" ", "_")
    file_extension = body.get('file_extension', 'jpg').lower()
    file_name = f"{customer_name}_{str(uuid.uuid4())}.{file_extension}"
    
    content_type = EXTENSION_TO_MIME.get(file_extension, 'application/octet-stream')

    presigned_url = s3.generate_presigned_url(
        'put_object',
        Params={
            'Bucket': BUCKET_NAME,
            'Key': file_name,
            'ContentType': content_type
        },
        ExpiresIn=300
    )

    return {
        'statusCode': 200,
        'body': json.dumps({
            'upload_url': presigned_url,
            'file_key': file_name,
            'file_url': f"https://{BUCKET_NAME}.s3.amazonaws.com/{file_name}"
        }),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
