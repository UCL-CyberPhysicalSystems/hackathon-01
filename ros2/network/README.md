# ROS2 docker image with network tools

## Build docker images with custom parameters
Example of [build-docker.bash](../build-docker.bash).
```bash
cd ros2/
PROFILE=network && ROS_DISTRO=humble && VERSION_ID=0.0.1
bash build-docker.bash $PROFILE $ROS_DISTRO $VERSION_ID
```

## Run and test docker images
```bash
cd ros2/network
PROFILE=network && ROS_DISTRO=humble && VERSION_ID=0.0.1
bash run-ros2.bash $PROFILE $ROS_DISTRO $VERSION_ID
#to run multiple terminals with the same docker images id
docker exec -it $(docker container ls  | grep "ros2:${PROFILE}-${ROS_DISTRO}-${VERSION_ID}" | awk '{print $1}') bash
```
