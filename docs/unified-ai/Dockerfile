# Docker image for https://github.com/UCL-CyberPhysicalSystems/hackathon-01/tree/main/notebooks/potential_based_diffusion_motion_planning

FROM ghcr.io/ucl-arc-environments/kubeflow-notebook-images-jupyter-pytorch-cuda-arc:v1.0.11

# Switch to root for package installation
USER root

# Setup the sources
RUN apt-get update -qq && apt-get install -y software-properties-common curl && \
    add-apt-repository universe && \
    curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | tee /etc/apt/sources.list.d/ros2.list > /dev/null


# General ROS2 environment variables
ENV ROS_DISTRO=humble
ENV ROS_VERSION=2
ENV ROS_PYTHON_VERSION=3


# Install ROS 2 distro and colcon deps
RUN apt-get update -qq && apt-get upgrade -y && \
    apt-get install -y \
    ros-${ROS_DISTRO}-desktop \
    python3-colcon-common-extensions \
    && rm -rf /var/lib/apt/lists/*

# Downgrade libbrotli1 to fix compatibility issues in Isaac Sim 4.5.0
# But it might cause some issues in Isaac Sim with something like streaming or caching.
# https://forums.developer.nvidia.com/t/docker-nvcr-io-nvidia-isaac-sim-4-5-0-cant-install-ros2-humble/323574

# Install ROS2 packages
RUN apt-get update && apt-get install -y \
    ros-${ROS_DISTRO}-turtlesim \
    ros-${ROS_DISTRO}-rqt* \
    ros-${ROS_DISTRO}-xacro \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install system dependencies in a single layer with cleanup
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    bash-completion \
    cmake \
    git \
    git-core \
    tree \
    lsb-release \
    wget \
    less \
    ffmpeg \
    udev \
    curl \
    vim \
    xclip \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Upgrade pip first and set cache directory
RUN python3 -m pip install --upgrade pip setuptools wheel

# Combine Python package installations to reduce layers
RUN python3 -m pip install --no-cache-dir \
    gdown \
    GitPython \
    opencv-python \
    h5py \
    tqdm \
    gym \
    typed-argument-parser \
    termcolor \
    matplotlib \
    pybullet \
    colorama \
    pandas \
    imageio \
    scipy \
    torchvision \
    einops \
    wandb \
    mediapy \
    mediapipe \
    imageio[ffmpeg]


# ROS2 Environment Setup and sourcing
SHELL ["/bin/bash", "-c"]
RUN echo "" >> ~/.bashrc
RUN echo "## ROS2" >> ~/.bashrc
RUN echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> ~/.bashrc

# Switch to default user `$NB_UID` is defined in base image
USER $NB_UID

