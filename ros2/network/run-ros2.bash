#!/bin/bash

# Docker run script for ROS2 containers
# Usage: bash run-docker.bash [ROS_DISTRO] [VERSION_ID]
# Or set environment variables: GITHUB_USERNAME, PROJECT_NAME, VERSION_ID

set -e  # Exit on error

# Set default values from environment variables or arguments
GITHUB_USERNAME="${GITHUB_USERNAME:-YOUR_GITHUB_USERNAME}"
PROJECT_NAME="${PROJECT_NAME:-ros2condenser}"
VERSION_ID="${3:-${VERSION_ID:-0.0.2}}"
ROS_DISTRO="${2:-${ROS_DISTRO:-humble}}"

# Build the image name using provided variables
IMAGE="ghcr.io/${GITHUB_USERNAME}/${PROJECT_NAME}:${VERSION_ID}"

# For backward compatibility with the original script format
# If no GITHUB_USERNAME was provided and it's still the placeholder, use the old naming convention
if [[ "${GITHUB_USERNAME}" == "YOUR_GITHUB_USERNAME" ]]; then
    echo "Warning: Using default GITHUB_USERNAME placeholder. Please set GITHUB_USERNAME environment variable."
    echo "Falling back to original image naming convention: ros2:network-${ROS_DISTRO}-${VERSION_ID}"
    IMAGE="ros2:network-${ROS_DISTRO}-${VERSION_ID}"
fi

CONTAINER_NAME="${PROJECT_NAME}-${ROS_DISTRO}"

echo "Running container with:"
echo "  Image: ${IMAGE}"
echo "  Container name: ${CONTAINER_NAME}"
echo "  ROS Distro: ${ROS_DISTRO}"
echo "  Version: ${VERSION_ID}"

# Allow Docker to connect to X server and Enable X11 forwarding
xhost +local:docker > /dev/null 2>&1

# Run container - combining both your and original parameters
docker run \
    --name "${CONTAINER_NAME}" \
    --entrypoint bash \
    -it \
    --rm \
    --net=host \
    --privileged \
    -v "$(pwd):/workspace" \
    --device=/dev/video0:/dev/video0 \
    --group-add video \
    --env "DISPLAY=$DISPLAY" \
    --env "QT_X11_NO_MITSHM=1" \
    --env "ACCEPT_EULA=Y" \
    --env "PRIVACY_CONSENT=Y" \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
    -v "$HOME/.Xauthority:/home/rosuser/.Xauthority:rw" \
    -v "$HOME/repositories/UCL-CyberPhysicalSystems/hackathon-01:/home/rosuser/hackathon-01" \
    "${IMAGE}"

# Cleanup
xhost -local:docker > /dev/null 2>&1