#!/usr/bin/python3
import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list

try:
    from math import pi, tau, dist, fabs, cos
except:  # For Python 2 compatibility
    from math import pi, fabs, cos, sqrt
    tau = 2.0 * pi
    def dist(p, q):
        return sqrt(sum((p_i - q_i) ** 2.0 for p_i, q_i in zip(p, q)))

moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node("move_group_python_interface", anonymous=True)

robot = moveit_commander.RobotCommander()
scene = moveit_commander.PlanningSceneInterface()

group_name = "manipulator"
move_group = moveit_commander.MoveGroupCommander(group_name)

display_trajectory_publisher = rospy.Publisher(
    "/move_group/display_planned_path",
    moveit_msgs.msg.DisplayTrajectory,
    queue_size=20,
)

# We can get the name of the reference frame for this robot:
planning_frame = move_group.get_planning_frame()
print("============ Planning frame: %s" % planning_frame)

# We can also print the name of the end-effector link for this group:
eef_link = move_group.get_end_effector_link()
print("============ End effector link: %s" % eef_link)

# We can get a list of all the groups in the robot:
group_names = robot.get_group_names()
print("============ Available Planning Groups:", robot.get_group_names())

# Sometimes for debugging it is useful to print the entire state of the
# robot:
print("============ Printing robot state")
print(robot.get_current_state())
print("")

# We get the joint values from the group and change some of the values:
joint_goal = move_group.get_current_joint_values()
joint_goal[0] = 0
joint_goal[1] = -tau / 8
joint_goal[2] = 0
joint_goal[3] = -tau / 4
joint_goal[4] = 0
joint_goal[5] = tau / 6  # 1/6 of a turn

# The go command can be called with joint values, poses, or without any
# parameters if you have already set the pose or joint target for the group
move_group.go(joint_goal, wait=True)

# Calling ``stop()`` ensures that there is no residual movement
move_group.stop()

while True:
    dr = input("Dame dir")
    vertical = 0
    horizontal = 0
    if dr == 'W':
        vertical=0.01
    elif dr == 'S':
        vertical=-0.01
    elif dr == 'A':
        horizontal=-0.01
    elif dr == 'D':
        horizontal=0.01

    pose_goal = move_group.get_current_pose().pose
    #pose_goal = geometry_msgs.msg.Pose()
    #pose_goal.orientation.w = 1.0
    pose_goal.position.x += vertical
    pose_goal.position.y += horizontal
    pose_goal.position.z += 0

    move_group.set_pose_target(pose_goal)



class arm_movement_node:

    def __init__(self):
        # Msg for the publish
        self.msg_gripper = String()
        self.msg_finish = Bool()
    
        # Publisher and subscriber
        self.pub_gripper_action = rospy.Publisher('pickUp_flag', String, queue_size=10)
        self.pub_finish_confirmation = rospy.Publisher('finish', Bool, queue_size=10)
        self.subs_reset_system = rospy.Subscriber('reset_arm', Bool, self.callback_reset_system)
        self.subs_coordinates_goal = rospy.Subscriber('coordinates', Float64MultiArray, self.callback_coordinates_goal)
        self.rate = rospy.Rate(10) 

        # Extract target object 
        while not rospy.is_shutdown():
            a = 0
          
    def callback_reset_system(self, msg_reset):
        # Extract the object to identify            
        self.reset = msg_reset.data

    def callback_coordinates_goal(self, msg_coordinates):
          # Extract the object to identify            
          self.goal_coordinates = msg_reset.data
                  
if __name__ == '__main__':
    try:
        rospy.init_node('arm_movement_node')
        arm_movement_node()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
