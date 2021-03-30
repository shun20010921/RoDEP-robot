#!/usr/bin/env python
import serial,time,sys,struct,threading
import rospy
from sensor_msgs.msg import Joy
from stm_communication.msg import stm_protocol

def send_stm(flag,type,data):
    stm_msg.flag=flag
    stm_msg.data=type<<8 | data
    stm_pub.publish(stm_msg)

def send_stm(flag,data):
    stm_msg.flag=flag
    stm_msg.data=data
    stm_pub.publish(stm_msg)

def callback(data):
    global past
    if not past==None:
        if  (past.axes[1] != data.axes[1]):
            send_stm(2,1,int(data.axes[1]*-1*100+100))
    else:
        pass
    past=data

def main():
    global i
    rospy.init_node('joy_stm', anonymous=True)
    rospy.Subscriber('joy', Joy, callback, queue_size=10)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        ser.close()
        sys.exit()


stm_pub = rospy.Publisher('/stm', stm_protocol, queue_size=1)
stm_msg = stm_protocol()
past=None


if __name__ == '__main__':
    main()