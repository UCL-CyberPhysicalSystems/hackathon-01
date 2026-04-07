# Pose estimation with Yolo by @pineapple-cat and @sfmig

0. SSH to condenser and setup ROS2 docker image
SSH to condenser
	ssh -Y -J condenser ubuntu@10.134.35.3 #CPU VM

	(If you have too many keys, you may want to use the -i flag to specify
your private key for authentication.)

	You can check if the docker image is there with docker image
docker run -it --rm --net=host --name=ros2condenser ghcr.io/mxochicale/ros2condenser:0.0.2 bash
(Could possibly want the --gpus all flag if using a GPU machine. If it works, the nvidia-smi command will produce useful output.)
To mount a directory from inside the container
 docker run -it --rm --net=host -v /home/sminano:/home/rosuser/ros2_ws/ --name=ros2condenser ghcr.io/mxochicale/ros2condenser:0.0.2 bash
export ROS_DOMAIN_ID=2
ros2 topic list ​
ros2 node list ​
ros2 topic echo <any topic URL>


1. Install deps	
```bash
pip install ultralytics opencv-python-headless flask
sudo apt install ros-humble-cv-bridge
```

2. Create a ROS2 package
```bash
cd ~/ros2_ws/src # this is created by default?
ros2 pkg create --build-type ament_python pose_estimator 
cd pose_estimator/pose_estimator
```


3. Creating a ROS2 node [pose_node.py](pose_node.py)
touch pose_node.py to create pose_estimator/pose_estimator/pose_node.py
Some concepts: subscription and publishing 


4. Configure setup.py
In pose_estimator/setup.py, we register the entry point:
```bash
entry_points={
    'console_scripts': [
        'pose_node = pose_estimator.pose_node:main',
    ],
},
```


5. To build and run the node:

```bash
cd ~/ros2_ws
# build node
colcon build --packages-select pose_estimator
source install/setup.bash

# run node
ros2 run pose_estimator pose_node
```

If all works /pose_estimator/annotated should be listed under ros2 topic list


6. Checks / troubleshooting
Check ROS_DOMAIN_ID is set to the value you wanted! (echo $ROS_DOMAIN_ID)
If error re numpy version, run: pip install "numpy<2" --break-system-packages



7. Forward the port

Run hostname -I —-> 10.xxx.xx.3 172.xx.x.1 —->  I used the first address to forward the port 
 
The easiest was to do it via VScode
In VSCode via command palette > Forward Port > 10.xxx.xx.3:5000 —> this got mapped to my local port 5001



8. To record the annotated images into a rosbag
ros2 bag record -o output -d 5 /pose_estimator/annotated
	Note that the last argument is the topic directly (vs the docs that say to use --topic <topic-name>
Inspect with ros2 bag info output
Playback with ros2 bag play output — it will behave as a regular topic?


Future improvements
Mounting outside the container - it would be very convenient for debugging the python code (rather than using nano)
Export model as .onnx – it should speed things up
Run on a node with gpu
