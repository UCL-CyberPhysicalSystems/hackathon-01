# Zenoh Bridge ROS2 - Connecting UCL HereEast and Condensor/Unified AI Exmaples

This guide is a setup guide for the connection between UCL HereEast and Condensor. 

The tool is located here: https://github.com/eclipse-zenoh/zenoh-plugin-ros2dds?tab=readme-ov-file 

## Connecting to UCL HereEast Data Sources

For the connection between UCL HereEast G40 space and Condensor/Unified-AI, we need a way of transmitting data across the UCL VPN. 

To do this we use the `zenoh-bridge-ros2dds` tool which listens on ros2 but sends relevant data over a TCP pipe between two locations. 

The zenoh bridge will only be needed to bridge the gap between G40 and a gateway VM within our condensor cluster. Once inside the condensor cluster on the same subnet, standard ROS2 middleware discovery and data sharing will be accessible. 

To set this up, make a note of the UCL VPN IP Address of the G40 Machine. 

Install zenoh bridge ros2dds:

```bash
curl -L https://download.eclipse.org/zenoh/debian-repo/zenoh-public-key | sudo gpg --dearmor --yes --output /etc/apt/keyrings/zenoh-public-key.gpg
echo "deb [signed-by=/etc/apt/keyrings/zenoh-public-key.gpg] https://download.eclipse.org/zenoh/debian-repo/ /" | sudo tee -a /etc/apt/sources.list > /dev/null
sudo apt update
sudo apt install zenoh-bridge-ros2dds
```

Once installed, in a terminal, simple run `zenoh-bridge-ros2dds` and this will start a listener (note you will likely need to run this with all of your ros environments sourced if using custom messages). 

Once running, start the ros2 data streams you wish to send through 

On the Unified-AI side, spin up your `ros:humble` container

```bash
docker run -it --net=host ros:humble bash
```

Do the same installation as above, and this time run:

```bash
zenoh-bridge-ros2dds -e tcp/<g40_machine_ucl_vpn_ip>:7447
```

In a separate terminal inside docker, you should be able to interrogate ROS using `ros2 topic list` etc. 

## Running the Docker container

In this folder there is a docker container with `zenoh-bridge-ros2dds` already written.

To build use: 

```bash
docker build -t zenoh_test .
```

Then to run 
```bash
docker run -it --net=host zenoh_test:latest bash
```

And that will drop you into the container, at which point follow the above examples. 