import cv2
import imutils
import threading
import numpy as np

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


width=720
height=480
flip=2
font=cv2.FONT_HERSHEY_SIMPLEX
#camSet1='nvarguscamerasrc sensor-id=0 ee-mode=1 ee-strength=0 tnr-mode=2 tnr-strength=1 wbmode=3 ! video/x-raw(memory:NVMM), width=1280, height=720, framerate=29/1,format=NV12 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(width)+', height='+str(height)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! videobalance contrast=1.3 brightness=-.2 saturation=1.2 ! appsink drop=True'
#camSet2='nvarguscamerasrc sensor-id=1 00ee-mode=1 ee-strength=0 tnr-mode=2 tnr-strength=1 wbmode=3 ! video/x-raw(memory:NVMM), width=1280, height=720, framerate=29/1,format=NV12 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(width)+', height='+str(height)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! videobalance contrast=1.3 brightness=-.2 saturation=1.2 ! appsink drop=True'

#camSet1='nvarguscamerasrc sensor_id=0'
#camSet2='nvarguscamerasrc sensor_id=1'

#camSet='nvarguscamerasrc sensor-id=0 ! video/x-raw(memory:NVMM), width=3264, height=2464, framerate=21/1,format=NV12 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(width)+', height='+str(height)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
#camSet ='v4l2src device=/dev/video1 ! video/x-raw,width='+str(width)+',height='+str(height)+',framerate=20/1 ! videoconvert ! appsink'

camSet1 = "nvarguscamerasrc sensor-id=0 !video/x-raw(memory:NVMM), width=(int)3240, height=(int)2464, framerate=(fraction)15/1 ! nvvidconv flip-method=0 ! video/x-raw, width=(int)960, height=(int)540, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink"
camSet2 = "nvarguscamerasrc sensor-id=1 !video/x-raw(memory:NVMM), width=(int)3240, height=(int)2464, framerate=(fraction)15/1 ! nvvidconv flip-method=0 ! video/x-raw, width=(int)960, height=(int)540, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink"
cam1=cv2.VideoCapture(camSet1, cv2.CAP_GSTREAMER)
cam2=cv2.VideoCapture(camSet2, cv2.CAP_GSTREAMER)

cv2.namedWindow("trackbars", 0)
create_trackbars()

while True:
    _, frame1 = cam1.read()
    _, frame2 = cam2.read()
    frame_to_mask1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
    frame_to_mask2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)
    H_min, S_min, V_min, H_max, S_max, V_max = get_trackbar_values()

    mask1 = cv2.inRange(frame_to_mask1,
                       (H_min,S_min,V_min,),
                       (H_max,S_max,V_max))
    mask2 = cv2.inRange(frame_to_mask2,
                       (H_min,S_min,V_min,),
                       (H_max,S_max,V_max))
    

    blurred1 = cv2.GaussianBlur(frame1, (11,11), 0)
    maskErode1 = cv2.erode(mask1, None, iterations=2)
    maskDilate1 = cv2.dilate(mask1, None, iterations=2)
    contr1 = cv2.findContours(maskDilate1.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contr1= imutils.grab_contours(contr1)
    if len(contr1) > 0:
        c1 = max(contr1, key=cv2.contourArea)
        ((x1,y1), radius1) = cv2.minEnclosingCircle(c1)
        #cv2.circle(frame1, (int(x1), int(y1)), int(radius1), (0, 255, 255),2)


    blurred2 = cv2.GaussianBlur(frame2, (11,11), 0)
    maskErode2 = cv2.erode(mask2, None, iterations=2)
    maskDilate2 = cv2.dilate(mask2, None, iterations=2)
    contr2 = cv2.findContours(maskDilate2.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contr2= imutils.grab_contours(contr2)
    if len(contr2) > 0:
        c2 = max(contr2, key=cv2.contourArea)
        ((x2,y2), radius2) = cv2.minEnclosingCircle(c2)
        #cv2.circle(frame2, (int(x2), int(y2)), int(radius2), (0, 255, 255),2)

    
    
    cv2.imshow('video1', frame1)
    cv2.imshow("mask1", mask1)
    cv2.imshow('video2', frame2)
    cv2.imshow("mask2", mask2)
    key = cv2.waitKey(1)
    if key == 27:
        break

cam1.release()
cam2.release()
cv2.destroyAllWindows()
