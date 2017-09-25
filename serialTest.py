import time
import serial
import pyrebase
import random

ser = serial.Serial('COM9', 115200, timeout=0)
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

while 1:

  
  temp = ser.readline().strip()
  ecg = ser.readline().strip()
  bpm = ser.readline().strip()
  ox  = ser.readline().strip()
  peso = ser.readline().strip()
 

  '''
  temp = random.uniform(35, 40)
  ecg = random.uniform(0, 5)
  bpm = random.randint(70, 120)
  ox = random.randint(80, 100)
  '''
  
  try:
  	temp = float(temp)
  	db.update({"temp": temp})
  	print("temp: %.2f " %temp)
  except:
  	print("waiting for temp...")

  try:
  	ecg = float(ecg)
  	db.update({"ecg": ecg})
  	print("ecg: %.2f" %ecg)
  except:
  	print("waiting for ecg...")
  	
  try:
  	bpm = float(bpm)
  	db.update({"pulso": bpm})
  	print("bpm: %.2f " %bpm)
  except:
  	print("waiting for bpm...")
   
  try:
    ox = float(ox)
    db.update({"spo2": ox})
    print("spo2: %.2f " %ox)
  except:
  	print("waiting for spo2...")

  try:
    peso = float(peso)
    db.update({"peso": peso})
    print("peso: %.2f " %peso)
  except:
  	print("waiting for peso...")
  	
  time.sleep(0.5)