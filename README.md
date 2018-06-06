# snapshotalyzer69

Demo project to manage AWS EC2 instance snapshots

## About

This project is a demo, and uses boto3 to manage AWS EC2 instance snapshots.

## Configuring

snappy uses the configuration file created by the AWS CLI. e.g.

'aws configure --profile snappy'

## Running

'pipenv run python snappy/snappy.py <command> <--project=PROJECT>'

*command* is list, start or stop
*project* is optional
