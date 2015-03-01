#!/usr/bin/python

"""
Laser Gimbal Main Program
Bolling/Gola 2015
"""
"""
import Adafruit_BBIO.UART as UART
import Adafruit_BBIO.PWM as PWM
from math import sqrt
import serial
import threading 
"""
import cv2
import numpy as np

current_servo_x = 7.5
current_servo_y = 7.5
cp = .01
x_servo = "P9_14"
y_servo = "P9_16"
valid = 0
size_to_target = {1:(1,2),
                  2:(1,3),
                  3:(2,4)}

#repeatedly takes measurements with the laser...
def take_measurements():
    while 1:
        if(valid):
            ser.write("*00004#")
            for x in range(0,3):
                s = ser.readline()
                print(s)

# get ball position, change servo position accordingly
def track_ball():
    #Get Ball position
    x,y,size = 0,0,0
        
    #Calculate desired ball position based on distance
    size_int = int(round(size))
    (target_x,target_y) = size_to_target[size_int]
    x_err = x - target_x
    y_err = y - target_y

    #control shit
    current_servo_x += x_err*cp
    current_servo_y += y_err*cp
    current_servo_x = min(current_servo_x,10)
    current_servo_x = max(current_servo_x,5)
    current_servo_y = min(current_servo_y,10)
    current_servo_y = max(current_servo_y,5)

    #check if we're on target
    valid = sqrt(x_err**2 + y_err**2) < size


#Initialize Servo PWM control
"""
PWM.start(x_servo,current_servo_x,50,0)
PWM.start(y_servo,current_servo_y,50,0)

#Initialize UART for laser data
UART.setup("UART1")
ser = serial.Serial(port = "/dev/ttyO1", baudrate=115200,timeout=1)
ser.close()
ser.open()

t = threading.Thread(target=take_measurements)
t.daemon = True
t.start()
"""


cap = cv2.VideoCapture(0)

while 1:
    h,s,v = 100,100,100

    _, frame = cap.read()

    #converting to HSV
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    # Normal masking algorithm
    lower_blue = np.array([127, 98, 118])
    upper_blue = np.array([178, 255, 255])

    mask = cv2.inRange(hsv,lower_blue, upper_blue)
    kernel_close = np.ones((21,21),np.uint8)
    kernel_open = np.ones((11, 11), np.uint8)
    #kernel_erode = np.ones((4, 4), np.uint8)
    #kernel_dilate = np.ones((8, 8), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel_close)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_open)

    mask = cv2.GaussianBlur(mask,(15,15),0)
    circles = cv2.HoughCircles(mask,cv2.cv.CV_HOUGH_GRADIENT,1,1600, param1 = 50, param2 = 20)

    if circles != None:
        for i in circles[0,:]:
            # draw the outer circle
            #cv2.circle(result,(i[0],i[1]),i[2],(0,255,0),2)
            # draw the center of the circle
            #cv2.circle(result,(i[0],i[1]),2,(0,0,255),3)
            print (i[0], i[1])

    """
    track_ball()
    PWM.set_duty_cycle(x_servo,current_servo_x)
    PWM.set_duty_cycle(y_servo,current_servo_y)
    """

cap.release()

