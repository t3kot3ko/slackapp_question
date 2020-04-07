import json
import os
from urllib.parse import parse_qs
import boto3
import time
import hmac
import hashlib
from datetime import datetime

ddb = boto3.resource("dynamodb")
table = ddb.Table(os.getenv("TABLE_NAME"))  # Passed from template.yaml

def lambda_handler(event, context):
    method = event["httpMethod"]

    if method == "GET":
        # For debug purpose
        result = table.scan()["Items"]
        return json.dumps(result)

    if method == "POST":
        timestamp = event["headers"]['X-Slack-Request-Timestamp']

        # Validate request
        ## Timestamp
        if abs(time.time() - int(timestamp)) > 60 * 5:
            return {
                    "statusCode": 200,
                    "headers": {},
                    "body": json.dumps({
                        "response_type": "in_channel",
                        "text": "Could not validate the integrity of request"
                        })
                    }

        ## Signature
        sig_basestring = 'v0:' + timestamp + ':' + event["body"]
        my_signature = 'v0=' + hmac.new(os.getenv("SLACK_SIGNING_SECRET").encode("utf-8"), sig_basestring.encode("utf-8"), hashlib.sha256).hexdigest()

        if event["headers"]['X-Slack-Signature'] != my_signature:
            return {
                    "statusCode": 200,
                    "headers": {},
                    "body": json.dumps({
                        "response_type": "in_channel",
                        "text": "Could not validate the integrity of request"
                        })
                    }

        # Here, request integrity has been validated

        # Extract necessary fields
        body = parse_qs(event["body"])
        
        token = body["token"][0]
        trigger_id = body["trigger_id"][0]
        team_id = body["team_id"][0]
        text = body["text"][0]
        user_id = body["user_id"][0]
        channel_id = body["channel_id"][0]

        posted_at = datetime.now().isoformat()

        
        
        # Put item into DynamoDB
        table.put_item(Item={
            "trigger_id": trigger_id,
            "team_id": team_id,
            "text": text,
            "user_id": user_id,
            "channel_id": channel_id,
            "posted_at": posted_at
        })

        return {
                "statusCode": 200,
                "headers": {},
                "body": json.dumps({
                    "response_type": "in_channel",
                    "text": "Your question has been accepted: " + str(event)
                    })
                }

