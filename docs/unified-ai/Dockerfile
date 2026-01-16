# Use a specific tag for reproducibility
FROM ghcr.io/ucl-arc-environments/kubeflow-notebook-images-jupyter-pytorch-cuda-arc:v1.0.11

# Switch to root for package installation
USER root

# Setup the sources
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    software-properties-common \
    curl \
    gnupg \
    ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Add ROS 2 repository
RUN curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | tee /etc/apt/sources.list.d/ros2.list > /dev/null

# Update and install essential C/C++ build tools and headers FIRST
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    gdb \
    clang \
    clang-tools \
    clang-format \
    llvm \
    llvm-dev \
    libclang-dev \
    clangd \
    pkg-config \
    libssl-dev \
    libc6-dev \
    libc++-dev \
    libc++abi-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install Rust using rustup (non-interactive mode) - installed early to leverage cargo cache
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --default-toolchain stable \
    && . "$HOME/.cargo/env" \
    && rustup update \
    && rustup component add rustfmt clippy rust-src

# Install remaining system dependencies
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    bash-completion \
    cmake \
    git \
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
    python3-colcon-common-extensions \
    ninja-build \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libudev-dev \
    libsystemd-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# General ROS2 environment variables
ENV ROS_DISTRO=humble
ENV ROS_VERSION=2
ENV ROS_PYTHON_VERSION=3
ENV PATH="/root/.cargo/bin:${PATH}"
ENV RUSTUP_HOME="/root/.rustup"
ENV CARGO_HOME="/root/.cargo"

# Install ROS 2 distro
RUN apt-get update -qq && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    ros-${ROS_DISTRO}-desktop \
    ros-${ROS_DISTRO}-rmw-fastrtps-cpp \
    ros-${ROS_DISTRO}-rmw-cyclonedds-cpp \
    && rm -rf /var/lib/apt/lists/*

# Install additional ROS2 packages
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    ros-${ROS_DISTRO}-turtlesim \
    ros-${ROS_DISTRO}-rqt \
    ros-${ROS_DISTRO}-xacro \
    ros-${ROS_DISTRO}-demo-nodes-cpp \
    ros-${ROS_DISTRO}-demo-nodes-py \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set up environment variables for clang/bindgen
ENV LIBCLANG_PATH=/usr/lib/llvm-14/lib/
ENV LLVM_CONFIG_PATH=/usr/bin/llvm-config
ENV BINDGEN_EXTRA_CLANG_ARGS="-I/usr/include -I/usr/include/x86_64-linux-gnu"

# Install bindgen dependencies and setup clang
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    llvm-14 \
    llvm-14-dev \
    llvm-14-runtime \
    libllvm14 \
    libclang-14-dev \
    clang-14 \
    && update-alternatives --install /usr/bin/clang clang /usr/bin/clang-14 100 \
    && update-alternatives --install /usr/bin/clang++ clang++ /usr/bin/clang++-14 100 \
    && update-alternatives --install /usr/bin/llvm-config llvm-config /usr/bin/llvm-config-14 100 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Clone and build zenoh-plugin-ros2dds with proper environment setup
RUN . "$HOME/.cargo/env" \
    && export LIBCLANG_PATH=$(find /usr/lib -name "libclang*.so*" | head -n1 | xargs dirname) \
    && git clone --depth 1 https://github.com/eclipse-zenoh/zenoh-plugin-ros2dds.git /tmp/zenoh-plugin-ros2dds \
    && cd /tmp/zenoh-plugin-ros2dds \
    && cargo build --release \
    && mkdir -p /usr/local/lib/zenoh \
    && find /tmp/zenoh-plugin-ros2dds/target/release -name "*.so" -exec cp {} /usr/local/lib/zenoh/ \; \
    && ldconfig \
    && rm -rf /tmp/zenoh-plugin-ros2dds \
    && echo 'export ZENOH_PLUGIN_ROS2DDS_LIBRARY_PATH="/usr/local/lib/zenoh"' >> /etc/profile.d/zenoh.sh

# Upgrade pip and install Python packages
RUN python3 -m pip install --upgrade pip setuptools wheel

# Install Python packages
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
    'imageio[ffmpeg]' \
    opencv-contrib-python \
    numpy \
    setuptools==58.2.0

# Create ROS 2 log directory and set proper permissions
RUN mkdir -p /home/jovyan/.ros/log \
    && chown -R $NB_UID:$NB_GID /home/jovyan/.ros \
    && chmod 755 /home/jovyan/.ros \
    && chmod 755 /home/jovyan/.ros/log

# Create a wrapper script to set ROS_HOME and fix permissions
RUN echo '#!/bin/bash' > /usr/local/bin/ros2 \
    && echo 'export ROS_HOME=${ROS_HOME:-/home/jovyan/.ros}' >> /usr/local/bin/ros2 \
    && echo 'export ROS_LOG_DIR=${ROS_LOG_DIR:-${ROS_HOME}/log}' >> /usr/local/bin/ros2 \
    && echo 'mkdir -p ${ROS_HOME} ${ROS_LOG_DIR}' >> /usr/local/bin/ros2 \
    && echo 'chmod 755 ${ROS_HOME} ${ROS_LOG_DIR} 2>/dev/null || true' >> /usr/local/bin/ros2 \
    && echo 'exec /opt/ros/${ROS_DISTRO}/bin/ros2 "$@"' >> /usr/local/bin/ros2 \
    && chmod +x /usr/local/bin/ros2

# Setup ROS2 environment in user's bashrc and include Rust
RUN echo "" >> /home/jovyan/.bashrc \
    && echo "## ROS2" >> /home/jovyan/.bashrc \
    && echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> /home/jovyan/.bashrc \
    && echo "export ROS_HOME=/home/jovyan/.ros" >> /home/jovyan/.bashrc \
    && echo "export ROS_LOG_DIR=/home/jovyan/.ros/log" >> /home/jovyan/.bashrc \
    && echo "" >> /home/jovyan/.bashrc \
    && echo "## Rust" >> /home/jovyan/.bashrc \
    && echo 'source "$HOME/.cargo/env"' >> /home/jovyan/.bashrc \
    && echo 'export PATH="$HOME/.cargo/bin:${PATH}"' >> /home/jovyan/.bashrc \
    && echo "" >> /home/jovyan/.bashrc \
    && echo "## Zenoh" >> /home/jovyan/.bashrc \
    && echo 'export ZENOH_PLUGIN_ROS2DDS_LIBRARY_PATH="/usr/local/lib/zenoh"' >> /home/jovyan/.bashrc \
    && echo 'export LD_LIBRARY_PATH="/usr/local/lib/zenoh:${LD_LIBRARY_PATH}"' >> /home/jovyan/.bashrc \
    && echo "" >> /home/jovyan/.bashrc \
    && echo "## Fix for ROS 2 logging" >> /home/jovyan/.bashrc \
    && echo 'mkdir -p $ROS_HOME $ROS_LOG_DIR 2>/dev/null || true' >> /home/jovyan/.bashrc

# Create symbolic links for ROS 2 DDS plugins
RUN mkdir -p /opt/ros/${ROS_DISTRO}/lib/rmw_zenoh \
    && find /usr/local/lib/zenoh -name "*.so" -exec ln -sf {} /opt/ros/${ROS_DISTRO}/lib/rmw_zenoh/ \; \
    && echo 'export RMW_IMPLEMENTATION=rmw_zenoh' >> /etc/profile.d/ros_zenoh.sh

# Switch back to default user (jovyan in Jupyter images)
USER $NB_UID

# Set working directory
WORKDIR /home/jovyan

# Default command
CMD ["/bin/bash"]
