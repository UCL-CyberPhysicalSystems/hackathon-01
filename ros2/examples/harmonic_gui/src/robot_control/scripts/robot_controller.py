#!/usr/bin/python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
from sensor_msgs.msg import Joy

import numpy as np
import threading
import math

target_values = np.array([0.0, 0.0], float)

class Commander(Node):

    def __init__(self):
        super().__init__('commander')

        self.knuckle_pos = np.array([0,0], float)  #left right
        self.wheel_vel= np.array([0,0], float)     #left right
        self.publisher_pos = self.create_publisher(Float64MultiArray, '/forward_position_controller/commands', 10)
        self.publisher_vel = self.create_publisher(Float64MultiArray, '/forward_velocity_controller/commands', 10)

        self.T = 1.1  # track of the front and rear 
        self.L = 1.8 # wheel base
        self.Rw = 0.3 # Radius of the front and rear wheel

        self.time_interval = 0.02
        self.timer = self.create_timer(self.time_interval, self.timer_callback)

    def timer_callback(self):
        global target_values

        vel = target_values[0]
        omega = target_values[1]

        if((2*vel - omega*self.T) != 0):
            self.knuckle_pos[0] = math.atan(omega*self.L/(2*vel - omega*self.T))
        else:
            self.knuckle_pos[0] = 0
        
        if((2*vel + omega*self.T) != 0):
            self.knuckle_pos[1] = math.atan(omega*self.L/(2*vel + omega*self.T))
        else:
            self.knuckle_pos[1] = 0

        self.wheel_vel[0] = (vel - omega*self.T/2)/self.Rw
        self.wheel_vel[1] = (vel + omega*self.T/2)/self.Rw 

        #self.get_logger().info(f"self.wheel_vel:{self.wheel_vel}, knuckle_pos:{self.knuckle_pos}")

        wheel_vel_array = Float64MultiArray(data=self.wheel_vel)    
        self.publisher_vel.publish(wheel_vel_array)  
        knuckle_pos_array = Float64MultiArray(data=self.knuckle_pos)    
        self.publisher_pos.publish(knuckle_pos_array)     

class Joy_subscriber(Node):

    def __init__(self):
        super().__init__('joy_subscriber')
        self.target_pitch_angle = 0
        self.target_w = 0
        self.subscription = self.create_subscription(
            Joy,
            'joy',
            self.listener_callback,
            10)
        self.subscription

    def listener_callback(self, data):
        global target_values

        target_values[0] = 4.0*data.axes[1]
        target_values[1] = data.axes[0]

if __name__ == '__main__':
    rclpy.init(args=None)

    commander = Commander()
    joy_subscriber = Joy_subscriber()

    executor = rclpy.executors.MultiThreadedExecutor()
    executor.add_node(commander)
    executor.add_node(joy_subscriber)

    executor_thread = threading.Thread(target=executor.spin, daemon=True)
    executor_thread.start()

    rate = commander.create_rate(2)
    try:
        while rclpy.ok():
            rate.sleep()
    except KeyboardInterrupt:
        pass

    rclpy.shutdown()
    executor_thread.join()

