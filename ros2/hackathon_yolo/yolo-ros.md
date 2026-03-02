# Using YOLO with ROS2 for object detection on Condensor


## Logging to Condensor

- follow the instructions in the [ros2/condenser](../condenser/README.md) to set up the Condensor environment


> [!WARNING]
> **Note for Mac users:** add ` -o "ObscureKeystrokeTiming=no"` to your ssh command to avoid issues with excessive warning messages.

> [!NOTE]
> **Streaming to local machine:** you can stream the video to your local machine by using by adding `-L 8080:localhost:8080` to your ssh command and then accessing `http://localhost:8080` in your browser. This requires `web_video_server` to be installed on the Condensor machine. More on this [here](https://github.com/RobotWebTools/web_video_server).


## Building the yolo module

- Start by building a docker container from the ros docker image as per the [basic](../basic/README.md) instructions.

- Get a terminal inside the docker container and clone the yolo module from the [yolo_ros](https://github.com/mgonzs13/yolo_ros/tree/main) repository.

- Follow the instructions in the [yolo_ros](https://github.com/mgonzs13/yolo_ros/tree/main) repository to build the yolo module.

> [!WARNING]
> **add rosdep:** the instructions in the [yolo_ros](https://github.com/mgonzs13/yolo_ros/tree/main) repository to build the yolo module include adding rosdep. You can add rosdep by running the following command:
> ```bash
> sudo apt-get update
> sudo apt-get install python3-rosdep
> rosdep init
> rosdep update
> ```

to test the yolo module, run the following command:
```bash
ros2 launch yolo_bringup yolo.launch.py input_image_topic:=/peak_cam/W_6340/image_raw model_type:=YOLOE device:=cpu model:=yolov8n-seg.pt
```
you should see an output like the following:
```bash
[yolo_node-1] [INFO] [1234567890.123456789] [yolo.yolo_node]: [yolo_node] Activated
```
and you should be able to see the yolo topics in the ros topics list:
```bash
ros2 topic list
```
you should see an output like the following:
```bash
/yolo/dbg_image
/yolo/debug_node/transition_event
/yolo/detections
/yolo/dgb_bb_markers
/yolo/dgb_kp_markers
/yolo/tracking
/yolo/tracking_node/transition_event
/yolo/yolo_node/transition_event
```


