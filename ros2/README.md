# ROS2
> The Robot Operating System (ROS) is a set of software libraries and tools for building robot applications. From drivers and state-of-the-art algorithms to powerful developer tools, ROS has the open source tools you need for your next robotics project.
> REP 2000: https://ros.org/reps/rep-2000.html defines the timeline for future ROS 2 releases as well as the targeted platforms for each specific one. 

## Build docker images with custom parameters
Example of [build-docker.bash](build-docker.bash):
```bash
PROFILE=ros2 #Profiles: ros2, ros2cuda, isaacsim, all
ROS_DISTRO=humble
VERSION_ID=0.0.1
bash build-docker.bash $PROFILE $ROS_DISTRO $VERSION_ID
```

## Run and test images
Once you have built docker images, you can then run your image for [basic](basic), [cuda](cuda), [isaacsim](isaacsim).

## Useful commands

* docker commands: images, ps, stop, remove
```bash
docker images && docker ps
docker exec -it <container_id> bash
docker exec -it $(docker container ls  | grep 'ros2:cuda' | awk '{print $1}') bash
docker stop $(docker ps -a -q)
docker system prune -f --volumes
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
