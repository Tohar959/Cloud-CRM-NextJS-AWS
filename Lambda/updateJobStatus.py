import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('jobes')

def lambda_handler(event, context):
    body = json.loads(event['body'])
    job_id = body.get('j_Id')
    new_status = body.get('status')

    if not job_id or not new_status:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing job ID or status'})
        }

    try:
        table.update_item(
            Key={'j_Id': job_id},
            UpdateExpression='SET #s = :val',
            ExpressionAttributeNames={'#s': 'status'},
            ExpressionAttributeValues={':val': new_status}
        )
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Job status updated'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
