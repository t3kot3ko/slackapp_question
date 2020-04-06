import json
import os
from urllib.parse import parse_qs
import boto3
from datetime import datetime

ddb = boto3.resource("dynamodb")
table = ddb.Table(os.getenv("TABLE_NAME"))  # Passed from template.yaml

def lambda_handler(event, context):
    method = event["httpMethod"]

    if method == "GET":
        result = table.scan()
        return result

    if method == "POST":
        body = parse_qs(event["body"])

        # Extract necessary fields
        token = body["token"][0]
        trigger_id = body["trigger_id"][0]
        team_id = body["team_id"][0]
        text = body["text"][0]
        user_id = body["user_id"][0]
        channel_id = body["channel_id"][0]

        posted_at = datetime.now().isoformat()

        # TODO: Validate request by token

        # Put item into DynamoDB
        table.put_item(Item={
            "trigger_id": trigger_id,
            "team_id": team_id,
            "text": text,
            "user_id": user_id,
            "channel_id": channel_id,
            "posted_at": posted_at
        })

        response_body = {
                "response_type": "in_channel",
                "text": "hello world"
                }

        return {
            "statusCode": 200,
            "headers": {},
            "body": json.dumps(response_body)
        }
