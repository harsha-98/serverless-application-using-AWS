import json
import boto3


TABLE_NAME = "Minion"

dynamodb = boto3.resource('dynamodb', region_name="us-east-2")
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):
    response = table.get_item(
                                Key={
                                        'minionid': event['minionid']
                                    }
                            )
        
    if('Item' in response):
        items=response['Item']
        if(response['Item']['minionStatus']==1):
            table.update_item(
                    Key={
                            'minionid': event['minionid']
                        },
                    UpdateExpression= "SET minionStatus = :minionStatus",
                    ExpressionAttributeValues={':minionStatus': 0},
                    ReturnValues="UPDATED_NEW")
                    
                    
            return  {
                        'statusCode': 200,
                        'body': response['Item'],
                        'headers': {
                                        'Content-Type': 'application/json',
                                        'Access-Control-Allow-Origin': '*'
                                    }
                    }
        else:
            return "This minion was already called!!"
    else:
        return {
                    "No minion found with  id" : event['minionid']
        }
