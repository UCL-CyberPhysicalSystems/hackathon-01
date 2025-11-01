#! /usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
import math
import numpy as np
import cv2
from pathlib import Path

from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from path_tracking_simulator_window import Ui_Form

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
from tf2_msgs.msg import TFMessage

class Map_GraphicsScene(QGraphicsScene):
    def __init__(self, parent=None):
        QGraphicsScene.__init__(self, parent)
        self.center_x = 250
        self.center_y = 250
        self.prev_x = 250
        self.prev_y = 250
        self.scale = 0.2 #m/pix
        self.path = []
        self.path.append([(self.prev_x - self.center_x)*self.scale, 
                     -1*(self.prev_y - self.center_y)*self.scale])
        self.path_pen = QPen(Qt.blue)

    def mouseMoveEvent(self,event):
        x = event.scenePos().x()
        y = event.scenePos().y()

        window.map_scene.addLine(QLineF(self.prev_x, self.prev_y, x, y), self.path_pen)   
        self.path.append([(x - self.center_x)*self.scale, 
                          -1*(y - self.center_y)*self.scale])
        self.prev_x = x
        self.prev_y = y  

    def mousePressEvent(self, event):
        pass

class Path_Tracking_Simulator(QDialog):
    def __init__(self,parent=None):

        super(Path_Tracking_Simulator, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.map_scene = Map_GraphicsScene(self.ui.map_graphicsView)
        self.ui.map_graphicsView.setScene(self.map_scene)

        rclpy.init(args=None)
        self.pub_node = Node('pub_path')
        self.pub = self.pub_node.create_publisher(Float64MultiArray, '/path', 10)
        self.sub_node = Node('sub_observation')
        self.sub = self.sub_node.create_subscription(TFMessage, '/model/fws_robot/pose', self.listener_callback, 10)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(10)      

        self.pixmap = QPixmap(500, 500)
        self.vehicle_pen = QPen(Qt.red)
        self.center_line=QPen(Qt.black)
        self.center_line.setStyle(Qt.DashLine)
        self.map_scene.addLine(QLineF(250, 0, 250, 500), self.center_line) 
        self.map_scene.addLine(QLineF(0, 250, 500, 250), self.center_line)

        self.diameter = 2 #pix
        self.C = 10 #length
        self.first_time = True
        self.enable_repaint = False

    def listener_callback(self, data):
        for tfsf in data.transforms:
            if(tfsf.child_frame_id == 'fws_robot'):
                pose = tfsf.transform.translation
                orientation = tfsf.transform.rotation
                x = pose.x/self.map_scene.scale + self.map_scene.center_x
                y = -pose.y/self.map_scene.scale + self.map_scene.center_y
                q0 = orientation.x
                q1 = orientation.y
                q2 = orientation.z
                q3 = orientation.w
                numerator = q0*q1 + q2*q3
                denominator = q0**2 - q1**2 - q2**2 + q3**2
                angle = -math.pi/2 + math.atan2(2*numerator, denominator)

                if(self.enable_repaint):
                    if self.first_time == False:
                        self.map_scene.clear()
                    else:
                        self.first_time = False
                    self.map_scene.addPixmap(self.pixmap)
                    self.map_scene.addLine(QLineF(250, 0, 250, 500), self.center_line) 
                    self.map_scene.addLine(QLineF(0, 250, 500, 250), self.center_line)
                    self.ui.map_graphicsView.setScene(self.map_scene)

                    self.map_scene.addEllipse(x - int(self.diameter),
                                              y - int(self.diameter/2), 
                                              self.diameter,
                                              self.diameter,
                                              self.vehicle_pen)
                    self.pixmap = self.ui.map_graphicsView.grab(QRect(QPoint(0,0),QSize(500, 500)))


                    points = [[x - self.C*math.sin(angle), y - self.C*math.cos(angle)], 
                              [x - math.cos(angle)*self.C/2 + math.sqrt(3)*math.sin(angle)*self.C/2,
                               y + math.sin(angle)*self.C/2 + math.sqrt(3)*math.cos(angle)*self.C/2],
                              [x + math.cos(angle)*self.C/2 + math.sqrt(3)*math.sin(angle)*self.C/2,
                               y - math.sin(angle)*self.C/2 + math.sqrt(3)*math.cos(angle)*self.C/2]]

                    qpoly = QPolygonF([QPointF(p[0], p[1]) for p in points])
                    self.map_scene.addPolygon(qpoly, QPen(Qt.blue), QBrush(Qt.blue)) 
        
        
    def update(self): 
        rclpy.spin_once(self.sub_node, timeout_sec=0)

    def publish_path(self):
        #'''
        path_to_publish = []
        path_to_publish.append(np.array(self.map_scene.path[0]))
        nodes_interval = 0.2 # meter
        path_index = 1
        path_to_publish_index = 0

        # removing points that are closer to each other than 0.2 meter.
        while True:
            have_removed_idex = False
            for i in range(len(self.map_scene.path)-1):
                distance = math.sqrt((self.map_scene.path[i+1][0] - self.map_scene.path[i][0])**2 +
                             (self.map_scene.path[i+1][1] - self.map_scene.path[i][1])**2)
                if(distance < 0.2):
                    self.map_scene.path.pop(i+1)
                    have_removed_idex = True
                    print(f"poped index{i+1}")
                    break
            if(have_removed_idex == False):
                print("all edges with less then 0.2 length are removed.")
                break

        while True:
            dist = math.sqrt((path_to_publish[path_to_publish_index][0] - self.map_scene.path[path_index][0])**2 +
                             (path_to_publish[path_to_publish_index][1] - self.map_scene.path[path_index][1])**2)

            if(dist >= 0.2):
                if((self.map_scene.path[path_index-1][0] - self.map_scene.path[path_index][0]) != 0):
                    grad = (self.map_scene.path[path_index-1][1] - self.map_scene.path[path_index][1])/(self.map_scene.path[path_index-1][0] - self.map_scene.path[path_index][0])
                    x1 = nodes_interval/math.sqrt(1 + grad**2) + path_to_publish[path_to_publish_index][0]
                    x2 = -nodes_interval/math.sqrt(1 + grad**2) + path_to_publish[path_to_publish_index][0]

                    p1 = np.array([x1, (x1 - path_to_publish[path_to_publish_index][0])*grad + path_to_publish[path_to_publish_index][1]])
                    p2 = np.array([x2, (x2 - path_to_publish[path_to_publish_index][0])*grad + path_to_publish[path_to_publish_index][1]])
                    path_target_node = np.array(self.map_scene.path[path_index])
                    A = path_target_node - path_to_publish[path_to_publish_index]
                    B = p2 - path_to_publish[path_to_publish_index]
                    C = p1 - path_to_publish[path_to_publish_index]
                    cos_theta1 = A@B/(np.linalg.norm(A)*np.linalg.norm(B))
                    cos_theta2 = A@C/(np.linalg.norm(A)*np.linalg.norm(C))
                    if(cos_theta1 < cos_theta2):
                        path_to_publish.append(p1)
                        path_to_publish_index += 1
                    else:
                        path_to_publish.append(p2)
                        path_to_publish_index += 1     
                else:
                    x = self.map_scene.path[path_index-1][0]
                    y1 = path_to_publish[path_to_publish_index][1] + 0.2
                    y2 = path_to_publish[path_to_publish_index][1] - 0.2

                    if(path_to_publish[path_to_publish_index][1] <= y1 <= self.map_scene.path[path_index][1]):
                        path_to_publish.append(np.array([x,y1]))
                    else:
                        path_to_publish.append(np.array([x,y2]))

                    path_to_publish_index += 1
            else:
                path_index += 1

            if path_index == len(self.map_scene.path)-1:
                self.pixmap = self.ui.map_graphicsView.grab(QRect(QPoint(0,0),QSize(500, 500)))
                self.enable_repaint = True
                break

            if path_to_publish_index > 10000:
                self.map_scene.path.clear()
                self.map_scene.clear()
                path_to_publish.clear()
                self.map_scene.prev_x = 250
                self.map_scene.prev_y = 250
                self.map_scene.path.append([(self.map_scene.prev_x - self.map_scene.center_x)*self.map_scene.scale, 
                                  -1*(self.map_scene.prev_y - self.map_scene.center_y)*self.map_scene.scale])
                self.map_scene.addLine(QLineF(250, 0, 250, 500), self.center_line) 
                self.map_scene.addLine(QLineF(0, 250, 500, 250), self.center_line)
                print("path generation failed. Please draw another path.")
                break

        print(path_to_publish)
        path_to_publish_np = np.array(path_to_publish)
        print(f"done!")
        path_pub = Float64MultiArray(data=np.ravel(path_to_publish_np))    
        self.pub.publish(path_pub) 

    def pixmap_to_cv(self, pixmap):
        qimage = pixmap.toImage()
        w, h, d = qimage.size().width(), qimage.size().height(), qimage.depth()
        bytes_ = qimage.bits().asstring(w * h * d // 8)
        arr = np.frombuffer(bytes_, dtype=np.uint8).reshape((h, w, d // 8))
        im_bgr = cv2.cvtColor(arr, cv2.COLOR_BGRA2BGR)
        return im_bgr
    
    def update_path_image(self):
        pixmap2cv = self.ui.map_graphicsView.grab(QRect(QPoint(1,1),QSize(500, 500)))
        frame = self.pixmap_to_cv(pixmap2cv)
        frame = cv2.resize(frame, (1000, 1000))
        cv2.imwrite(os.environ['HOME'] + '/path_tracking_sim_ros2/src/robot_simulation/robot_gazebo/worlds/path_tracking_stage/meshes/stage.png', frame)
        install_dir = Path(os.environ['HOME'] + '/path_tracking_sim_ros2/install/robot_gazebo/share/robot_gazebo/worlds/path_tracking_stage/meshes')
        if install_dir.exists():
            cv2.imwrite(os.environ['HOME'] + '/path_tracking_sim_ros2/install/robot_gazebo/share/robot_gazebo/worlds/path_tracking_stage/meshes/stage.png', frame)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Path_Tracking_Simulator()
    window.show()
    sys.exit(app.exec_())