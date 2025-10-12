# ROS2
> The Robot Operating System (ROS) is a set of software libraries and tools for building robot applications. From drivers and state-of-the-art algorithms to powerful developer tools, ROS has the open source tools you need for your next robotics project.
> REP 2000: https://ros.org/reps/rep-2000.html defines the timeline for future ROS 2 releases as well as the targeted platforms for each specific one. 

## Install docker images
* build
```bash
bash build.bash
```
* run
```bash
bash run.bash
bash run-ros2.bash
```
* docker commands: images, ps, stop, remove
```bash
docker images && docker ps
docker exec -it <container_id> bash
docker stop $(docker ps -a -q)
docker system prune -f --volumes
```

## References
* https://docs.ros.org/en/foxy/index.html
* https://roboticseabass.com/2023/07/09/updated-guide-docker-and-ros2/ 


