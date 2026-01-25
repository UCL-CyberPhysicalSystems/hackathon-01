# Use Ubuntu LTS with explicit version for reproducibility
FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    ACCEPT_EULA=Y \
    PRIVACY_CONSENT=Y \
    LANG=en_GB.UTF-8 \
    LC_ALL=en_GB.UTF-8 \
    TZ=Europe/London \
    ROS_DISTRO=humble \
    ROS_VERSION=2 \
    ROS_PYTHON_VERSION=3 \
    SHELL=/bin/bash

# Set non-interactive for tzdata
ENV DEBCONF_NOWARNINGS=yes

# Configure timezone, locales, and install minimal packages in a single RUN layer
RUN set -eux && \
    ln -snf /usr/share/zoneinfo/${TZ} /etc/localtime && \
    echo ${TZ} > /etc/timezone && \
    # Configure apt for better caching and faster downloads
    echo 'Acquire::Languages "none";' > /etc/apt/apt.conf.d/99translations && \
    echo 'Acquire::GzipIndexes "true";' > /etc/apt/apt.conf.d/99gzipindexes && \
    echo 'Acquire::CompressionTypes::Order:: "gz";' > /etc/apt/apt.conf.d/99compressbydefault && \
    # Install locales and tzdata
    apt-get update && \
    apt-get install -y --no-install-recommends \
        locales \
        tzdata \
        ca-certificates && \
    locale-gen en_GB.UTF-8 && \
    update-locale LC_ALL=${LC_ALL} LANG=${LANG} && \
    # Clean up
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install essential system packages and dependencies
RUN set -eux && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        apt-utils \
        curl \
        gnupg \
        lsb-release \
        software-properties-common \
        wget \
        unzip \
        dirmngr \
        # Add gpg for key management
        gpg \
        gpg-agent && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install X11 and Qt5 packages for GUI support
RUN set -eux && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        # Core X11 server components
        xserver-xorg-core \
        xserver-xorg-input-evdev \
        # Essential X11 utilities
        x11-utils \
        x11-xserver-utils \
        xauth \
        xinit \
        # X11 VNC for remote display
        x11vnc \
        dbus-x11 \
        # Core Qt5 development and runtime
        qtbase5-dev \
        qtchooser \
        qt5-qmake \
        qtbase5-dev-tools \
        libqt5core5a \
        libqt5gui5 \
        libqt5widgets5 \
        libqt5dbus5 \
        libqt5network5 \
        libqt5svg5 \
        libqt5x11extras5 \
        libqt5opengl5 \
        # XCB libraries for Qt X11 support
        libx11-xcb1 \
        libxcb1 \
        libxcb-randr0 \
        libxcb-xfixes0 \
        libxcb-xkb1 \
        libxcb-keysyms1 \
        libxcb-render-util0 \
        libxcb-xinerama0 \
        # Essential X11 development libraries
        libx11-dev \
        libxext-dev \
        libxfixes-dev \
        libxi-dev \
        libxrandr-dev \
        libxtst-dev \
        libxv-dev \
        # X11 runtime libraries
        libglib2.0-0 \
        libsm6 \
        libxext6 \
        libxrender1 \
        libxi6 \
        libxrandr2 \
        libxfixes3 \
        libxcursor1 \
        libxinerama1 \
        libxcomposite1 \
        # Basic fonts for GUI
        fonts-dejavu-core \
        fonts-liberation \
        fonts-noto \
        fonts-noto-cjk \
        # Audio support
        libpulse0 \
        libasound2 \
        # Input support
        libevdev2 && \
    # Configure qtchooser to use qt5
    update-alternatives --install /usr/bin/qmake qmake /usr/lib/x86_64-linux-gnu/qt5/bin/qmake 100 && \
    update-alternatives --install /usr/bin/moc moc /usr/lib/x86_64-linux-gnu/qt5/bin/moc 100 && \
    update-alternatives --install /usr/bin/uic uic /usr/lib/x86_64-linux-gnu/qt5/bin/uic 100 && \
    update-alternatives --install /usr/bin/rcc rcc /usr/lib/x86_64-linux-gnu/qt5/bin/rcc 100 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


