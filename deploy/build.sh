#!/bin/bash

# This command runs the docker build with previous configured entries
#
# @param $1 stage - Environment name - Default `dev`
# @param $2 port - Is the default op[en port on the docker image - Default `8000`
# @param $3 aws_key - AWS Access Key ID of the account to upload image
# @param $4 aws_secret - AWS Secret Access Key of the account to upload image
# @param $5 aws_region - AWS Default Region of the current repository

docker build -t lift-pass:latest \
  --build-arg stage=$1 \
  --build-arg port=$2 \
  --build-arg aws_key=$3 \
  --build-arg aws_secret=$4 \
  --build-arg aws_region=$5 \
   .
