xhost +
docker run --name ros2cuda --entrypoint bash -it --runtime=nvidia --gpus all -e "ACCEPT_EULA=Y" --rm --network=host \
    -e "PRIVACY_CONSENT=Y" \
    -v $HOME/.Xauthority:/root/.Xauthority:rw \
    -v $HOME/Downloads/diffusion_path_planning:/home/diffusion_path_plannig \
    -e DISPLAY \
    ros2:cuda
