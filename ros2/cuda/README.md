# Docker image with CUDA depdendencies

## Build docker images locallly with [build-docker.bash](build-docker.bash) 
```bash
PROFILE=ros2cuda && ROS_DISTRO=jazzy && VERSION_ID=0.0.2
bash build-docker.bash $PROFILE $ROS_DISTRO $VERSION_ID
```

## Lauch docker image
```bash
PROFILE=ros2cuda && ROS_DISTRO=jazzy && VERSION_ID=0.0.2
bash run-ros2cuda.bash $PROFILE $ROS_DISTRO $VERSION_ID
#to run multiple terminals with the same docker images id
docker exec -it $(docker container ls  | grep "${PROFILE}-${ROS_DISTRO}:${VERSION_ID}" | awk '{print $1}') bash
```
