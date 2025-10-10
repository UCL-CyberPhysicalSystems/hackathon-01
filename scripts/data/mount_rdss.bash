#!/bin/bash

# Define variables
UCL_USER=$1
LOCAL_USER=$(whoami)
PROJECT_NAME="ritd-ag-project-rd025m-mxoch87"
DESTINATION=$2

# Mount the CIFS share
sudo mount \
  -t cifs \
  -o domain=ad.ucl.ac.uk,user="$UCL_USER",uid="$LOCAL_USER" \
  "//rdp.arc.ucl.ac.uk/$PROJECT_NAME" \
  "$DESTINATION"

# Ensure the mount was successful
if mountpoint -q "$DESTINATION"; then
  echo "Successfully mounted $PROJECT_NAME at $DESTINATION"
else
  echo "Failed to mount $PROJECT_NAME at $DESTINATION"
  exit 1
fi
