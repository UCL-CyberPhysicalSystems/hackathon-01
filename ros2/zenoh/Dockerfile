FROM ros:humble

RUN apt-get update && apt-get install -y \
        python3-pip \
        cmake \
        curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -L https://download.eclipse.org/zenoh/debian-repo/zenoh-public-key | sudo gpg --dearmor --yes --output /etc/apt/keyrings/zenoh-public-key.gpg \
    && echo "deb [signed-by=/etc/apt/keyrings/zenoh-public-key.gpg] https://download.eclipse.org/zenoh/debian-repo/ /" | sudo tee -a /etc/apt/sources.list > /dev/null \
    && apt-get update && apt-get install -y \
        zenoh-bridge-ros2dds \
    && rm -rf /var/lib/apt/lists/*