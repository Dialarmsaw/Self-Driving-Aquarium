import cv2
import threading
import numpy as np
import imutils


class CSI_Camera:

    def __init__(self):
        # Initialize instance variables
        # OpenCV video capture element
        self.video_capture = None
        # The last captured image from the camera
        self.frame = None
        self.grabbed = False
        # The thread where the video capture runs
        self.read_thread = None
        self.read_lock = threading.Lock()
        self.running = False

    def open(self, gstreamer_pipeline_string):
        try:
            self.video_capture = cv2.VideoCapture(
                gstreamer_pipeline_string, cv2.CAP_GSTREAMER
            )
            # Grab the first frame to start the video capturing
            self.grabbed, self.frame = self.video_capture.read()

        except RuntimeError:
            self.video_capture = None
            print("Unable to open camera")
            print("Pipeline: " + gstreamer_pipeline_string)


    def start(self):
        if self.running:
            print('Video capturing is already running')
            return None
        # create a thread to read the camera image
        if self.video_capture != None:
            self.running = True
            self.read_thread = threading.Thread(target=self.updateCamera)
            self.read_thread.start()
        return self

    def stop(self):
        self.running = False
        # Kill the thread
        self.read_thread.join()
        self.read_thread = None

    def updateCamera(self):
        # This is the thread to read images from the camera
        while self.running:
            try:
                grabbed, frame = self.video_capture.read()
                with self.read_lock:
                    self.grabbed = grabbed
                    self.frame = frame
            except RuntimeError:
                print("Could not read image from camera")
        # FIX ME - stop and cleanup thread
        # Something bad happened

    def read(self):
        with self.read_lock:
            frame = self.frame.copy()
            grabbed = self.grabbed
        return grabbed, frame

    def release(self):
        if self.video_capture != None:
            self.video_capture.release()
            self.video_capture = None
        # Now kill the thread
        if self.read_thread != None:
            self.read_thread.join()


""" 
gstreamer_pipeline returns a GStreamer pipeline for capturing from the CSI camera
Flip the image by setting the flip_method (most common values: 0 and 2)
display_width and display_height determine the size of each camera pane in the window on the screen
Default 1920x1080
"""


def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1920,
    capture_height=1080,
    display_width=1920,
    display_height=1080,
    framerate=30,
    flip_method=0,
):
    return (
        "nvarguscamerasrc sensor-id=%d ! "
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )


############################################################
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






def doAll(cam1, cam2):
    ################CAM1##########################
    frame_to_mask = cv2.cvtColor(cam1, cv2.COLOR_BGR2HSV)
    H_min, S_min, V_min, H_max, S_max, V_max = get_trackbar_values()
   
    mask = cv2.inRange(frame_to_mask,
                       (H_min,S_min,V_min,),
                       (H_max,S_max,V_max))
    
    blurred = cv2.GaussianBlur(cam1, (11,11), 0)
    maskErode = cv2.erode(mask, None, iterations=2)
    maskDilate = cv2.dilate(mask, None, iterations=2)
    contr = cv2.findContours(maskDilate.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contr = imutils.grab_contours(contr)
    if len(contr) > 0:
        c = max(contr, key=cv2.contourArea)
        ((x,y), radius) = cv2.minEnclosingCircle(c)
        cv2.circle(cam1, (int(x), int(y)), int(radius), (0, 255, 255),2)
    cv2.imshow("cam1", cam1)
    cv2.imshow("mask1", mask)
    ###############CAM2######################
    frame_to_mask = cv2.cvtColor(cam2, cv2.COLOR_BGR2HSV)
    H_min, S_min, V_min, H_max, S_max, V_max = get_trackbar_values()
   
    mask = cv2.inRange(frame_to_mask,
                       (H_min,S_min,V_min,),
                       (H_max,S_max,V_max))
    
    blurred = cv2.GaussianBlur(cam2, (11,11), 0)
    maskErode = cv2.erode(mask, None, iterations=2)
    maskDilate = cv2.dilate(mask, None, iterations=2)
    contr = cv2.findContours(maskDilate.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contr = imutils.grab_contours(contr)
    if len(contr) > 0:
        c = max(contr, key=cv2.contourArea)
        ((x,y), radius) = cv2.minEnclosingCircle(c)
        cv2.circle(cam2, (int(x), int(y)), int(radius), (0, 255, 255),2)
    cv2.imshow("cam2", cam2)
    cv2.imshow("mask2", mask)
###############################################################











def run_cameras():
    window_title = "Dual CSI Cameras"
    left_camera = CSI_Camera()
    left_camera.open(
        gstreamer_pipeline(
            sensor_id=0,
            capture_width=1920,
            capture_height=1080,
            flip_method=0,
            display_width=960,
            display_height=540,
        )
    )
    left_camera.start()

    right_camera = CSI_Camera()
    right_camera.open(
        gstreamer_pipeline(
            sensor_id=1,
            capture_width=1920,
            capture_height=1080,
            flip_method=0,
            display_width=960,
            display_height=540,
        )
    )
    right_camera.start()

    if left_camera.video_capture.isOpened() and right_camera.video_capture.isOpened():

        cv2.namedWindow("Cam1", cv2.WINDOW_AUTOSIZE)
        cv2.namedWindow("Cam2", cv2.WINDOW_AUTOSIZE)
        cv2.namedWindow("Mask1", cv2.WINDOW_AUTOSIZE)
        cv2.namedWindow("Mask2", cv2.WINDOW_AUTOSIZE)
        cv2.namedWindow("trackbars", 0)
        create_trackbars()


        try:
            while True:
                _, left_image = left_camera.read()
                _, right_image = right_camera.read()

                

                # This also acts as
                keyCode = cv2.waitKey(30) & 0xFF
                # Stop the program on the ESC key
                if keyCode == 27:
                    break
        finally:

            left_camera.stop()
            left_camera.release()
            right_camera.stop()
            right_camera.release()
        cv2.destroyAllWindows()
    else:
        print("Error: Unable to open both cameras")
        left_camera.stop()
        left_camera.release()
        right_camera.stop()
        right_camera.release()



if __name__ == "__main__":
    run_cameras()
