#!/bin/bash

# Push new image tag to ECR
#
# @param $1 ecr_token - AWS ECR Access token
# @param $2 tag_name - Tag Name that will be pushed

ECR_TOKEN=$1
TAG_NAME=$2

docker login --username AWS -p "$ECR_TOKEN" 052184127097.dkr.ecr.us-east-1.amazonaws.com

docker tag lift-pass:latest 052184127097.dkr.ecr.us-east-1.amazonaws.com/lift-pass:latest
docker push 052184127097.dkr.ecr.us-east-1.amazonaws.com/lift-pass:latest

docker tag lift-pass:latest 052184127097.dkr.ecr.us-east-1.amazonaws.com/lift-pass:$TAG_NAME
docker push 052184127097.dkr.ecr.us-east-1.amazonaws.com/lift-pass:$TAG_NAME
