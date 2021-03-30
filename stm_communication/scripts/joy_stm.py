#!/usr/bin/env python

# -*- coding: utf-8 -*-

import serial, time, sys, struct, threading
import rospy, math
from sensor_msgs.msg import Joy
from stm_communication.msg import stm_protocol


class Robot_info:
    def __init__(self):
        self._MAX_NORM_VELOCITY = 255
        self._MAX_THETA_VELOCITY = 20
        self.x = 0  # -1 ~ 1
        self.y = 0  # -1 ~ 1
        self.theta = 0  # -1 ~ 1
        self.past = None

        rospy.Subscriber('joy', Joy, self.callback, queue_size=10)
        self.stm_pub = rospy.Publisher('/stm', stm_protocol, queue_size=1)

    def callback(self, data):
        past = data
        if not past is None:
            if past.axes[0] != data.axes[0]:  # L stick horizontal(left=+1, right=-1)
                pass
            elif past.axes[1] != data.axes[1]:  # L stick vertical(up=+1, down=-1)
                self.theta = data.axes[1]
            elif past.axes[2] != data.axes[2]:  # R stick horizontal(left=+1, right=-1)
                self.x = data.axes[2] * -1
            elif past.axes[5] != data.axes[5]:  # R stick vertical(up=+1, down=-1)
                self.y = data.axes[5]
        else:
            pass

    def update(self):
        stm_com = stm_protocol()

        stm_com.vel_norm = math.sqrt((self._MAX_NORM_VELOCITY * self.x)**2, (self._MAX_NORM_VELOCITY * self.y))
        stm_com.omega = int(254 * (math.atan2(self.y, self.x) + math.pi) / 2 * math.pi)
        stm_com.vel_theta = self._MAX_THETA_VELOCITY * self.y

        self.stm_pub.publish(stm_com)


def main():
    rospy.init_node('joy_stm', anonymous=True)
    robot_info = Robot_info()
    rate = rospy.Rate(60)  # 60hz
    try:
        rate.sleep()
    except KeyboardInterrupt:
        sys.exit()


if __name__ == '__main__':
    main()
