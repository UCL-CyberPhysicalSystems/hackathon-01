#!/bin/bash

# Docker build script with configurable ROS distribution and version
# Usage: ./build-docker.bash [profile] [ROS_DISTRO] [VERSION_ID]

set -euo pipefail  # Exit on error, undefined variables, and pipe failures

# ==================== CONFIGURATION ====================
readonly SCRIPT_NAME="$(basename "$0")"
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Default values
DEFAULT_PROFILE="ros2"
DEFAULT_ROS_DISTRO="humble"
DEFAULT_VERSION_ID="0.0.1"

# Dockerfile paths
declare -A DOCKERFILE_PATHS=(
    ["ros2"]="basic/Dockerfile-ros2"
    ["network"]="network/Dockerfile"
    ["ros2cuda"]="cuda/Dockerfile-ros2-cuda"
    ["isaacsim"]="isaacsim/Dockerfile-isaacsim-ros2"
)

# Docker image tags
declare -A IMAGE_TAGS=(
    ["ros2"]="ros2:${ROS_DISTRO:-$DEFAULT_ROS_DISTRO}-${VERSION_ID:-$DEFAULT_VERSION_ID}"
    ["network"]="ros2:network-${ROS_DISTRO:-$DEFAULT_ROS_DISTRO}-${VERSION_ID:-$DEFAULT_VERSION_ID}"
    ["ros2cuda"]="ros2:cuda-${ROS_DISTRO:-$DEFAULT_ROS_DISTRO}-${VERSION_ID:-$DEFAULT_VERSION_ID}"
    ["isaacsim"]="isaacsim-${ROS_DISTRO:-$DEFAULT_ROS_DISTRO}-${VERSION_ID:-$DEFAULT_VERSION_ID}"
)

# ==================== FUNCTIONS ====================

print_usage() {
    cat << EOF
Usage: $SCRIPT_NAME [profile] [ROS_DISTRO] [VERSION_ID]

Build Docker images for ROS2 with various profiles.

Arguments:
  profile     - Build profile (ros2, network, ros2cuda, isaacsim, all)
  ROS_DISTRO  - ROS distribution (default: $DEFAULT_ROS_DISTRO)
  VERSION_ID  - Version identifier (default: $DEFAULT_VERSION_ID)

Available profiles:
  ros2        - Basic ROS2 image
  network - ROS2 with network tools
  ros2cuda    - ROS2 with CUDA support
  isaacsim    - Isaac Sim with ROS2
  all         - Build all profiles

Dockerfile locations:
  ros2:       ${DOCKERFILE_PATHS[ros2]}
  network: ${DOCKERFILE_PATHS[network]}
  ros2cuda:   ${DOCKERFILE_PATHS[ros2cuda]}
  isaacsim:   ${DOCKERFILE_PATHS[isaacsim]}

Examples:
  $SCRIPT_NAME ros2 humble 0.0.1
  $SCRIPT_NAME ros2cuda foxy 1.0.0
  $SCRIPT_NAME isaacsim galactic 2.0.0
  $SCRIPT_NAME all humble 0.0.1
  $SCRIPT_NAME --help
EOF
}

print_error() {
    echo -e "\033[1;31mError: $1\033[0m" >&2
}

print_success() {
    echo -e "\033[1;32m$1\033[0m"
}

print_info() {
    echo -e "\033[1;34m$1\033[0m"
}

check_dockerfile() {
    local profile="$1"
    local dockerfile_path="${DOCKERFILE_PATHS[$profile]}"
    
    if [[ ! -f "$dockerfile_path" ]]; then
        print_error "Dockerfile not found for '$profile' profile: $dockerfile_path"
        return 1
    fi
    
    if [[ ! -r "$dockerfile_path" ]]; then
        print_error "Dockerfile is not readable: $dockerfile_path"
        return 1
    fi
}

check_docker_installed() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed or not in PATH"
        return 1
    fi
    
    if ! docker info &> /dev/null; then
        print_error "Docker daemon is not running or you don't have permission"
        return 1
    fi
}

build_image() {
    local profile="$1"
    local ros_distro="$2"
    local version_id="$3"
    
    print_info "Building $profile image..."
    print_info "  ROS_DISTRO: $ros_distro"
    print_info "  VERSION_ID: $version_id"
    
    local dockerfile_path="${DOCKERFILE_PATHS[$profile]}"
    local image_tag
    
    # Generate image tag with actual values
    case "$profile" in
        "ros2")
            image_tag="ros2-${ros_distro}:${version_id}"
            ;;
        "network")
            image_tag="ros2-network-${ros_distro}:${version_id}"
            ;;
        "ros2cuda")
            image_tag="ros2cuda-${ros_distro}:${version_id}"
            ;;
        "isaacsim")
            image_tag="isaacsim-${ros_distro}:${version_id}"
            ;;
    esac
    
    print_info "  Image tag: $image_tag"
    print_info "  Dockerfile: $dockerfile_path"
    
    # Build with progress output (progress=plain) and cache
    if docker build \
        --tag "$image_tag" \
        --file "$dockerfile_path" \
        --build-arg ROS_DISTRO="$ros_distro" \
        --build-arg VERSION_ID="$version_id" \
        --progress=plain \
        .; then
        print_success "Successfully built $image_tag"
    else
        print_error "Failed to build $profile image"
        return 1
    fi
}

# ==================== MAIN SCRIPT ====================

main() {
    # Parse command line arguments
    local PROFILE="${1:-$DEFAULT_PROFILE}"
    local ROS_DISTRO="${2:-$DEFAULT_ROS_DISTRO}"
    local VERSION_ID="${3:-$DEFAULT_VERSION_ID}"
    
    # Validate ROS distribution
    local valid_distros=("foxy" "galactic" "humble" "iron" "rolling" "jazzy")
    if [[ ! " ${valid_distros[*]} " =~ " ${ROS_DISTRO} " ]]; then
        print_warning "Note: $ROS_DISTRO is not in the typical ROS2 distribution list"
    fi
    
    # Check if Docker is available
    if ! check_docker_installed; then
        exit 1
    fi
    
    # Handle special cases
    case "$PROFILE" in
        "-h"|"--help")
            print_usage
            exit 0
            ;;
        "all")
            print_info "Building all images with ROS_DISTRO=$ROS_DISTRO, VERSION_ID=$VERSION_ID"
            
            # Build each profile
            for profile in "ros2" "network" "ros2cuda" "isaacsim"; do
                echo ""
                echo "========================================"
                if check_dockerfile "$profile"; then
                    build_image "$profile" "$ROS_DISTRO" "$VERSION_ID" || {
                        print_error "Stopping build process due to error in $profile"
                        exit 1
                    }
                fi
            done
            ;;
        *)
            # Validate profile
            if [[ -z "${DOCKERFILE_PATHS[$PROFILE]:-}" ]]; then
                print_error "Unknown profile '$PROFILE'"
                echo ""
                print_usage
                exit 1
            fi
            
            # Check Dockerfile exists
            if ! check_dockerfile "$PROFILE"; then
                exit 1
            fi
            
            # Build single profile
            build_image "$PROFILE" "$ROS_DISTRO" "$VERSION_ID"
            ;;
    esac
    
    # Final summary
    echo ""
    print_success "Build process completed!"
    
    # Show built images
    if [[ "$PROFILE" == "all" ]]; then
        echo ""
        print_info "Built images:"
        docker images | grep -E "(ros2|isaac_sim_ros2)" | head -10
    fi
}

# Run main function with all arguments
main "$@"
