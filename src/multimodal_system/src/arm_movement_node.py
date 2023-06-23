#!/usr/bin/python3
import sys
import rospy
import time
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from tf.transformations import quaternion_from_euler
from std_msgs.msg import String, Bool, Float64MultiArray
from moveit_commander.conversions import pose_to_list

try:
    from math import pi, tau, dist, fabs, cos
except:  # For Python 2 compatibility
    from math import pi, fabs, cos, sqrt
    tau = 2.0 * pi
    def dist(p, q):
        return sqrt(sum((p_i - q_i) ** 2.0 for p_i, q_i in zip(p, q)))

class arm_movement_node:

    def __init__(self):
        # Flags
        self.not_take = True
        self.gripper_close = False
        self.flag_coordinates = False
        
        # Msg for the publish
        self.msg_gripper = String()
        self.msg_finish = Bool()
    
        # Publisher and subscriber
        self.pub_gripper_action = rospy.Publisher('pickUp_flag', String, queue_size=10)
        self.pub_finish_confirmation = rospy.Publisher('finish', Bool, queue_size=10)
        self.subs_reset_system = rospy.Subscriber('reset_arm', Bool, self.callback_reset_system)
        self.subs_speech_object = rospy.Subscriber('word_detector', String, self.callback_speech_object)
        self.subs_coordinates_goal = rospy.Subscriber('coordinates', Float64MultiArray, self.callback_coordinates_goal)
        self.rate = rospy.Rate(10) 

        # Move-It
        moveit_commander.roscpp_initialize(sys.argv)
        robot = moveit_commander.RobotCommander()
        scene = moveit_commander.PlanningSceneInterface()
        
        self.group_name = "arm"
        self.move_group = moveit_commander.MoveGroupCommander(self.group_name)
        
        display_trajectory_publisher = rospy.Publisher(
            "/move_group/display_planned_path",
            moveit_msgs.msg.DisplayTrajectory,
            queue_size=20,
        )
        
        # We can get the name of the reference frame for this robot:
        planning_frame = self.move_group.get_planning_frame()
        print("============ Planning frame: %s" % planning_frame)
        
        # We can also print the name of the end-effector link for this group:
        eef_link = self.move_group.get_end_effector_link()
        print("============ End effector link: %s" % eef_link)
        
        # We can get a list of all the groups in the robot:
        group_names = robot.get_group_names()
        print("============ Available Planning Groups:", robot.get_group_names())
        
        # Sometimes for debugging it is useful to print the entire state of the
        # robot:
        print("============ Printing robot state")
        print(robot.get_current_state())
        print("")

        # Extract target object 
        while not rospy.is_shutdown():
            print(self.move_group.get_current_pose().pose)
            if self.flag_coordinates == True and self.not_take == True:
                self.move_to_object()
                time.sleep(2)
                self.down_to_object()
                time.sleep(4)
                self.move_to_object()
                time.sleep(2)
                self.goal_to_object()
                time.sleep(2)
                self.goal_down_to_object
                time.sleep(4)
                self.goal_to_object()
                self.not_take = False
                self.msg_finish.data = True
                self.pub_finish_confirmation.publish( self.msg_finish)

    def callback_speech_object(self, msg_object):
        # Extract the object to identify            
        self.object_target = msg_object.data
        
    def callback_reset_system(self, msg_reset):
        # Extract the object to identify            
        self.reset = msg_reset.data
        if self.reset == True:
            # We get the joint values from the group and change some of the values:
            joint_goal = self.move_group.get_current_joint_values()
            joint_goal[0] = -tau/4
            joint_goal[1] = 0
            joint_goal[2] = -tau/6
            joint_goal[3] = -tau/3
            joint_goal[4] = tau/4
            joint_goal[5] = tau/4  
            
            # The go command can be called with joint values, poses, or without any
            # parameters if you have already set the pose or joint target for the group
            self.move_group.go(joint_goal, wait=True)
            
            # Calling stop() ensures that there is no residual movement
            self.move_group.stop()
            self.reset = False
            
        else:
            pass
            
    def callback_coordinates_goal(self, msg_coordinates):
        # Extract the object to identify            
        self.goal_coordinates = msg_coordinates.data
        self.flag_coordinates = True

    def move_to_object(self):
        if  self.object_target == "cables":
            joint_goal = self.move_group.get_current_joint_values()
            joint_goal[0] = (-94)*tau/360
            joint_goal[1] = (-147)*tau/360
            joint_goal[2] = (-31)*tau/360
            joint_goal[3] = (-87)*tau/360
            joint_goal[4] = (90)*tau/360
            joint_goal[5] = (83)*tau/360

            # The go command can be called with joint values, poses, or without any
            # parameters if you have already set the pose or joint target for the group
            self.move_group.go(joint_goal, wait=True)
            
            # Calling stop() ensures that there is no residual movement
            self.move_group.stop()
            self.reset = False

    def down_to_object(self):
        pose_goal = self.move_group.get_current_pose().pose
    
        # Operational coordinates
        pose_goal.position.z -= 0.145

        self.move_group.set_pose_target(pose_goal)
        plan = self.move_group.go(wait=True)

        # Calling `stop()` ensures that there is no residual movement
        self.move_group.stop()
        self.move_group.clear_pose_targets()

    def goal_to_object(self):
        joint_goal = self.move_group.get_current_joint_values()
        joint_goal[0] = (-256)*tau/360
        joint_goal[1] = (-128)*tau/360
        joint_goal[2] = (-74)*tau/360
        joint_goal[3] = (-65)*tau/360
        joint_goal[4] = (88)*tau/360
        joint_goal[5] = (103)*tau/360
            
        # The go command can be called with joint values, poses, or without any
        # parameters if you have already set the pose or joint target for the group
        self.move_group.go(joint_goal, wait=True)
            
        # Calling stop() ensures that there is no residual movement
        self.move_group.stop()
        self.reset = False

    def goal_down_to_object(self):
        pose_goal = self.move_group.get_current_pose().pose
    
        # Operational coordinates
        pose_goal.position.z = 0.0707

        self.move_group.set_pose_target(pose_goal)
        plan = self.move_group.go(wait=True)

        # Calling `stop()` ensures that there is no residual movement
        self.move_group.stop()
        self.move_group.clear_pose_targets()
         
if __name__ == '__main__':
    try:
        rospy.init_node('arm_movement_node')
        arm_movement_node()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
