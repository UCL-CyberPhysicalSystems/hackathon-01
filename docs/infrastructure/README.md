# UCL infrastructure

The following diagram illustrates the infrastructure for the hackathon. UCL East hosts a server connected to the sensors (lasers, IMUs, cameras, etc), with data streamed via the ROSBridge-suite and the Zenoh ROS 2 DDS bridge (sample rate and datasize to be tested). A Zenoh router with 10 GbE connectivity will link G40 server to the UCL ARC platform (condender and unified-ai). 
The ARC platforms will run containers using ROS 2 Humble on Ubuntu 22.04, where 5–10 participants will be able to access the sensor data through the ROSBridge Suite to visualise it, recognise/segmnt objecives of live video streaming, and visualise data.

![fig](cyber-physical-hackathon-network.svg)

## Resources
* Dockefiles: [Dockerfile-ros2](../../ros2/Dockerfile-ros2) , [Dockerfile-ros2-cuda](../../ros2/Dockerfile-ros2-cuda) and [others](../../ros2) 
* Zenoh (Zero Overhead Network Protocol): [home](https://zenoh.io/), [Zenoh router in a Docker container](https://zenoh.io/docs/getting-started/quick-test/)
* [UCL Virtual Private Network (VPN)](https://www.ucl.ac.uk/isd/services/get-connected/ucl-virtual-private-network-vpn)

