#!/usr/bin/env python
import serial,time,sys,struct,threading
import rospy
from stm_communication.msg import stm_protocol

def send_stm(flag,data):
    stm_msg.flag=flag
    stm_msg.data=data
    stm_pub.publish(stm_msg)


def main():
    global i
    rospy.init_node('serial-test', anonymous=True)
    try:
        r = rospy.Rate(10) # 10hz
        while not rospy.is_shutdown():
            for i in range(0,65535):
                send_stm(1,i)
                r.sleep()
    except KeyboardInterrupt:
        sys.exit()


stm_pub = rospy.Publisher('/stm', stm_protocol, queue_size=1)
stm_msg = stm_protocol()


if __name__ == '__main__':
    main()