#include <moveit/move_group_interface/move_group_interface.h>
#include <moveit/planning_scene_interface/planning_scene_interface.h>

#include <moveit_msgs/DisplayRobotState.h>
#include <moveit_msgs/DisplayTrajectory.h>

#include <moveit_msgs/AttachedCollisionObject.h>
#include <moveit_msgs/CollisionObject.h>

#include "ros/ros.h"
#include "std_msgs/String.h"
 
#include <sstream>


#include <iostream>
#include <stdio.h>

// tau = 2*pi. Un tau es una rotacion en radianes.
const double tau = 2 * M_PI;

int main(int argc, char** argv)
{
  
  // Ros node inicilization

  ros::init(argc, argv, "move_group_interface_tutorial");
  ros::NodeHandle node_handle;
  ros::AsyncSpinner spinner(1);
  spinner.start();

  
  // Setup
  
  // Group definition in order to move the manipulator
  
  static const std::string PLANNING_GROUP = "manipulator";
  moveit::planning_interface::MoveGroupInterface move_group_interface(PLANNING_GROUP);

  // Class :planning_interface:`PlanningSceneInterface` for put and eliminate objects and collisions
  moveit::planning_interface::PlanningSceneInterface planning_scene_interface;

  // Configuraciones adicionales para mejorar la planeacion (Creo).
  const moveit::core::JointModelGroup* joint_model_group =
      move_group_interface.getCurrentState()->getJointModelGroup(PLANNING_GROUP);

  // Second group for control de gripper.
  static const std::string PLANNING_GROUP2 = "gripper";

  moveit::planning_interface::MoveGroupInterface move_group_interface_2(PLANNING_GROUP2);
  moveit::planning_interface::PlanningSceneInterface planning_scene_interface_2;

  const moveit::core::JointModelGroup* joint_model_group_2 =
      move_group_interface_2.getCurrentState()->getJointModelGroup(PLANNING_GROUP2);

  // We can print the name of the reference frame for this robot.
  ROS_INFO_NAMED("tutorial", "Planning frame: %s", move_group_interface.getPlanningFrame().c_str());

  // We can also print the name of the end-effector link for this group.
  ROS_INFO_NAMED("tutorial", "End effector link: %s", move_group_interface.getEndEffectorLink().c_str());

  // We can get a list of all the groups in the robot:
  ROS_INFO_NAMED("tutorial", "Available Planning Groups:");
  std::copy(move_group_interface.getJointModelGroupNames().begin(),
            move_group_interface.getJointModelGroupNames().end(), std::ostream_iterator<std::string>(std::cout, ", "));

  // Start 
 char movement; 
 int pos=0;

// Code inicialization
 while(pos != 14)
{

printf("\n\n Types of movements:\n\n w: Forward \n\n s Backward \n\n a: Left \n\n d: right \n\n");
setbuf(stdin,NULL);
scanf("%c",&movement);

// Initial pose
if(movement == 'r'){

  // Get actual articular pose of the joints
  std::vector<double> joints;
  joints = move_group_interface.getCurrentJointValues();

  // New goal positions
  joints.at(0) = tau/2;
  move_group_interface.setJointValueTarget(joints);
  move_group_interface.move();

}

// Forward
if(movement == 'w'){
  geometry_msgs::PoseStamped actual;
  actual = move_group_interface.getCurrentPose();

  geometry_msgs::Pose target_poseW;
  target_poseW.orientation.x = 0.0;

  target_poseW.position.x = actual.pose.position.x + 0.01;
  target_poseW.position.y = actual.pose.position.y;
  target_poseW.position.z = actual.pose.position.z;
  move_group_interface.setPoseTarget(target_poseW);

   // Create new trayectory plan
  moveit::planning_interface::MoveGroupInterface::Plan my_plan;

  // Plan to the goal position

  bool success = (move_group_interface.plan(my_plan) == moveit::planning_interface::MoveItErrorCode::SUCCESS);
  ROS_INFO_NAMED("tutorial", "Visualizing plan 1 (pose goal) %s", success ? "" : "FAILED");
  ROS_INFO_NAMED("tutorial", "Visualizing plan 1 as trajectory line");
  
  // Plan execution.
  move_group_interface.move();
}

// Backward
if(movement == 's'){
  geometry_msgs::PoseStamped actual;
  actual = move_group_interface.getCurrentPose();

  geometry_msgs::Pose target_poseS;
  target_poseS.orientation.x = 0.0;

  target_poseS.position.x = actual.pose.position.x - 0.01;
  target_poseS.position.y = actual.pose.position.y;
  target_poseS.position.z = actual.pose.position.z;
  move_group_interface.setPoseTarget(target_poseS);

   // Create new trayectory plan
  moveit::planning_interface::MoveGroupInterface::Plan my_plan;

  // Plan to the goal position

  bool success = (move_group_interface.plan(my_plan) == moveit::planning_interface::MoveItErrorCode::SUCCESS);
  ROS_INFO_NAMED("tutorial", "Visualizing plan 1 (pose goal) %s", success ? "" : "FAILED");
  ROS_INFO_NAMED("tutorial", "Visualizing plan 1 as trajectory line");
  
  // Plan execution.
  move_group_interface.move();
}

// Left
if(movement == 'a'){
  geometry_msgs::PoseStamped actual;
  actual = move_group_interface.getCurrentPose();

  geometry_msgs::Pose target_poseA;
  target_poseA.orientation.x = 0.0;

  target_poseA.position.x = actual.pose.position.x;
  target_poseA.position.y = actual.pose.position.y + 0.01;
  target_poseA.position.z = actual.pose.position.z;
  move_group_interface.setPoseTarget(target_poseA);

   // Create new trayectory plan
  moveit::planning_interface::MoveGroupInterface::Plan my_plan;

  // Plan to the goal position

  bool success = (move_group_interface.plan(my_plan) == moveit::planning_interface::MoveItErrorCode::SUCCESS);
  ROS_INFO_NAMED("tutorial", "Visualizing plan 1 (pose goal) %s", success ? "" : "FAILED");
  ROS_INFO_NAMED("tutorial", "Visualizing plan 1 as trajectory line");
  
  // Plan execution.
  move_group_interface.move();
}

// Right
if(movement == 'd'){
  geometry_msgs::PoseStamped actual;
  actual = move_group_interface.getCurrentPose();

  geometry_msgs::Pose target_poseD;
  target_poseD.orientation.x = 0.0;

  target_poseD.position.x = actual.pose.position.x;
  target_poseD.position.y = actual.pose.position.y - 0.01;
  target_poseD.position.z = actual.pose.position.z;
  move_group_interface.setPoseTarget(target_poseD);

   // Create new trayectory plan
  moveit::planning_interface::MoveGroupInterface::Plan my_plan;

  // Plan to the goal position

  bool success = (move_group_interface.plan(my_plan) == moveit::planning_interface::MoveItErrorCode::SUCCESS);
  ROS_INFO_NAMED("tutorial", "Visualizing plan 1 (pose goal) %s", success ? "" : "FAILED");
  ROS_INFO_NAMED("tutorial", "Visualizing plan 1 as trajectory line");
  
  // Plan execution.
  move_group_interface.move();
}

// Up
if(movement == 'u'){
  geometry_msgs::PoseStamped actual;
  actual = move_group_interface.getCurrentPose();

  geometry_msgs::Pose target_poseU;
  target_poseU.orientation.x = 0.0;

  target_poseU.position.x = actual.pose.position.x;
  target_poseU.position.y = actual.pose.position.y;
  target_poseU.position.z = actual.pose.position.z + 0.01;
  move_group_interface.setPoseTarget(target_poseU);

   // Create new trayectory plan
  moveit::planning_interface::MoveGroupInterface::Plan my_plan;

  // Plan to the goal position

  bool success = (move_group_interface.plan(my_plan) == moveit::planning_interface::MoveItErrorCode::SUCCESS);
  ROS_INFO_NAMED("tutorial", "Visualizing plan 1 (pose goal) %s", success ? "" : "FAILED");
  ROS_INFO_NAMED("tutorial", "Visualizing plan 1 as trajectory line");
  
  // Plan execution.
  move_group_interface.move();
}

// Down
if(movement == 'j'){
  geometry_msgs::PoseStamped actual;
  actual = move_group_interface.getCurrentPose();

  geometry_msgs::Pose target_poseJ;
  target_poseJ.orientation.x = 0.0;

  target_poseJ.position.x = actual.pose.position.x;
  target_poseJ.position.y = actual.pose.position.y;
  target_poseJ.position.z = actual.pose.position.z - 0.01;
  move_group_interface.setPoseTarget(target_poseJ);

   // Create new trayectory plan
  moveit::planning_interface::MoveGroupInterface::Plan my_plan;

  // Plan to the goal position

  bool success = (move_group_interface.plan(my_plan) == moveit::planning_interface::MoveItErrorCode::SUCCESS);
  ROS_INFO_NAMED("tutorial", "Visualizing plan 1 (pose goal) %s", success ? "" : "FAILED");
  ROS_INFO_NAMED("tutorial", "Visualizing plan 1 as trajectory line");
  
  // Plan execution.
  move_group_interface.move();
}

}
   
  ros::shutdown();
  return 0;
}