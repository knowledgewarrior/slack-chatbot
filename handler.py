import os
import re
import boto3
import logging
from botocore.exceptions import ClientError
from slack_bolt import Ack, App
from slack_bolt.error import BoltError
from slack_bolt.adapter.aws_lambda import SlackRequestHandler

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# process_before_response must be True when running on FaaS
app = App(process_before_response=True)

slack_channel_id=os.environ.get("SLACK_CHANNEL_ID"),
slack_channel_name=os.environ.get("SLACK_CHANNEL_NAME"),
dev_redeploy_lambda_arn=os.environ.get("DEV_REDEPLOY_LAMBDA_ARN"),
prod_redeploy_lambda_arn=os.environ.get("PROD_REDEPLOY_LAMBDA_ARN"),
staging_redeploy_lambda_arn=os.environ.get("STAGING_REDEPLOY_LAMBDA_ARN")

@app.action("redeploy_button")
def redeploy(action, say, ack, respond):
    logger.info("Inside redeploy function...")
    ack()
    environment = action["value"]
    if environment == "dev":
        respond(f"Redeploying dev")
        lambda_arn = dev_redeploy_lambda_arn[0]
    elif environment == "prod":
        respond(f"Redeploying prod")
        lambda_arn = prod_redeploy_lambda_arn[0]
    elif environment == "staging":
        respond(f"Redeploying staging")
        lambda_arn = staging_redeploy_lambda_arn[0]
    else:
        respond(f"Cannot retrieve environment {environment!r}")
        return
    client = boto3.client('lambda')
    payload = '{}'
    client.invoke(FunctionName=lambda_arn, 
                     InvocationType='RequestResponse',
                     Payload=payload)
    respond(f"Completed redeploy")

@app.action("cancel_button")
def cancel_redeploy(action, ack, body, logger, respond):
    ack()
    logger.info(body)
    respond(f"Redeploy cancelled")
    return

@app.event("app_mention")
def handle(event, say):
    logger.info(event)
    channel_id = event.get("channel")
    if channel_id != slack_channel_id[0] :
        say(f"This bot is restricted to {slack_channel_name[0]}")
        return
    else:
        args = event["text"].split()[1:]
        if len(args) < 1:
            say(f":wave: Usage:  command `<environment id>`")
            return
        command = args.pop(0)

        if command == "redeploy":
            if len(args) != 1:
                say("Usage: redeploy `<environment id>`")
                return
            environment = args[0]
            say(
                blocks=[
                    {
        			"type": "actions",
        			"elements": [
        				    {
        					"type": "button",
        					"text": {
        						"type": "plain_text",
        						"text": "Redeploy",
        					},
        					"value": environment,
        					"action_id": "redeploy_button"
        				},
        				{
        					"type": "button",
        					"text": {
        						"type": "plain_text",
        						"text": "Cancel",
        					},
        					"action_id": "cancel_button"
        			    	}
        			    ]
        			}
                ]
            )

        else:
            say("Unknown command: `{command}`".format(command=command))
    
### Handler for all
def handler(event, context):
    slack_handler = SlackRequestHandler(app=app)
    return slack_handler.handle(event, context)
