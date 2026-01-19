#!/bin/bash

# Docker run script for ROS2 containers (simplified)
# Usage: bash run-docker.bash [profile] [ROS_DISTRO] [VERSION_ID]

set -e  # Exit on error

# Set default values
PROFILE="${1:-ros2}"
ROS_DISTRO="${2:-humble}"
VERSION_ID="${3:-0.0.1}"

IMAGE_TAG="ros2:${ROS_DISTRO}-${VERSION_ID}"
CONTAINER_NAME="ros2-${ROS_DISTRO}"


# Enable X11 forwarding
#xhost +
xhost +local:docker > /dev/null 2>&1

# Run container
docker run \
    --name "${CONTAINER_NAME}" \
    --entrypoint bash \
    -it \
    -e "ACCEPT_EULA=Y" \
    -e "PRIVACY_CONSENT=Y" \
    --rm \
    --network=host \
    -e "DISPLAY=$DISPLAY" \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
    -v "$HOME/.Xauthority:/root/.Xauthority:rw" \
    -v "$PWD:/workspace" \
    "${IMAGE_TAG}"

# Cleanup
xhost -local:docker > /dev/null 2>&1
