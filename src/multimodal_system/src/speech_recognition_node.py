#!/usr/bin/env python
import rospy
import speech_recognition as sr
from std_msgs.msg import Float64MultiArray


def speech_recognition_node():
    # Create recognition instance
    r = sr.Recognizer()
    not_identify = True
    target_words = ["motor", "caja", "protoboard", "cables"]
    
    # Publisher
    pub = rospy.Publisher('word_detector', Float64MultiArray, queue_size=10)
    rospy.init_node('speech_recognition_node', anonymous=True)
    rate = rospy.Rate(10) 

    while not rospy.is_shutdown():
        # Msg fot the publish
        msg = Float64MultiArray()

        # Use microphone
        while not_identify:

            with sr.Microphone() as source:
                print("Say something...")
                
                # Listen to the audio
                audio = r.listen(source, timeout=5, phrase_time_limit=8)

                # Recognition
                try:
                    text = r.recognize_google(audio, language="es-CO")
                    words = text.split()
                    print(words)
                    if words[2] in target_words:
                        msg.data = words
                        not_identify = False

                        # Publish
                        rospy.loginfo(msg)
                        pub.publish(msg)
                        rate.sleep()
                        print("Object word target identified:", words[2])
                    else:
                        print("Object word target not identified")
                            
                except sr.UnknownValueError:
                    print("Could not understand the audio")
                except sr.RequestError as e:
                    print("Could not request results from Google's speech recognition service; {0}".format(e))


if __name__ == '__main__':
    try:
        speech_recognition_node()
    except rospy.ROSInterruptException:
        pass