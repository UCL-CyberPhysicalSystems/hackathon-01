# UCL infrascture

The following diagram illustrates the infrastructure for the hackathon. UCL East hosts a server connected to the sensors, with data streamed via the ROSBridge Suite and the Zenoh ROS 2 DDS bridge. A Zenoh router with 100 GbE connectivity will link this to the UCL ARC server. The ARC server will run containers using ROS 2 Humble on Ubuntu 22.04, where 5–10 participants will be able to access the sensor data through the ROSBridge Suite.

![fig](cyber-physical-hackathon-network.svg)


