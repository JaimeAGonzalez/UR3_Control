#!/usr/bin/env python
import rospy
import speech_recognition as sr
from std_msgs.msg import String, Bool

class speech_recognition_node:

    def __init__(self):
        # Msg for the publish
        self.msg_word = String()
        self.msg_reset = Bool()
        
        # Create recognition instance
        self.r = sr.Recognizer()
        self.flag_finish = False
        self.not_identify = True
        self.target_words = ["motor", "caja", "protoboard", "cables"]
        
        # Publisher
        self.pub_word = rospy.Publisher('word_detector', String, queue_size=10)
        self.pub_reset_arm = rospy.Publisher('reset_arm', Bool, queue_size=10)
        self.subs_finish = rospy.Subscriber("finish", Bool, self.callback_finish)
        self.rate = rospy.Rate(10) 

        # Extract target word
        while not rospy.is_shutdown():
            if self.not_identify == True:
                self.identify_word()
            else:
                if self.flag_finish == False:
                    print("Executing...")
                else:
                    print("Object is already placed")

    def identify_word(self):
        # Ask the client
        self.flag_init = input("Do you want to pick an object?")
        
        if self.flag_init == "Yes":
            # Reset flag arm
            self.msg_reset.data = True
            self.pub_reset_arm.publish(self.msg_reset)

            # Use microphone
            with sr.Microphone() as source:
                print("Say something...")
                    
                # Listen to the audio
                audio = self.r.listen(source, timeout=5, phrase_time_limit=8)
                
                # Recognition
                try:
                    text = self.r.recognize_google(audio, language="es-CO")
                    self.words = text.split()

                    if self.words[2] in self.target_words:
                        self.msg_word.data = self.words[2]
                        self.not_identify = False

                        # Publish arm
                        self.msg_reset.data = False
                        self.pub_reset_arm.publish(self.msg_reset)

                        # Publish word
                        self.pub_word.publish(self.msg_word)
                        self.rate.sleep()
                        print("Object word target identified:", self.words[2])
                    else:
                        print("Object word target not identified")
                                
                except sr.UnknownValueError:
                    print("Could not understand the audio")
                except sr.RequestError as e:
                    print("Could not request results from Google's speech recognition service; {0}".format(e))
        else:
            pass
    
    def callback_finish(self,msg_finish):
        self.flag_finish = msg_finish.data

if __name__ == '__main__':
    try:
        rospy.init_node('speech_recognition_node')
        speech_recognition_node()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass