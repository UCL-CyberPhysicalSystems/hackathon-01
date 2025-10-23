#!/bin/bash

# Simple Docker build script
# Usage: bash build-docker.bash [profile]

set -e  # Exit on error

case "$1" in
    "ros2")
        echo "Building ROS2 base image..."
        docker build -t ros:two -f Dockerfile-ros2 .
        ;;
    "ros2-cuda")
        echo "Building ROS2 with CUDA..."
        docker build -t ros2:cuda -f Dockerfile-ros2-cuda .
        ;;
    "isaac-sim")
        echo "Building Isaac Sim with ROS2..."
        docker build -t isaac_sim_ros2:5.0.0-Humble -f Dockerfile-isaacsim-ros2 .
        ;;
    "all")
        echo "Building all images..."
        docker build -t ros:two -f Dockerfile-ros2 .
        docker build -t ros2:cuda -f Dockerfile-ros2-cuda .
        docker build -t isaac_sim_ros2:5.0.0-Humble -f Dockerfile-isaacsim-ros2 .
        ;;
    ""|"-h"|"--help")
        echo "Usage: $0 [profile]"
        echo "Profiles: ros2, ros2-cuda, isaac-sim, all"
        exit 1
        ;;
    *)
        echo "Error: Unknown profile '$1'"
        echo "Available profiles: ros2, ros2-cuda, isaac-sim, all"
        exit 1
        ;;
esac

echo "Build completed successfully!"

