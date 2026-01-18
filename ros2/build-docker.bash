#!/bin/bash

# Docker build script with configurable ROS distribution and version
# Usage: bash build-docker.bash [profile] [ROS_DISTRO] [VERSION_ID]

set -e  # Exit on error

# Set default values
PROFILE="${1:-ros2}"
ROS_DISTRO="${2:-humble}"
VERSION_ID="${3:-0.0.1}"

# Dockerfile paths
DOCKERFILE_ROS2="basic/Dockerfile-ros2"
DOCKERFILE_ROS2_CUDA="cuda/Dockerfile-ros2-cuda"
DOCKERFILE_ISAACSIM_ROS2="isaacsim/Dockerfile-isaacsim-ros2"

# Check if Dockerfiles exist
check_dockerfile() {
    local dockerfile_path="$1"
    local profile_name="$2"
    
    if [ ! -f "$dockerfile_path" ]; then
        echo "Error: Dockerfile not found for $profile_name profile: $dockerfile_path"
        echo "Please ensure the Dockerfile exists at the specified location."
        exit 1
    fi
}

case "$PROFILE" in
    "ros2")
        echo "Building ROS2 base image..."
        echo "ROS_DISTRO: $ROS_DISTRO, VERSION_ID: $VERSION_ID"
        check_dockerfile "$DOCKERFILE_ROS2" "ros2"
        docker build --tag ros2:${ROS_DISTRO}-${VERSION_ID} --file "$DOCKERFILE_ROS2" .
        ;;
    "ros2cuda")
        echo "Building ROS2 with CUDA..."
        echo "ROS_DISTRO: $ROS_DISTRO, VERSION_ID: $VERSION_ID"
        check_dockerfile "$DOCKERFILE_ROS2_CUDA" "ros2cuda"
        docker build -t ros2:cuda-${ROS_DISTRO}-${VERSION_ID} -f "$DOCKERFILE_ROS2_CUDA" .
        ;;
    "isaacsim")
        echo "Building Isaac Sim with ROS2..."
        echo "ROS_DISTRO: $ROS_DISTRO, VERSION_ID: $VERSION_ID"
        check_dockerfile "$DOCKERFILE_ISAACSIM_ROS2" "isaacsim"
        docker build -t isaac_sim_ros2:5.0.0-${ROS_DISTRO}-${VERSION_ID} -f "$DOCKERFILE_ISAACSIM_ROS2" .
        ;;
    "all")
        echo "Building all images..."
        echo "ROS_DISTRO: $ROS_DISTRO, VERSION_ID: $VERSION_ID"
        
        # Build ROS2 base
        echo "Building ROS2 base image..."
        check_dockerfile "$DOCKERFILE_ROS2" "ros2"
        docker build -t ros2:${ROS_DISTRO}-${VERSION_ID} -f "$DOCKERFILE_ROS2" .
        
        # Build ROS2 with CUDA
        echo "Building ROS2 with CUDA..."
        check_dockerfile "$DOCKERFILE_ROS2_CUDA" "ros2cuda"
        docker build -t ros2:cuda-${ROS_DISTRO}-${VERSION_ID} -f "$DOCKERFILE_ROS2_CUDA" .
        
        # Build Isaac Sim with ROS2
        echo "Building Isaac Sim with ROS2..."
        check_dockerfile "$DOCKERFILE_ISAACSIM_ROS2" "isaacsim"
        docker build -t isaac_sim_ros2:5.0.0-${ROS_DISTRO}-${VERSION_ID} -f "$DOCKERFILE_ISAACSIM_ROS2" .
        ;;
    "-h"|"--help")
        echo "Usage: $0 [profile] [ROS_DISTRO] [VERSION_ID]"
        echo ""
        echo "Arguments:"
        echo "  profile     - Build profile (ros2, ros2cuda, isaacsim, all)"
        echo "  ROS_DISTRO  - ROS distribution (default: humble)"
        echo "  VERSION_ID  - Version identifier (default: 0.0.1)"
        echo ""
        echo "Dockerfile locations:"
        echo "  ros2:       $DOCKERFILE_ROS2"
        echo "  ros2cuda:   $DOCKERFILE_ROS2_CUDA"
        echo "  isaacsim:   $DOCKERFILE_ISAACSIM_ROS2"
        echo ""
        echo "Examples:"
        echo "  $0 ros2 humble 0.0.1"
        echo "  $0 ros2cuda foxy 1.0.0"
        echo "  $0 isaacsim galactic 2.0.0"
        echo "  $0 all humble 0.0.1"
        exit 0
        ;;
    *)
        echo "Error: Unknown profile '$PROFILE'"
        echo "Available profiles: ros2, ros2cuda, isaacsim, all"
        echo "Usage: $0 [profile] [ROS_DISTRO] [VERSION_ID]"
        exit 1
        ;;
esac

echo "Build completed successfully!"
