#!/usr/bin/env python
"""PANTILT TF BROADCASTER

This node broadcast tf transformation for a pantilt camera. It subscribes to a
sensor_msg/JointState topic with pan and tilt angular position and generate the
corresponding transformation from pantilt base to camera frame.

NODE PARAM:

    a (double)                  : The horizontal offset between camera and tilt
                                  frames.
    d (double)                  : The vertical offset between tilt and pan
                                  frames.
    pantilt_frame_name (string) : Name for pantilt base frame.
    camera_frame_name (string)  : Name for the output camera frame.
    joint_input_topic (string)  : The topic where joint info are published.
"""
import roslib
roslib.load_manifest('pantilt_tf_broadcaster')
import rospy
from sensor_msgs.msg import JointState

import tf

import pt_transformation as pt 


def pantilt_callback(msg) :
    print "Callback!"
    br = tf.TransformBroadcaster()
    #Get position and orientation and convert them in standard python list.
    position = [i[0] for i in PT.translation_to_camera(0,0).tolist()]
    orientation = PT.quaternion_to_camera(0,0).tolist()[0]
    #print position, orientation
    br.sendTransform(position,
                    orientation,
                    rospy.Time.now(),
                    camera_frame_name,
                    pantilt_frame_name)

if __name__ == '__main__':
    rospy.init_node('odometry_tf_broadcaster')
    a = rospy.get_param('~a')
    d = rospy.get_param('~d')
    pantilt_frame_name = rospy.get_param('~pantilt_frame_name')
    camera_frame_name = rospy.get_param('~camera_frame_name')
    joint_input_topic = rospy.get_param('~joint_input_topic')
    PT = pt.PanTiltFrame(a,d)
    # TODO: Check message type.
    print "Subscribe to %s" % joint_input_topic
    print "Ready to broadcast tf from %s to %s" % (pantilt_frame_name,camera_frame_name)
    rospy.Subscriber(joint_input_topic,
        JointState,
        pantilt_callback)
    rospy.spin()
