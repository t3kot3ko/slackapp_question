import json
from urllib.parse import parse_qs
import boto3

ddb = boto3.resource("dynamodb")
table = ddb.Table("slack-questions")

# import requests


def lambda_handler(event, context):
    print(event)
    method = event["httpMethod"]

    if method == "GET":
        pass

    if method == "POST":
        body = parse_qs(event["body"])

        # Extract necessary fields
        token = body["token"][0]
        trigger_id = body["trigger_id"][0]
        team_id = body["team_id"][0]
        text = body["text"][0]
        user_id = body["user_id"][0]
        channel_id = body["channel_id"][0]

        # Put them into DynamoDB
        table.put_item(Item={"trigger_id": trigger_id, "foo": 1000})
        
        return {
            "statusCode": 200,
            "response_type": "in_channel",
            "text": body
        }
