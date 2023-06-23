#!/usr/bin/env python
import cv2
import pandas
import rospy
import torch
import numpy as np
from std_msgs.msg import String, Bool, Float64MultiArray

class object_recognition_node:

    def __init__(self):
        # Msg for the publish
        self.msg_coordinates = Float64MultiArray()
        self.msg_object_confirmation = Bool()
        
        # Create recognition instance
        self.counter = 0
        self.flag_object = False
        self.flag_finish = False
        self.not_identify = True 
        self.cap = cv2.VideoCapture(0)
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path='/home/cesim-ai/TesisJaimeMultimodal/src/UR3_Control/src/multimodal_system/src/best.pt')
        
        # Publisher and subscriber
        self.pub_coordinates_arm = rospy.Publisher('coordinates', Float64MultiArray, queue_size=10)
        self.pub_object_confirmation = rospy.Publisher('object_confirmation', Bool, queue_size=10)
        self.subs_reset_system = rospy.Subscriber('reset_arm', Bool, self.callback_reset_system)
        self.subs_speech_object = rospy.Subscriber('word_detector', String, self.callback_speech_object)
        self.rate = rospy.Rate(10) 

        # Extract target object 
        while not rospy.is_shutdown():
            if self.not_identify == True and self.flag_object == True: 
                self.msg_object_confirmation.data = self.flag_finish
                self.pub_object_confirmation.publish(self.msg_object_confirmation)
                self.identify_objects()
                
            elif self.flag_finish == True:
                self.identify_objects()
                self.msg_object_confirmation.data = self.flag_finish
                self.pub_object_confirmation.publish(self.msg_object_confirmation)
                print(self.object_target + ' is in the experimental scene')
                
            self.counter += 1
    
    def callback_reset_system(self, msg_reset):
        # Extract the object to identify            
        self.reset = msg_reset.data
        
        if self.reset == True:
            # Re-initialize initial coonditions
            self.flag_object = False
            self.flag_finish = False
            self.not_identify = True 
            self.counter = 0
        else:
            pass
             
    def callback_speech_object(self, msg_object):
        # Extract the object to identify            
        self.object_target = msg_object.data
        self.flag_object = True
            
    def identify_objects(self):
        ret, frame = self.cap.read()
        detect = self.model(frame)
            
        # Identification
        cv2.imshow('Object detection', np.squeeze(detect.render()))
        t = cv2.waitKey(5)
            
        # Confirmation of identification
        if self.object_target == 'motor' and (detect.pandas().xyxy[0]['name'].eq('motor')).any():
            # Experimental operatonal coordinates
            self.msg_coordinates.data = [0.0, 0.0, 0.0]
            self.pub_coordinates_arm.publish(self.msg_coordinates)
            self.not_identify = False
            self.flag_finish = True
            
        elif self.object_target == 'caja' and (detect.pandas().xyxy[0]['name'].eq('caja')).any():
            # Experimental operatonal coordinates
            self.msg_coordinates.data = [1.0, 1.0, 1.0]
            self.pub_coordinates_arm.publish(self.msg_coordinates)
            self.not_identify = False
            self.flag_finish = True
            
        elif self.object_target == 'protoboard' and (detect.pandas().xyxy[0]['name'].eq('protoboard')).any():
            # Experimental operatonal coordinates
            self.msg_coordinates.data = [2.0, 2.0, 2.0]
            self.pub_coordinates_arm.publish(self.msg_coordinates)
            self.not_identify = False
            self.flag_finish = True
        
        elif self.object_target == 'cables' and (detect.pandas().xyxy[0]['name'].eq('cables')).any():
            # Experimental operatonal coordinates
            self.msg_coordinates.data = [0.163157, 0.502895, 0.216378]
            self.pub_coordinates_arm.publish(self.msg_coordinates)
            self.not_identify = False
            self.flag_finish = True
        
        elif self.counter >= 70:
            print(self.object_target + ' is NOT in the experimental scene')
            
if __name__ == '__main__':
    try:
        rospy.init_node('object_recognition_node')
        object_recognition_node()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
