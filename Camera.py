import serial
import time

from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np
from time import sleep


def take_photo():
    print("Hey!")
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 50
    camera.hflip = True

    rawCapture = PiRGBArray(camera, size=(640, 480))
 
    # allow the camera to warmup
    time.sleep(0.1)
    i = 0 
    # capture frames from the camera
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
        image = frame.array

        blur = cv2.blur(image, (3,3))

        #hsv to complicate things, or stick with BGR
        #hsv = cv2.cvtColor(blur,cv2.COLOR_BGR2HSV)
        #thresh = cv2.inRange(hsv,np.array((0, 200, 200)), np.array((20, 255, 255)))

        lower = np.array([76,31,4],dtype="uint8")
        #upper = np.array([225,88,50], dtype="uint8")
        upper = np.array([210,90,70], dtype="uint8")

        thresh = cv2.inRange(blur, lower, upper)
        thresh2 = thresh.copy()

        # find contours in the threshold image
        image, contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

        # finding contour with maximum area and store it as best_cnt
        max_area = 0
        best_cnt = 1
        for cnt in contours:    
            area = cv2.contourArea(cnt)
            if area > max_area:
                max_area = area
                best_cnt = cnt

        # finding centroids of best_cnt and draw a circle there
        M = cv2.moments(best_cnt)
        cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
        #if best_cnt>1:
        cv2.circle(blur,(cx,cy),10,(0,0,255),-1)
        # show the frame
        cv2.imshow("Frame", blur)
        #cv2.imshow('thresh',thresh2)
        #key = cv2.waitKey(1) & 0xFF
        i = i + 1
	# clear the stream in preparation for the next frame
        rawCapture.truncate(0)
	# if the `q` key was pressed, break from the loop
        if i == 70:
            cv2.imwrite('new_image.jpg', blur)
            break

    return cx, cy

ser=serial.Serial("/dev/ttyUSB0",9600)  #change ACM number as found from ls /dev/tty/ACM*
ser.baudrate=9600

ser1=serial.Serial("/dev/ttyACM0",9600)  #change ACM number as found from ls /dev/tty/ACM*
ser1.baudrate=9600

read_ser=ser.readline()
j=0
while j<1:
    read_ser=ser.readline()
    print("Ser:" , read_ser)
    time.sleep(0.1)
    read_ser1 =ser1.readline()
    print("Ser1:" , read_ser1)
    time.sleep(0.1)

    if(read_ser1==b'1\r\n'):
        
        cx, cy = take_photo()
        print("cx: ", cx)
        print("cy: ", cy)
        print("Ser:" , read_ser)
        print("Ser1:" , read_ser1)
        
        i=0
        #while i<20:
            #read_ser=ser.readline()
            #print("Batimento1:" , read_ser)
            #read_ser=ser.readline()
            #print("Ox1:" , read_ser)
            #read_ser=ser.readline()
            #print("ECG1:" , read_ser)
            #read_ser=ser.readline()
            #print("Tem1:" , read_ser)
            #i=i+1

    j=j+1