# Install bindgen dependencies and setup clang with specific version
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        llvm-14 \
        llvm-14-dev \
        llvm-14-runtime \
        libllvm14 \
        libclang-14-dev \
        clang-14 \
        lld-14 && \
    update-alternatives --install /usr/bin/clang clang /usr/bin/clang-14 100 && \
    update-alternatives --install /usr/bin/clang++ clang++ /usr/bin/clang++-14 100 && \
    update-alternatives --install /usr/bin/llvm-config llvm-config /usr/bin/llvm-config-14 100 && \
    update-alternatives --install /usr/bin/llvm-symbolizer llvm-symbolizer /usr/bin/llvm-symbolizer-14 100 && \
    update-alternatives --install /usr/bin/lld lld /usr/bin/lld-14 100 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Setup ROS2 repository with proper key handling
RUN set -eux && \
    # Create directory for keys
    mkdir -p /usr/share/keyrings && \
    # Download and install ROS key
    curl -fsSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /tmp/ros.key && \
    gpg --dearmor < /tmp/ros.key > /usr/share/keyrings/ros-archive-keyring.gpg && \
    # Add ROS repository
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" > /etc/apt/sources.list.d/ros2.list && \
    rm -f /tmp/ros.key

# Setup Gazebo transport repository
RUN set -eux && \
    # Download and install Gazebo key
    curl -fsSL https://packages.osrfoundation.org/gazebo.key | gpg --dearmor > /usr/share/keyrings/gazebo-archive-keyring.gpg && \
    # Add Gazebo repository
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/gazebo-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" > /etc/apt/sources.list.d/gazebo-stable.list

