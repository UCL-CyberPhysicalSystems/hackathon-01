# ROS2
> The Robot Operating System (ROS) is a set of software libraries and tools for building robot applications. From drivers and state-of-the-art algorithms to powerful developer tools, ROS has the open source tools you need for your next robotics project.
> REP 2000: https://ros.org/reps/rep-2000.html defines the timeline for future ROS 2 releases as well as the targeted platforms for each specific one. 

## Build docker images with custom parameters
Example of [build-docker.bash](build-docker.bash):
```bash
#Profiles: ros2, ros2cuda, isaacsim, all
PROFILE=ros2 && ROS_DISTRO=humble && VERSION_ID=0.1.0

bash build-docker.bash $PROFILE $ROS_DISTRO $VERSION_ID
```

## Run and test images
Once you have built docker images, you can then run your image for [basic](basic), [unified-ai](unified-ai), [cuda](cuda), [isaacsim](isaacsim).

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

## References
* https://docs.ros.org/en/foxy/index.html
* https://roboticseabass.com/2023/07/09/updated-guide-docker-and-ros2/ 
* https://faun.pub/ros2-humble-gui-docker-container-a-step-by-step-guide-c541b73fe141
