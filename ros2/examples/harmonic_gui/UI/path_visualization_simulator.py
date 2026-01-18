#! /usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import math

from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from path_visualization_window import Ui_Form

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
from tf2_msgs.msg import TFMessage
from sensor_msgs.msg import  Joy

class Controller_GraphicsScene(QGraphicsScene):

    pressed = False

    def __init__(self, parent=None):
        W, H = 150, 150
        self.Cx, self.Cy = int(W/2), int(H/2)
        QGraphicsScene.__init__(self, 0, 0, W, H, parent = None) 
        self.opt = ""

    def setOption(self, opt):
        self.opt = opt

    def mouseReleaseEvent(self,event):
        self.pressed = False
        window.repaint(self.Cx, self.Cy)
        window.cmd_Joy.axes = [0,0,0,0,0,0,0,0]

    def mousePressEvent(self,event):
        self.pressed = True

    def mouseMoveEvent(self,event):
        if(self.pressed == True):
            x = event.scenePos().x()
            y = event.scenePos().y()
            if(((x - self.Cx)**2 + (y - self.Cy)**2) < 60**2):
                if((x-self.Cx) != 0):
                    theta = math.atan2((self.Cy - y),(x - self.Cx))
                else:
                    theta = 0

                window.cmd_Joy.axes = [-(math.sqrt((x - self.Cx)**2 + (y - self.Cy)**2)/60)*math.cos(theta),
                                        (math.sqrt((x - self.Cx)**2 + (y - self.Cy)**2)/60)*math.sin(theta),
                                        0, 0, 0, 0, 0, 0]
                window.repaint(x, y)

class Map_GraphicsScene(QGraphicsScene):
    def __init__(self, parent=None):
        QGraphicsScene.__init__(self, parent)
        self.center_x = 250
        self.center_y = 250
        self.prev_x = 250
        self.prev_y = 250
        self.scale = 0.2 #m/pix

    def mouseMoveEvent(self,event):
        pass

    def mousePressEvent(self, event):
        pass

class Path_Visualization_Simulator(QDialog):
    def __init__(self,parent=None):
        super(Path_Visualization_Simulator, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.map_scene = Map_GraphicsScene(self.ui.map_graphicsView)
        self.ui.map_graphicsView.setScene(self.map_scene)

        rclpy.init(args=None)
        self.sub_node = Node('sub_observation')
        self.sub = self.sub_node.create_subscription(TFMessage, '/model/acs_robot/pose', self.listener_callback, 10)
        self.cmd_Joy = Joy()
        self.cmd_Joy.axes = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.cmd_Joy.buttons = [0,0,0,0,0,0,0,0,0,0,0]
        self.pub_node = Node('pub_path')
        self.pub_Joy = self.pub_node.create_publisher(Joy, '/joy', 10)

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

        self.repaint(75, 75)

    def listener_callback(self, data):
        for tfsf in data.transforms:
            if(tfsf.child_frame_id == 'acs_robot'):
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

                if(self.first_time == False):
                    self.map_scene.clear()
                    self.map_scene.addPixmap(self.pixmap)
                    self.map_scene.addLine(QLineF(250, 0, 250, 500), self.center_line) 
                    self.map_scene.addLine(QLineF(0, 250, 500, 250), self.center_line)
                    self.ui.map_graphicsView.setScene(self.map_scene)
                    self.first_time = False

                self.map_scene.addEllipse(x - int(self.diameter), y - int(self.diameter/2), 
                                      self.diameter, self.diameter,
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
        rclpy.spin_once(self.sub_node)
        self.pub_Joy.publish(self.cmd_Joy)
      
    def repaint(self, x, y):
        if(self.first_time):
            self.scene = Controller_GraphicsScene()
            self.first_time = False
        self.ui.controller_graphicsView.setScene(self.scene)
        self.scene.addEllipse(0, 0, 150, 150, QPen(QColor(0,180,100)), QBrush(QColor(0,180,100)))
        self.scene.addEllipse(x - 15, y - 15, 30, 30, QPen(Qt.red), QBrush(Qt.red))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Path_Visualization_Simulator()
    window.show()
    sys.exit(app.exec_())