# Install zenoh-bridge-ros2dds
RUN mkdir -p /etc/apt/keyrings \
    && curl -L https://download.eclipse.org/zenoh/debian-repo/zenoh-public-key | gpg --dearmor --yes --output /etc/apt/keyrings/zenoh-public-key.gpg \
    && echo "deb [signed-by=/etc/apt/keyrings/zenoh-public-key.gpg] https://download.eclipse.org/zenoh/debian-repo/ /" | tee -a /etc/apt/sources.list > /dev/null \
    && apt-get update && apt-get install -y \
        zenoh-bridge-ros2dds \
    && rm -rf /var/lib/apt/lists/*


# Install ROS2 desktop and development tools
RUN set -eux && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        # ROS2 core and desktop
        ros-${ROS_DISTRO}-desktop \
        # Essential ROS2 packages
        ros-${ROS_DISTRO}-ros-core \
        ros-${ROS_DISTRO}-turtlesim \
        ros-${ROS_DISTRO}-xacro \
        ros-${ROS_DISTRO}-rmw-cyclonedds-cpp \
        # RQT core tools
        ros-${ROS_DISTRO}-rqt \
        ros-${ROS_DISTRO}-rqt-common-plugins \
        # Build and development tools
        python3-colcon-common-extensions \
        python3-colcon-cd \
        python3-colcon-cmake \
        python3-colcon-ros \
        build-essential \
        cmake \
        git \
        python3-pip \
        python3-dev \
        # Python development
        python3-setuptools \
        python3-wheel \
        # System utilities
        bash-completion \
        file \
        less \
        sudo \
        tree \
        vim \
        nano \
        htop \
        tmux \
        # Graphics dependencies
        libgl1-mesa-glx \
        libglib2.0-0 \
        libgomp1 \
        libsm6 \
        libxext6 \
        libxrender-dev \
        libpng-dev \
        libegl1 \
        libgtk-3-0 \
        libopencv-dev \
        # Network and USB
        udev \
        openssh-client \
        net-tools \
        iputils-ping \
        iperf3 \
        # Python packages
        python3-argcomplete \
        python3-vcstool \
        # Gazebo transport
        libgz-transport13-dev \
        python3-gz-transport13 \
        # Additional tools for ROS development
        libasio-dev \
        libtinyxml2-dev \
        libyaml-cpp-dev \
        libbullet-dev \
        libeigen3-dev \
        liblog4cxx-dev \
        libconsole-bridge-dev && \
    # Install additional RQT tools that are commonly useful
    apt-get install -y --no-install-recommends \
        ros-${ROS_DISTRO}-rqt-graph \
        ros-${ROS_DISTRO}-rqt-topic \
        ros-${ROS_DISTRO}-rqt-service-caller \
        ros-${ROS_DISTRO}-rqt-console \
        ros-${ROS_DISTRO}-rqt-shell \
        ros-${ROS_DISTRO}-rqt-image-view \
        ros-${ROS_DISTRO}-rqt-plot \
        2>/dev/null || true && \
    # Clean up
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install additional Python packages
RUN set -eux && \
    pip3 install --no-cache-dir --upgrade \
        pip \
        setuptools \
        wheel && \
    pip3 install --no-cache-dir \
        argcomplete \
        catkin_pkg \
        empy \
        lark \
        # Development tools
        pre-commit \
        # Testing
        pytest \
        pytest-cov \
        pytest-html \
        pytest-repeat \
        pytest-xdist \
        # Utilities
        ipython \
        numpy \
        pandas \
        matplotlib \
        seaborn \
        # ROS tools
        rosdep \
        rosinstall_generator \
        vcstool \
        # Build tools
        colcon-bundle \
        colcon-cmake \
        colcon-core \
        # Zenoh Python bindings
        eclipse-zenoh==1.5.0 \
        pycdr2 \
        zenoh && \
    # Initialize rosdep
    rosdep init 2>/dev/null || true && \
    rm -rf /root/.cache/pip

# Create a non-root user with proper UID/GID handling
ARG USERNAME=rosuser
ARG USER_UID=1000
ARG USER_GID=1000

RUN set -eux && \
    # Create group if it doesn't exist
    if ! getent group ${USER_GID} >/dev/null; then \
        groupadd --gid ${USER_GID} ${USERNAME}; \
    fi && \
    # Create user
    useradd --uid ${USER_UID} --gid ${USER_GID} --shell /bin/bash -m ${USERNAME} && \
    # Add to sudoers without password for convenience in development
    echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/${USERNAME} && \
    chmod 0440 /etc/sudoers.d/${USERNAME} && \
    # Create common directories
    mkdir -p /home/${USERNAME}/.local/bin && \
    mkdir -p /home/${USERNAME}/ros2_ws/src && \
    mkdir -p /home/${USERNAME}/.cargo && \
    # Setup cargo directory for user
    ln -sf /opt/cargo /home/${USERNAME}/.cargo && \
    ln -sf /opt/rustup /home/${USERNAME}/.rustup && \
    chown -R ${USER_UID}:${USER_GID} /home/${USERNAME}

# Setup bash environment - FIXED: Using cat with HEREDOC to avoid quoting issues
RUN cat << 'EOF' > /etc/bash.bashrc

# ROS2 Environment
if [ -f /opt/ros/${ROS_DISTRO}/setup.bash ]; then
    source /opt/ros/${ROS_DISTRO}/setup.bash
fi

# Colcon bash completion
if [ -f /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash ]; then
    source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash
fi

# Python argcomplete
if command -v register-python-argcomplete &> /dev/null; then
    eval "$(register-python-argcomplete colcon)"
fi

# Rust environment
if [ -f /opt/cargo/env ]; then
    source /opt/cargo/env
fi

# Zenoh plugin environment
if [ -f /etc/profile.d/zenoh.sh ]; then
    source /etc/profile.d/zenoh.sh
fi

# Color prompt with ROS distro info
export PS1='\[\e[1;32m\][\u@\h:\w]\[\e[1;36m\][${ROS_DISTRO}]\[\e[1;33m\][Rust]\[\e[0m\]\$ '

# Set default editor
export EDITOR=vim

# Improve terminal experience
export TERM=xterm-256color

# History configuration
export HISTSIZE=10000
export HISTFILESIZE=20000
export HISTCONTROL=ignoreboth
shopt -s histappend

# Aliases for convenience
alias ll="ls -la --color=auto"
alias la="ls -A --color=auto"
alias l="ls -CF --color=auto"
alias ..="cd .."
alias ...="cd ../.."
alias cw="cd ~/ros2_ws"
alias cs="cd ~/ros2_ws/src"
alias cb="cd ~/ros2_ws && colcon build --symlink-install"
alias cbr="cd ~/ros2_ws && colcon build --symlink-install && source install/setup.bash"
alias ct="cd ~/ros2_ws && colcon test"
alias cr="cd ~/ros2_ws && colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release"
alias cbrt="cd ~/ros2_ws && colcon build --symlink-install --packages-select"

# Rust aliases
alias rs="cargo run"
alias rb="cargo build"
alias rt="cargo test"
alias rfmt="cargo fmt"
alias rclippy="cargo clippy -- -D warnings"

# Function to source workspace
srcws() {
    if [ -f "install/setup.bash" ]; then
        source install/setup.bash
        echo "✓ Sourced current workspace"
    elif [ -f "../install/setup.bash" ]; then
        source ../install/setup.bash
        echo "✓ Sourced parent workspace"
    elif [ -f "../../install/setup.bash" ]; then
        source ../../install/setup.bash
        echo "✓ Sourced grandparent workspace"
    else
        echo "✗ No install/setup.bash found in current or parent directories"
        return 1
    fi
}

# Function to create new ROS2 package
newpkg() {
    if [ -z "$1" ]; then
        echo "Usage: newpkg <package_name> [dependencies...]"
        return 1
    fi
    local pkg_name=$1
    shift
    cd ~/ros2_ws/src
    ros2 pkg create $pkg_name --build-type ament_cmake $@
    cd ~/ros2_ws
    echo "Created package: $pkg_name"
}

# Check if workspace is sourced
wscheck() {
    if [ -n "$COLCON_PREFIX_PATH" ]; then
        echo "✓ Workspace is sourced: $COLCON_PREFIX_PATH"
    else
        echo "✗ No workspace is currently sourced"
    fi
}

# ROS doctor alias
alias doctor="ros2 doctor --report-warnings"

# Git status for ROS workspace
rosgit() {
    cd ~/ros2_ws
    for dir in src/*/; do
        if [ -d "$dir/.git" ]; then
            echo -e "\n\e[1;34m$(basename $dir)\e[0m"
            git -C "$dir" status --short --branch
        fi
    done
    cd - >/dev/null
}

