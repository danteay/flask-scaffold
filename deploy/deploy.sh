#!/bin/bash

# Script to deploy application to a certain cluster an stage configuration
#
# @param $1 app_name - Application name by environment
# @param $2 aws_key - AWS Access Key ID of the account to upload image
# @param $3 aws_secret - AWS Secret Access Key of the account to upload image
# @param $4 aws_region - AWS Default Region of the current repository
# @param $5 cluster - AWS Cluster name to deploy the application
# @param $6 port - Exposed Container port that will be use on the deploy
# @param $7 tag_name - Latest commit tag uploaded to the ECR image

STACK_FILE=$(pwd)/deploy/stackcf.yml
APP_NAME=$1
AWS_KEY=$2
AWS_SECRET=$3
AWS_REGION=$4
CLUSTER=$5
PORT=$6
TAG_NAME=$7

alias aws="docker run \
  -e AWS_ACCESS_KEY_ID=$AWS_KEY \
  -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET \
  -e AWS_DEFAULT_REGION=$AWS_REGION \
  -v $STACK_FILE:/stack.yml \
  amazon/aws-cli"

aws cloudformation update-stack --stack-name $APP_NAME \
  --template-body file:///stack.yml --parameters \
  ParameterKey=DockerImage,ParameterValue=052184127097.dkr.ecr.us-east-1.amazonaws.com/lift-pass:$TAG_NAME \
  ParameterKey=ClusterName,ParameterValue=$CLUSTER \
  ParameterKey=AppName,ParameterValue=$APP_NAME \
  ParameterKey=ContainerPort,ParameterValue=$PORT
