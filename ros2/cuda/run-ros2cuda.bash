IMAGE_NAME="ros2:cuda"

xhost +
docker run --name ros2cuda --entrypoint bash -it --rm --runtime=nvidia --gpus all \
    -e "ACCEPT_EULA=Y" \
    --network=host \
    --ipc=host \
    -e "PRIVACY_CONSENT=Y" \
    -e "DISPLAY=$DISPLAY" \
    -e "QT_X11_NO_MITSHM=1" \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
    -v $HOME/.Xauthority:/root/.Xauthority:rw \
    -v $HOME/repositories/UCL-CyberPhysicalSystems/hackathon-01:/home/hackathon-01 \
    -v $HOME/Downloads/diffusion_path_planning:/home/diffusion_path_planning \
    $IMAGE_NAME
