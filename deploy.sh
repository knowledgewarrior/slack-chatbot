#!/bin/bash

# Requirements:
# aws command line installed
# permission to aws account where deploying lambda

LAMBDA_NAME=slack-listener-lambda

python3 -m pip install --target ./package slack_bolt

cd package && zip -r ../${LAMBDA_NAME}.zip .
cd .. && zip -g ${LAMBDA_NAME}.zip handler.py requirements.txt 

rm -rf package/

aws lambda update-function-code --function-name ${LAMBDA_NAME} --zip-file fileb://${LAMBDA_NAME}.zip

