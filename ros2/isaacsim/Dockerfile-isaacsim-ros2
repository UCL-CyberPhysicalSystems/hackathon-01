# Base image

ARG ISAAC_MAJOR=5
ARG ISAAC_MINOR=0
ARG ISAAC_PATCH=0

FROM nvcr.io/nvidia/isaac-sim:${ISAAC_MAJOR}.${ISAAC_MINOR}.${ISAAC_PATCH}

ENV DEBIAN_FRONTEND=noninteractive

# Set environment variables
ENV ACCEPT_EULA=Y
ENV PRIVACY_CONSENT=Y
ENV LANG=en_GB.UTF-8
ENV LC_ALL=en_GB.UTF-8

# Timezone Europe/London
ENV TZ=Europe/London
RUN ln -snf /usr/share/zoneinfo/${TZ} /etc/localtime && echo ${TZ} > /etc/timezone


# Language
RUN apt-get update && apt-get install -y locales
RUN locale-gen en_GB ${LANG}
RUN update-locale LC_ALL=${LC_ALL} LANG=${LANG}

#####################################
# Installing and setting up ROS2
#####################################

# Setup the sources
RUN apt-get update -qq && apt-get install -y software-properties-common curl && \
    add-apt-repository universe && \
    curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | tee /etc/apt/sources.list.d/ros2.list > /dev/null

# General ROS2 environment variables
ENV ROS_DISTRO=humble
ENV ROS_VERSION=2
ENV ROS_PYTHON_VERSION=3

# Install ROS 2 packages
RUN apt-get update -qq && apt-get upgrade -y && \
    apt-get install -y --allow-downgrades libbrotli1=1.0.9-2build6 \
    ros-${ROS_DISTRO}-desktop \
    && rm -rf /var/lib/apt/lists/*

# Downgrade libbrotli1 to fix compatibility issues in Isaac Sim 4.5.0
# But it might cause some issues in Isaac Sim with something like streaming or caching.
# https://forums.developer.nvidia.com/t/docker-nvcr-io-nvidia-isaac-sim-4-5-0-cant-install-ros2-humble/323574

# Install ROS2 bridge for Isaac Sim
RUN apt-get update && apt-get install -y \
    ros-${ROS_DISTRO}-ros-ign-bridge \
    ros-${ROS_DISTRO}-turtlesim \
    ros-${ROS_DISTRO}-rqt* \
    ros-${ROS_DISTRO}-xacro \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


# install bootstrap tools
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    bash-completion \
    cmake \
    gdb \
    git \
    git-core \
    gnupg2 \
    bash-completion \
    openssh-client \
    file \
    tree \
    lsb-release \
    wget \
    less \
    udev \
    sudo \
    libpng-dev \
    libgomp1 \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libmagic-mgc \
    libmagic1 \
    libxext6 \
    libxrender-dev \
    software-properties-common \
    tree \
    curl \
    vim \
    vim-gtk \
    xclip \
    zstd \
    && rm -rf /var/lib/apt/lists/*



# Set up volumes for caches and data
VOLUME ["/isaac-sim/kit/cache", "/root/.cache/ov", "/root/.cache/pip", "/root/.cache/nvidia/GLCache", "/root/.nv/ComputeCache", "/root/.nvidia-omniverse/logs", "/root/.local/share/ov/data", "/root/Documents"]

# ROS2 Environment Setup and sourcing
SHELL ["/bin/bash", "-c"]
RUN echo "" >> ~/.bashrc
RUN echo "## ROS2" >> ~/.bashrc
RUN echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> ~/.bashrc
