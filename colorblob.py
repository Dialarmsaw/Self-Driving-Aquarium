import cv2
import imutils

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


cam = cv2.VideoCapture(0)
cv2.namedWindow("mask", cv2.WINDOW_NORMAL)
cv2.namedWindow("trackbars", 0)



create_trackbars()

while True:
    check, frame = cam.read()
    frame_to_mask = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    H_min, S_min, V_min, H_max, S_max, V_max = get_trackbar_values()
   
    mask = cv2.inRange(frame_to_mask,
                       (H_min,S_min,V_min,),
                       (H_max,S_max,V_max))
    
    blurred = cv2.GaussianBlur(frame, (11,11), 0)
    maskErode = cv2.erode(mask, None, iterations=2)
    maskDilate = cv2.dilate(mask, None, iterations=2)
    contr = cv2.findContours(maskDilate.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contr = imutils.grab_contours(contr)
    if len(contr) > 0:
        c = max(contr, key=cv2.contourArea)
        ((x,y), radius) = cv2.minEnclosingCircle(c)
        cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255),2)

    
    
    cv2.imshow('video', frame)
    cv2.imshow("mask", mask)
    print(x, y) #x, y is the center of the biggest color blobs, use this for the 3d tracking
    key = cv2.waitKey(1)
    if key == 27:
        break

cam.release()
cv2.destroyAllWindows()