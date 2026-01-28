# Zenoh Bridge ROS 2: Connecting UCL HereEast and Condenser/Unified AI

This guide explains how to connect **UCL HereEast (bare‑metal compute)** with **Condenser/Unified AI (virtual machines)** using the [`zenoh-plugin-ros2dds`](https://github.com/eclipse-zenoh/zenoh-plugin-ros2dds).

The setup is intended for an **admin‑controlled gateway VM** and for anyone from ARC UCL staff for **VM‑to‑VM communication inside Condenser**.

> **Notes**
> The HereEast link has limited bandwidth. Using a single gateway bridge avoids unnecessary data duplication across the VPN.

---

## Architecture overview

* **Source**: UCL HereEast G40 machine (Drummond)
* **Transport**: UCL VPN + TCP
* **Bridge**: `zenoh-bridge-ros2dds`
* **Destination**: Gateway VM inside the Condenser cluster
* **Inside Condenser**: Native ROS 2 discovery and communication

Only the **G40 ↔ gateway VM** hop requires Zenoh. Everything downstream remains pure ROS 2.

---

## Prerequisites

* Access to **UCL VPN**

  * VPN instructions: [https://www.ucl.ac.uk/isd/services/get-connected/ucl-virtual-private-network-vpn](https://www.ucl.ac.uk/isd/services/get-connected/ucl-virtual-private-network-vpn)
* Admin access to:

  * The **G40 machine IP address** (on the UCL VPN)
  * A **gateway VM** in the Condenser cluster
* Docker installed on both sides
* ROS 2 (Humble or compatible)

---

## Connecting to UCL HereEast data sources (G40 / Drummond)

To transmit ROS 2 data from the G40 space to Condenser across the UCL VPN, we use:

* `zenoh-bridge-ros2dds`

This tool:

* Listens to ROS 2 topics locally
* Forwards selected traffic over a **TCP connection**

Once traffic reaches the Condenser subnet, standard ROS 2 middleware handles discovery and transport.

> **Note**
> You must know the **UCL VPN IP address of the G40 machine** to complete this setup.

---

## Running the Docker container on the G40 machine

A Docker image is provided in this directory: [`Dockerfile`](Dockerfile). It builds `zenoh-bridge-ros2dds` following the official [Linux (Debian) install instructions](https://github.com/eclipse-zenoh/zenoh-plugin-ros2dds?tab=readme-ov-file#linux-debian).

### Build the image

```bash
docker build -t zenoh_test .
```

### Run the container

```bash
docker run -it --net=host zenoh_test:latest bash
```

> **Note**
> `--net=host` is only required if you want to communicate with other ROS containers on the host. Otherwise, exposing port `7447` explicitly is sufficient.

---

## Running `zenoh-bridge-ros2dds` on the G40 machine

1. **Record the G40 VPN IP address**.

2. **Set a consistent ROS domain ID**:

   ```bash
   export ROS_DOMAIN_ID=2
   ```

3. **Start the Zenoh bridge**:

   ```bash
   zenoh-bridge-ros2dds
   ```

4. **Launch the ROS 2 nodes** that publish the data you want to forward.

5. The bridge will now listen for ROS 2 traffic and wait for incoming TCP connections from Condenser.

---

## Connecting from the Condenser gateway VM

On the gateway VM, the Zenoh bridge actively connects back to the G40 machine.

```bash
zenoh-bridge-ros2dds -e tcp/${G40_MACHINE_IP}:7447 -d 2
```

Where:

* `${G40_MACHINE_IP}` is the VPN IP of the G40 machine
* `-d 2` matches the `ROS_DOMAIN_ID`

This pattern can be reused for other remote sources if required.

---

## Working inside Condenser virtual machines

### 1. Connect to the VM (with X11 forwarding)

```bash
IP2=00.000.00.4
ssh -Y -J condenser ubuntu@${IP2}  # example: cyber-physical-lab-2
```

### 2. Pull the ROS 2 container image (if needed)

Follow the instructions here:

* [https://github.com/UCL-CyberPhysicalSystems/hackathon-01/tree/main/ros2/condenser#pull-image](https://github.com/UCL-CyberPhysicalSystems/hackathon-01/tree/main/ros2/condenser#pull-image)

### 3. Start the ROS 2 container

```bash
wget https://raw.githubusercontent.com/UCL-CyberPhysicalSystems/hackathon-01/refs/heads/main/ros2/network/run-ros2.bash
GITHUB_USERNAME=mxochicale PROJECT_NAME=ros2condenser VERSION_ID=0.0.3 bash run-ros2.bash
```

### 4. Verify ROS 2 topics

Inside the container, open a separate terminal and run:

```bash
export ROS_DOMAIN_ID=2
ros2 topic list
ros2 topic echo /livox/lidar_IP
ros2 run rviz2 rviz2
```

You should see:

* The same topics published on the G40 side
* Matching message contents and frequencies

---

## Visualising data with RViz2

[RViz2](https://docs.ros.org/en/humble/Tutorials/Intermediate/RViz/RViz-User-Guide/RViz-User-Guide.html) can be used to visualise 3D sensor data forwarded through Zenoh.

Tips:

* Use **tmux** to manage multiple terminals (bridge, ROS nodes, debugging tools):

  * [https://github.com/tmux/tmux/wiki/Getting-Started](https://github.com/tmux/tmux/wiki/Getting-Started)
* Keep the Zenoh bridge running in a dedicated pane or window

