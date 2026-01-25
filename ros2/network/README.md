# ROS2 docker image with network tools

## Build docker images with custom parameters
Run [build-docker.bash](../build-docker.bash):
```bash
cd ros2/
PROFILE=network && ROS_DISTRO=humble && VERSION_ID=0.0.2
bash build-docker.bash $PROFILE $ROS_DISTRO $VERSION_ID
```

## Run and test docker images locally
```bash
cd ros2/network
bash run-ros2.bash $PROFILE $ROS_DISTRO $VERSION_ID
#to run multiple terminals with the same docker images id
docker exec -it $(docker container ls  | grep "ros2:${PROFILE}-${ROS_DISTRO}-${VERSION_ID}" | awk '{print $1}') bash
```

## Pushing container images
```bash
PROJECT_NAME=ros2condenser
GITHUB_USERNAME=YOUR_GITHUB_USERNAME
export CR_PAT=YOUR_TOKEN
echo ${CR_PAT} | docker login ghcr.io -u ${GITHUB_USERNAME} --password-stdin
```

Tag your Docker image using the image ID and your desired image name and hosting destination.
```bash
docker tag ros2:${PROFILE}-${ROS_DISTRO}-${VERSION_ID} ghcr.io/mxochicale/${PROJECT_NAME}:${VERSION_ID}
```
Pushing container images
```bash
docker push ghcr.io/mxochicale/${PROJECT_NAME}:${VERSION_ID}
```
Go to packages https://github.com/users/mxochicale/packages/container/package/ros2condenser and change visibility to public.


## Pull and test image registry 
* Connect to UCL VPN (see [here](https://www.ucl.ac.uk/isd/services/get-connected/ucl-virtual-private-network-vpn) for details)
```bash
#setup image, pull and run it
GITHUB_USERNAME=mxochicale && PROJECT_NAME=ros2condenser && VERSION_ID=0.0.2
IMAGE="ghcr.io/${GITHUB_USERNAME}/${PROJECT_NAME}:${VERSION_ID}"
docker pull $IMAGE
docker images
GITHUB_USERNAME=mxochicale PROJECT_NAME=ros2condenser VERSION_ID=0.0.2 bash run-ros2.bash
#to run multiple terminals with the same docker images id
docker exec -it $(docker container ls  | grep "${PROJECT_NAME}:${VERSION_ID}" | awk '{print $1}') bash
```
