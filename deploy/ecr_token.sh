#!/bin/bash

# Obtain an authentication token for ECR Login and be able to upload new image tags

docker run \
  -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
  -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
  -e AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION \
  amazon/aws-cli ecr get-login-password
