import cv2
import imutils
import threading
import numpy as np
import serial

#Setup a serial (USB) communication with the arduino
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser.reset_input_buffer()

##########CAMERA##########
def callback(value):
    pass

def create_trackbars():
    for i in ["MIN", "MAX"]:
        v = 0 if i == "MIN" else 255
        for j in "HSV":
            cv2.createTrackbar("%s_%s" % (j, i), "trackbars", v, 255, callback)

def get_trackbar_values():
    values = []
    for i in["MIN", "MAX"]:
        for j in "HSV":
            v = cv2.getTrackbarPos("%s_%s" % (j, i), "trackbars")
            values.append(v)
    return values


def getXY(frame):
  frame_to_mask = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
  mask = cv2.inRange(frame_to_mask,
                       (H_min,S_min,V_min,),
                       (H_max,S_max,V_max))
  #blurred = cv2.GaussianBlur(frame, (11,11), 0)
  #maskErode = cv2.erode(mask, None, iterations=2)
  maskDilate = cv2.dilate(mask, None, iterations=2)
  contr = cv2.findContours(maskDilate.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  contr= imutils.grab_contours(contr)
  if len(contr) > 0:
      c = max(contr, key=cv2.contourArea)
      ((x,y), radius) = cv2.minEnclosingCircle(c)
     return x, y, mask


def showWindows(frame1, frame2, mask1, mask2):
    cv2.imshow('video1', frame1)
    cv2.imshow("mask1", mask1)
    cv2.imshow('video2', frame2)
    cv2.imshow("mask2", mask2)

######MATH########
def scaleFactor(num, factor):
    num = num/factor
    return num

def calc2D(x, y):
    #A, D equation: sin(angle+1/4pi)*mag
    #B, C equation: sin(angle-1/4pi)*mag
    #This treats the XY as if it is a joystick
    angle =  math.atan2(y, x)
    mag = math.sqrt(x**2 + y**2)
    pi = math.pi
    out1 = math.sin(angle+(pi/4))*mag
    out2 = math.sin(angle-(pi/4))*mag
    return out1, out2

def calc3D(x, y, z):
    #A, D equation: sin(angle+1/4pi)*mag
    #B, C equation: sin(angle-1/4pi)*mag
    #This treats it like a 2d joystick, except ew are ignoring the the magnitude. The magnitude
    #is from the height of the fish
    offset = 0
    angle = math.atan2(y, x)
    mag = z - offset
    pi = math.pi
    out1 = math.sin(angle+(pi/4))*mag
    out2 = math.sin(angle-(pi/4))*mag
    return out1, out2

def writeOut(out1, out2):
    ser.write(b"{}, {}\n".format(out1, out2))

#Setup Cameras
width=720
height=480
flip=2
font=cv2.FONT_HERSHEY_SIMPLEX

camSet1 = "nvarguscamerasrc sensor-id=0 !video/x-raw(memory:NVMM), width=(int)3240, height=(int)2464, framerate=(fraction)15/1 ! nvvidconv flip-method=0 ! video/x-raw, width=(int)960, height=(int)540, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink"
camSet2 = "nvarguscamerasrc sensor-id=1 !video/x-raw(memory:NVMM), width=(int)3240, height=(int)2464, framerate=(fraction)15/1 ! nvvidconv flip-method=0 ! video/x-raw, width=(int)960, height=(int)540, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink"
cam1=cv2.VideoCapture(camSet1, cv2.CAP_GSTREAMER)
cam2=cv2.VideoCapture(camSet2, cv2.CAP_GSTREAMER)

cv2.namedWindow("trackbars", 0)
create_trackbars()

  
while True:
    #get each frame
    _, frame1 = cam1.read() #this will be the right camerra (FB)
    _, frame2 = cam2.read() #back camera (LR, UD)
    #get the XY's of the fish (adding z soon)
    y, p, mask1 = getXY(frame1) #y is the x axis of the right camera
    x, z, mask2= getXY(frame2) #x is the x axis of the bottom camera
    
    out1, out2 = calc2D(x/960, y/960) #this assumes the cameras are perfectly square, fix this
    
    writeOut(out1, out2)
    
    showWindows(frame1, frame2, mask1, mask2)
    
    key = cv2.waitKey(1)
    if key == 27:
        break

#kill all cameras
cam1.release()
cam2.release()
cv2.destroyAllWindows()
