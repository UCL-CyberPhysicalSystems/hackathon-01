IMAGE_NAME=$1-$2:$3
echo $IMAGE_NAME

xhost +
docker run --name $1 --entrypoint bash -it --rm --runtime=nvidia --gpus all \
    -e "ACCEPT_EULA=Y" \
    --network=host \
    --ipc=host \
    -e "PRIVACY_CONSENT=Y" \
    -e "DISPLAY=$DISPLAY" \
    -e "QT_X11_NO_MITSHM=1" \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
    -v $HOME/.Xauthority:/root/.Xauthority:rw \
    -v $HOME/repositories/UCL-CyberPhysicalSystems/hackathon-01:/home/hackathon-01 \
    $IMAGE_NAME


    #-v "$HOME/.Xauthority:/home/rosuser/.Xauthority:rw" \
