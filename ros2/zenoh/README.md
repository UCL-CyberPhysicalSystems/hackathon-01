# Zenoh Bridge ROS2 - Connecting UCL HereEast and Condensor/Unified AI Exmaples

This guide is a setup guide for the connection between UCL HereEast and Condensor. 

> **Note:** You will need admin knowledge of the IP Address of the UCL HereEast Machine for these instructions. 

This is intended for the admin controlled gateway VM, for VM-to-VM communication you will not need to set this up you should hopefully only be relying on ROS-to-ROS communication for intra-VM comms. The reason is that there is limited bandwidth on the HereEast connection and therefore we must minimise data duplication through that link. 

The tool is located here: https://github.com/eclipse-zenoh/zenoh-plugin-ros2dds?tab=readme-ov-file 

## Connecting to UCL HereEast Data Sources

For the connection between UCL HereEast G40 space and Condensor/Unified-AI, we need a way of transmitting data across the UCL VPN. 

> **Note:** Refer to this documentation for VPN instructions: https://www.ucl.ac.uk/isd/services/get-connected/ucl-virtual-private-network-vpn 

To do this we use the `zenoh-bridge-ros2dds` tool which listens on ros2 but sends relevant data over a TCP pipe between two locations. 

The zenoh bridge will only be needed to bridge the gap between G40 and a gateway VM within our condensor cluster. Once inside the condensor cluster on the same subnet, standard ROS2 middleware discovery and data sharing will be accessible. 


### Running the Docker container

In this folder there is a docker container with `zenoh-bridge-ros2dds` already written. You will first need to install Docker onto the VM, but once that is completed (with postinstallation steps performed):

To build use: 

```bash
docker build -t zenoh_test .
```

Then to drop you into the terminal run the following command 
```bash
docker run -it --net=host zenoh_test:latest bash
```

> **Note:** `--net=host` is only needed if you wish to communicate with other ROS docker environments, otherwise you can just expose port 7447

On the G40 Side, local sensing side, simply run `zenoh-bridge-ros2dds` and this will start a listener (note you will likely need to run this with all of your ros environments sourced if using custom messages). 

Once running, start the ros2 data streams you wish to send through 

On the Unified-AI side, spin up the container on the VM, and this time run:

```bash
zenoh-bridge-ros2dds -e tcp/${G40_MACHINE_IP}:7447
```

> **Note:** In this case the variable `${G40_MACHINE_IP}` is admin knowledge. However this setup can be replicated for other types of connections. 

In a separate terminal inside docker, you should be able to interrogate ROS using `ros2 topic list` etc. 

And that will drop you into the container, at which point follow the above examples. 

### Running Bare Metal

To set this up, make a note of the UCL VPN IP Address of the G40 Machine. 

Install zenoh bridge ros2dds (See [Linux Debian Install Instructions](https://github.com/eclipse-zenoh/zenoh-plugin-ros2dds?tab=readme-ov-file#linux-debian)):

```bash
curl -L https://download.eclipse.org/zenoh/debian-repo/zenoh-public-key | sudo gpg --dearmor --yes --output /etc/apt/keyrings/zenoh-public-key.gpg
echo "deb [signed-by=/etc/apt/keyrings/zenoh-public-key.gpg] https://download.eclipse.org/zenoh/debian-repo/ /" | sudo tee -a /etc/apt/sources.list > /dev/null
sudo apt update
sudo apt install zenoh-bridge-ros2dds
```

Once installed, in a terminal, simple run `zenoh-bridge-ros2dds` and this will start a listener (note you will likely need to run this with all of your ros environments sourced if using custom messages). 

Once running, start the ros2 data streams you wish to send through 

On the Unified-AI side, spin up your container as above, and follow the previous instructions. 

## Testing Connectivity 

First start up the zenoh bridge as above. There should be a set of stdout confirming a connection if successful. 

Then, on the G40 side, start some publishers. For this example we are just creating our own, but this could be other data too. Start a second terminal, source ros2 and run the following:

```bash
ros2 topic pub ros2 topic pub /hello std_msgs/msg/String {"data: hello"} 10.0
```

Then on the Unified-AI side VM, start a new terminal and exec into the running container e.g.

```bash
docker exec -it zenoh_test bash
```

> **Note**: Container has tmux installed if easier to use. Can run zenoh bridge and any additional commands as tmux panes/windows. 

And then see if you are getting ros data
```bash
ros2 topic list
ros2 topic echo /hello
ros2 topic hz /hello
```
You should see the topics you published on the G40 side, the contents and the message frequency should match as well. 


