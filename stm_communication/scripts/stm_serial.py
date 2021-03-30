#!/usr/bin/env python
import serial,time,sys,struct
import rospy,math
from stm_communication.msg import stm_protocol

Header=chr(0xFF)
i=1

# 0: 1111 1111 |HEADER_1 0xFF
# 1: 1100 0011 |HEADER_2 0xC3
# 2: aaaa aaaa |a:vel_norm(float)
# 3: aaaa aaaa |
# 4: bbbb bbbb |b:vel_theta(0>254 -> 0>=theta>2pi)
# 5: cccc cccc |c:omega(float)
# 6: cccc cccc |
# 7: xxxx xxxx |Servo1 (0<254 -> 0<180)
# 8: xxxx xxxx |Servo2
# 9: xxxx xxxx |Servo3
# 10:xxxx xxxx |Servo4
# 11:xxxx xxxx |Servo5
# 12:xxxx xxxx |Servo6

ser = serial.Serial('/dev/ttyS0',921600,timeout=10)

def to_Byte(data): #0-65535 can send
    high = chr(int((data>>8)&0xFF))
    low = chr(int(data&0xFF))
    return {high,low}
    
def convert_float(data): # |1|4|11  -8~7  float to bin
    if data == 0:
        return 0
    else:
        res = 0
        ex = 0
        if data<0:
            res|=1<<15
            data = abs(data)
        for a in range(-8,8):#-8~7
            if data<(2**(a+2)):
                ex = a
                break
        if ex == 0:
            print("error")
            return
        data -= 2**(ex+1)
        for a in range(10):
            if data >= 2**(ex-a):
                res|=1<<(10-a)
        ex = to_bin(ex)
        res|=ex<<11
        return res

def to_bin(data):   #bin to float
    res = 0
    if data<0:
        res |= 1<<3
        data += 8
    for a in range(3):
        if data >= (2**(2-a)):
            data -= 2**(2-a)
            res |= 1<<(2-a)
    return res
    
def send_stm(data):
    try:
        for a in data:
            ser.write(a)
    except Exception as e:
        print(e)

def callback(data):
    send_data = {}

    send_data.append(chr(0xFF))
    send_data.append(chr(0xC3))
    send_data.append(to_Byte(convert_float(data.vel_norm)))
    send_data.append(chr(int((data.vel_theta + math.pi) / 2*math.pi * 0xFF)))  # -pi < data < pi -> 0<0xFF
    send_data.append(to_Byte(convert_float(data.omega))
    for a in data.Servo_angle:
        send_data.append(chr(int(a/180 * 0xFF))) # 0<pi -> 0<0xFF
    send_stm(send_data)

def stm():
    rospy.init_node('stm_serial', anonymous=True)
    rospy.Subscriber('stm',stm_protocol, callback)

    rospy.spin()

if __name__ == '__main__':
    stm()