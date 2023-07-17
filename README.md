# Slack Listener Lambda aka ChatOps

This repo contains code to get started with using Slack to send commands via external lambdas to AWS infrastructure.

tl;dr, this is a lambda that can trigger other lambdas via Slack.

The lambda listens for Slack commands to run other lambdas.  For example, if you have a CodeDeploy application, you can create a "redeploy" lambda to redeploy your CodeDeploy application.  

The lambda in this repo, `handler.py` would be used to call the CodeDeploy lambda, whether in the existing account or another account, via the `staging_redeploy_lambda_arn=os.environ.get("STAGING_REDEPLOY_LAMBDA_ARN")` environment variable.  

If you use a multi-account structure on AWS, ie AWS Organizations / Control Tower, you'll need to set up your AWS infrastructure with IAM permissions between accounts.

`handler.py`
this file is the AWS Lambda for listening to slack events.
`requirements.txt`
python requirements file
`deploy.sh`
simple deploy script to push handler.py and required libraries to AWS
`slack_app_manifest.yml`
slack application configuration for importing into slack as an app after modifying for use.

For more information, see:
https://slack.dev/bolt-python/concepts