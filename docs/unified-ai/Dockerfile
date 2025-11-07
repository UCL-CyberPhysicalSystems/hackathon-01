# Dockerimage for https://github.com/UCL-CyberPhysicalSystems/hackathon-01/tree/main/notebooks/potential_based_diffusion_motion_planning

FROM ghcr.io/ucl-arc-environments/kubeflow-notebook-images-jupyter-pytorch-cuda-arc:v1.0.11

# Switch to root for package installation
USER root

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


