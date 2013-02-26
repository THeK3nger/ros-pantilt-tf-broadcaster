#! /usr/bin/env python
"""PANTILT-TRANSFORMATION MODULE

This module use Numpy framework to compute the omogeneous transformation matrix
for a camera mounted on a pantilt.
"""
from numpy import matrix, cos, sin, shape, copysign

class PanTiltFrame(object) :
    """This class is used to compute an omogeneous transformation matrix
    to bring point expressed in BASE_FRAME in CAMERA_FRAME.

    BASE_FRAME is the reference frame for the pan-tilt camera.

    CAMERA_FRAME is the reference frame for the ideal camera center.

    Attributes:
        camera_fixed_rotation (numpy.matrix)
            This is a static transformation matrix that can be used to match
            the ideal CAMERA_FRAME with the real camera frame.

        a (float)
            `a` is the horizontal offset of the camera respect to BASE_FRAME.

        d (float)
            `d` is the vertical offset of the camera respect to BASE_FRAME
    """

    camera_fixed_rotation = matrix([ 
        [1,0,0,0],
        [0,1,0,0],
        [0,0,1,0],
        [0,0,0,1]])

    def __init__(self,a,d,camera_rotation=[]) :
        self.a = a
        self.d = d
        # Replace the default camera_fixed_rotation matrix with the passed one.
        if shape(camera_rotation) == (4,4) :
            self.camera_fixed_rotation = camera_rotation

    def transformation_matrix(self,pan,tilt) :
        """This function returns the omogeneous transformation matrix
        that transform points in BASE_FRAME in CAMERA_FRAME according to
        `pan` and `tilt` values.

        PARAMS:
            pan (float)     : pan angle in radiants
            tilt (float)    : tilt angle in radiants

        RETURNS:
            tm (numpy.matrix)
        """
        tm = matrix([ [cos(pan)*cos(tilt), -sin(tilt)*cos(pan), sin(pan), self.a*cos(tilt)*cos(pan)],
                [sin(pan)*cos(tilt), -sin(tilt)*sin(pan), -cos(pan), self.a*cos(tilt)*sin(pan)],
                [ sin(tilt), cos(tilt), 0, self.a*sin(tilt) + self.d],
                [0,0,0,1] ])
        return tm*self.camera_fixed_rotation 

    def translation_to_camera(self,pan,tilt) :
        """This function returns the translation vector between origin of
        BASE_FRAME and origin of CAMERA_FRAME according to `pan` and `tilt`
        values.

        PARAMS:
            pan (float)     : pan angle in radiants
            tilt (float)    : tilt angle in radiants

        RETURNS:
            tm (numpy.matrix)
        """
        tm = self.transformation_matrix(pan,tilt)
        return tm[0:3,3]

    def rotation_to_camera(self,pan,tilt) :
        """This function returns the rotation matrix between BASE_FRAME and
        CAMERA_FRAME according to `pan` and `tilt` values.

        PARAMS:
            pan (float)     : pan angle in radiants
            tilt (float)    : tilt angle in radiants

        RETURNS:
            tm (numpy.matrix)
        """
        tm = self.transformation_matrix(pan,tilt)
        return tm[0:3,0:3]

    def quaternion_to_camera(self,pan,tilt) :
        """This function returns the rotation between BASE_FRAME and
        CAMERA_FRAME expressed in quaterions according to `pan` and `tilt`
        values.

        PARAMS:
            pan (float)     : pan angle in radiants
            tilt (float)    : tilt angle in radiants

        RETURNS:
            tm (numpy.matrix)
        """
        #TODO: Check tis formula.
        R = self.rotation_to_camera(pan,tilt)
        trace = R[0,0] + R[1,1] + R[2,2]
        r = (1+trace)**0.5
        w = 0.5*r
        x = copysign(0.5*(1+R[0,0]-R[1,1]-R[2,2])**0.5,R[2,1]-R[1,2])
        y = copysign(0.5*(1-R[0,0]+R[1,1]-R[2,2])**0.5,R[0,2]-R[2,0])
        z = copysign(0.5*(1-R[0,0]-R[1,1]+R[2,2])**0.5,R[1,0]-R[0,1])

        return matrix([x,y,z,w])

