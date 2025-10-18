

############
#docker build -t ros:two -f Dockerfile-ros2 .
#logs
#ros:two 4.02GB

############
docker build -t ros2:cuda -f Dockerfile-ros2-cuda .

#logs
#Building 1599.4s (29/29) FINISHED 
#ros2:cuda 22.4GB


############
#docker build -t isaac_sim_ros2:5.0.0-Humble -f Dockerfile-isaacsim-ros2 .
#logs
#isaac_sim_ros2:5.0.0-Humble 18.9GB

