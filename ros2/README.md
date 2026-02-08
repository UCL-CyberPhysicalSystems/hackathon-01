# ROS2
> The Robot Operating System (ROS) is a set of software libraries and tools for building robot applications. From drivers and state-of-the-art algorithms to powerful developer tools, ROS has the open source tools you need for your next robotics project.

## ROS2 releases and versions
Platforms are defined in REP 2000: https://ros.org/reps/rep-2000.html
REP 2000: https://ros.org/reps/rep-2000.html defines the timeline for future ROS 2 releases as well as the targeted platforms for each specific one. 

* General ROS2 environment variables
Define the container image(s) associated with each ROS distribution.
   * Humble Hawksbill (May 2022 - May 2027); Ubuntu 22.04 Jammy; python3.10
   * Iron Irwini (May 2023 - November 2024)
   * Jazzy Jalisco (May 2024 - May 2029);  Ubuntu 24.04 Noble; python3.12

* Gazebo versions https://gazebosim.org/docs/latest/ros_installation
   * Gz Jetty > ROS 2 Rolling
   * Gz Ionic > ROS 2 Kilted
   * GZ Fortress (LTS) > ROS 2 Humble (LTS)
   * GZ Harmonic (LTS) > ROS 2 Jazzy (LTS) > Harmonic binaries are provided for Ubuntu Jammy (22.04) and Ubuntu Noble (24.04)

## Build docker images with custom parameters
Example of [build-docker.bash](build-docker.bash) where Profiles could be: ros2, network, ros2cuda, isaacsim, all.
```bash
PROFILE=ros2 && ROS_DISTRO=humble && VERSION_ID=0.0.1
PROFILE=isaacsim && ROS_DISTRO=humble && VERSION_ID=0.0.2
bash build-docker.bash $PROFILE $ROS_DISTRO $VERSION_ID
```

## Run and test images
Once you have built docker images, you can then run your image for [basic](basic), [network](network), [unified-ai](unified-ai), [cuda](cuda), [isaacsim](isaacsim).

## Useful commands

* The following are a few useful commands, for more comprehensive list see this [cheatsheet](https://www.linuxteck.com/docker-management-command-cheat-sheet/)
```bash
docker images && docker ps # that list images containers
docker exec -it <container_id> # Exececute command inside the containers
# use IMAGENAME variable to select container id for docker command execution
docker exec -it $(docker container ls  | grep '${IMAGENAME}' | awk '{print $1}')
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


## References
* https://docs.ros.org/en/humble/index.html
* https://roboticseabass.com/2023/07/09/updated-guide-docker-and-ros2/ 
* https://faun.pub/ros2-humble-gui-docker-container-a-step-by-step-guide-c541b73fe141
* https://github.com/eclipse-zenoh/zenoh-plugin-ros2dds?tab=readme-ov-file 
