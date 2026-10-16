#!/bin/bash

# Delete these two lines############################
#echo "Edit deploy.sh first then delete these lines"
#exit 1
#####################################################

# Configuration
CONTAINER_NAME="lafbe"
IMAGE_NAME="lafbe"
SSH_PORT="2324"

# Clear the old container
docker stop "$CONTAINER_NAME"
docker rm "$CONTAINER_NAME"

#build it
docker build -t $IMAGE_NAME .

#start up the new one
docker run -d \
  --name $CONTAINER_NAME \
  --restart unless-stopped \
  --security-opt=no-new-privileges:true \
  -p $SSH_PORT:22 \
   $IMAGE_NAME

#mount lines for docker run
#  --mount type=volume,source=codex-data,target=/home/dan/.codex \
#  --mount type=bind,source="/Users/dan/docker/tutor_frog/curricula",target=/opt/app/Curricula \