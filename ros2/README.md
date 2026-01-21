# ROS2
> The Robot Operating System (ROS) is a set of software libraries and tools for building robot applications. From drivers and state-of-the-art algorithms to powerful developer tools, ROS has the open source tools you need for your next robotics project.
> REP 2000: https://ros.org/reps/rep-2000.html defines the timeline for future ROS 2 releases as well as the targeted platforms for each specific one. 

## Build docker images with custom parameters
Example of [build-docker.bash](build-docker.bash) where Profiles could be: ros2, network, ros2cuda, isaacsim, all.
```bash
PROFILE=ros2 && ROS_DISTRO=humble && VERSION_ID=0.0.1
bash build-docker.bash $PROFILE $ROS_DISTRO $VERSION_ID
```

## Run and test images
Once you have built docker images, you can then run your image for [basic](basic), [network](network), [unified-ai](unified-ai), [cuda](cuda), [isaacsim](isaacsim).

## Useful commands

* The following are a few useful commands, for more comprehensive list see this [cheatsheet](https://www.linuxteck.com/docker-management-command-cheat-sheet/)
```bash
docker images && docker ps # that list images containers
docker exec -it <container_id> # Exececute command inside the containers
docker exec -it $(docker container ls  | grep '${IMAGENAME}' | awk '{print $1}') # use IMAGENAME variable to select container id for docker command execution
docker rmi --force <ID> # remove docker images
docker system prune -f --volumes # free up disk space
```

* rosdep-init
```bash
ROS_DISTRO=humble
rosdep fix-permissions
rosdep init
rosdep update --rosdistro ${ROS_DISTRO}
rosdep install --from-paths src --ignore-src -r -y --rosdistro ${ROS_DISTRO}
colcon build --symlink-install
source install/setup.bash
```
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

> **Note**: there are many options which we have not explored with this bridge, but this should do for now. See instructions for further details. 


## References
* https://docs.ros.org/en/humble/index.html
* https://roboticseabass.com/2023/07/09/updated-guide-docker-and-ros2/ 
* https://faun.pub/ros2-humble-gui-docker-container-a-step-by-step-guide-c541b73fe141
* https://github.com/eclipse-zenoh/zenoh-plugin-ros2dds?tab=readme-ov-file 
