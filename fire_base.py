import time
import serial
import pyrebase
import random
import sys
from datetime import datetime;
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

ser = serial.Serial('/dev/ttyACM0', 115200, timeout=0)
config = {
    "apiKey": "AIzaSyB8mMEws9sB8822nrgtAzge9fvFiKr4Pms",
    "authDomain": "imacasbesc.firebaseapp.com",
    "databaseURL": "https://imacasbesc.firebaseio.com",
    "projectId": "imacasbesc",
    "storageBucket": "imacasbesc.appspot.com",
    "messagingSenderId": "947414408697"
  };
firebase = pyrebase.initialize_app(config)
 
db = firebase.database()
iMacaDB = "Médico Regulador/Atendimento/ID Maca"
ctrPhoto= False
f = open("sensores.txt", "w")

while 1:

  start = ser.readline().strip()
  start = start.decode('utf-8')
  print(start)

  if(start == "s"):
    print("comecou medicao")
    photo = ser.readline().strip()
    peso = ser.readline().strip()  
    temp = ser.readline().strip()
    ecg  = ser.readline().strip()
    bpm  = ser.readline().strip()
    ox   = ser.readline().strip()

    
    print(bpm)
    print(ox)
    sys.stdout.flush()

    if(ctrPhoto == False):

      photo = int(photo)
      if(photo == 1):
        cx, cy = take_photo()

        f.write("cx: " + str(cx) + "\n")
        f.write("cy: " +  str(cy) + "\n")
        f.flush()
        ctrPhoto = True
    
    try:
      peso = float(peso)
      #db.child(iMacaDB).update({"Peso": peso})
      f.write("peso: %.2f \n" %peso)
      f.flush()
    except ValueError :
      print("waiting for peso... ValueError: %s" %peso)
         
    try:
      temp = float(temp)
      #db.child(iMacaDB).update({"Temperatura": temp})
      f.write("temp: %.2f \n" %temp)
      f.flush()
    except:
      print("waiting for temp... ValueError: %s" %temp)

    try:
      ecg = float(ecg)
      #db.child(iMacaDB).update({"ecg": ecg})
      f.write("ecg: %.2f\n" %ecg)
      f.flush()
    except:
      print("waiting for ecg... ValueError: %s" %ecg)
      
    try:
      bpm = float(bpm)
      #db.child(iMacaDB).update({"BPM": bpm})
      f.write("bpm: %.2f \n" %bpm)
      f.flush()
    except:
      print("waiting for bpm... ValueError: %s" %bpm)
     
    try:
      ox = float(ox)
      #db.child(iMacaDB).update({"Spo2": ox})
      f.write("spo2: %.2f \n" %ox)
      f.flush()
    except:
      print("waiting for spo2... ValueError: %s" %ox)
    f.write("\n==================\n")
    f.flush()
    time.sleep(0.8)


