# Path Tracking Algorithm Simulation in ROS2
Source: https://www.youtube.com/watch?v=uls-WmxRiTw

![fig](runningdemo.png)

Run container
```bash
bash run-ros2cuda.bash
```

Build ros packages
```bash
cd /home/hackathon-01/ros2/tutorials/path_tracking_sim_ros2
colcon build --base-paths src
```

Run tracking simulator script
```bash
cd /home/hackathon-01/ros2/tutorials/path_tracking_sim_ros2/UI
python3 path_tracking_simulator.py
```

Run the main lunch script in a new terminal
```bash
docker exec -it <container_id> bash
source /home/hackathon-01/ros2/tutorials/path_tracking_sim_ros2/install/setup.bash
ros2 launch robot_gazebo main.launch.py
```

Run the Model Predictive Control
```bash
#TODO create a python environment within docker file to install depencies or a `ros_workspace`
python3 -m venv .venv
source .venv/bin/activate
export PYTHONPATH='/opt/ros/jazzy/lib/python3.12/site-packages:/.venv/lib/python3.12/site-packages/'
export PYTHONPATH='/opt/ros/jazzy/lib/python3.12/site-packages'
python3 -m pip install cvxpy
```

```bash
source /home/hackathon-01/ros2/tutorials/path_tracking_sim_ros2/install/setup.bash
ros2 run robot_control model_predictive_control.py 
```

