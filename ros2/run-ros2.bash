xhost +
docker run --name ros2 --entrypoint bash -it --runtime=nvidia --gpus all -e "ACCEPT_EULA=Y" --rm --network=host \
    -e "PRIVACY_CONSENT=Y" \
    -v $HOME/.Xauthority:/root/.Xauthority:rw \
    -e DISPLAY \
    ros:two
