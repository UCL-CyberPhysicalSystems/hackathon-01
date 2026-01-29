# Isaacsim docker image

## Build docker images locallly with [build-docker.bash](build-docker.bash) 
```bash
PROFILE=isaacsim && ROS_DISTRO=humble && VERSION_ID=0.0.2
bash build-docker.bash $PROFILE $ROS_DISTRO $VERSION_ID
```

## Lauch docker image
```bash
PROFILE=isaacsim && ROS_DISTRO=humble && VERSION_ID=0.0.2
bash run-ros2isaacsim.bash $PROFILE $ROS_DISTRO $VERSION_ID
#Inside the container run app
bash runapp.sh
#to run multiple terminals with the same docker images id
docker exec -it $(docker container ls  | grep "${PROFILE}:${ROS_DISTRO}-${VERSION_ID}" | awk '{print $1}') bash
```
