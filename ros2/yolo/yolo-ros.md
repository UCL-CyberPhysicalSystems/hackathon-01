# Using YOLO with ROS2 for object detection on Condensor


## Logging to Condensor

- follow the instructions in the [ros2/condenser](../condenser/README.md) to set up the Condensor environment


> [!WARNING]
> **Note for Mac users:** add ` -o "ObscureKeystrokeTiming=no"` to your ssh command to avoid issues with excessive warning messages.

> [!NOTE]
> **Streaming to local machine:** you can stream the video to your local machine by using by adding -L 8080:localhost:8080 to your ssh command and then accessing http://localhost:8080 in your browser. This requires `web_video_server` to be installed on the Condensor machine. More on this [here](https://github.com/RobotWebTools/web_video_server).