# Clear ROS logs
clearlogs() {
    rm -rf ~/.ros/log/*
    echo "Cleared ROS logs"
}

# Quick build and test
qbt() {
    local package=$1
    if [ -z "$package" ]; then
        echo "Usage: qbt <package_name>"
        return 1
    fi
    colcon build --symlink-install --packages-select $package
    if [ $? -eq 0 ]; then
        source install/setup.bash
        colcon test --packages-select $package
        colcon test-result --verbose
    fi
}
EOF

# Create entrypoint script
RUN cat << 'EOF' > /entrypoint.sh
#!/bin/bash
set -e

# Source Rust environment
if [ -f /opt/cargo/env ]; then
    source /opt/cargo/env
fi

# Source ROS environment
if [ -f /opt/ros/${ROS_DISTRO}/setup.bash ]; then
    source /opt/ros/${ROS_DISTRO}/setup.bash
fi

# Source Zenoh plugin environment
if [ -f /etc/profile.d/zenoh.sh ]; then
    source /etc/profile.d/zenoh.sh
fi

# Source workspace if it exists
if [ -f "/home/${USERNAME}/ros2_ws/install/setup.bash" ]; then
    source "/home/${USERNAME}/ros2_ws/install/setup.bash"
fi

# If no command is provided, start bash
if [ $# -eq 0 ]; then
    exec /bin/bash
else
    # Execute the command passed to the container
    exec "$@"
fi
EOF

RUN chmod +x /entrypoint.sh

# Copy bashrc to user's home and set proper permissions
RUN cp /etc/bash.bashrc /home/${USERNAME}/.bashrc && \
    chown ${USER_UID}:${USER_GID} /home/${USERNAME}/.bashrc && \
    chown ${USER_UID}:${USER_GID} /entrypoint.sh

# Create a .profile for login shells
RUN cat << 'EOF' > /home/${USERNAME}/.profile

# Include .bashrc if it exists
if [ -f "$HOME/.bashrc" ]; then
    . "$HOME/.bashrc"
fi

# Add user's local bin to PATH
export PATH="$HOME/.local/bin:$PATH"
EOF

RUN chown ${USER_UID}:${USER_GID} /home/${USERNAME}/.profile

# Create a setup script for first-time users
RUN cat << 'EOF' > /home/${USERNAME}/setup_workspace.sh
#!/bin/bash
echo "Setting up ROS2 workspace..."

# Create workspace structure
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws

# Initialize workspace if not already done
if [ ! -f src/CMakeLists.txt ]; then
    colcon build --symlink-install
    source install/setup.bash
fi

echo "Workspace setup complete!"
echo "Commands:"
echo "  cw  - Go to workspace"
echo "  cs  - Go to src directory"
echo "  cb  - Build workspace"
echo "  cbr - Build and source workspace"
echo "  srcws - Source current workspace"
EOF

RUN chmod +x /home/${USERNAME}/setup_workspace.sh && \
    chown ${USER_UID}:${USER_GID} /home/${USERNAME}/setup_workspace.sh

# Switch to non-root user
USER ${USERNAME}
WORKDIR /home/${USERNAME}

# Set up volume for persistent workspace
VOLUME ["/home/${USERNAME}/ros2_ws"]

# Health check to ensure ROS is working
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD ros2 doctor --report-warnings 2>&1 | grep -q "All 6 checks passed" || exit 1

# Set entrypoint and default command
ENTRYPOINT ["/entrypoint.sh"]
CMD ["bash"]