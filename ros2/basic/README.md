# Basic ROS2 docker image

Once you have built docker images, you can then run your image

```bash
PROFILE=ros2 #Profiles: ros2, ros2cuda, isaacsim, all
ROS_DISTRO=humble
VERSION_ID=0.0.1

bash run-ros2.bash $PROFILE $ROS_DISTRO $VERSION_ID
#to run multiple terminals with the same docker images id
docker exec -it $(docker container ls  | grep "${PROFILE}:${ROS_DISTRO}-${VERSION_ID}" | awk '{print $1}') bash
```
