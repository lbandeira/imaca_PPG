import time
import serial
import pyrebase
import random
import sys
from datetime import datetime
from time import sleep
from bitstring import BitArray



config = {
    "apiKey": "AIzaSyB8mMEws9sB8822nrgtAzge9fvFiKr4Pms",
    "authDomain": "imacasbesc.firebaseapp.com",
    "databaseURL": "https://imacasbesc.firebaseio.com",
    "projectId": "imacasbesc",
    "storageBucket": "imacasbesc.appspot.com",
    "messagingSenderId": "947414408697"
  };
firebase = pyrebase.initialize_app(config)
ser = serial.Serial('COM3', 115200, timeout=0)

db = firebase.database()
iMacaDB = "/sigfox/Atendimento/null/245A6F/-KwGoPq579dJpcKzV-4b/"
ctrPhoto= True
f = open('packet.txt', 'w')

while 1:

  start = ser.readline().strip()
  start = start.decode('utf-8')
  print(start)

  if(start == "s"):
    print("comecou medicao")
    temp = ser.readline().strip()
    ecg  = ser.readline().strip()
    bpm  = ser.readline().strip()
    ox   = ser.readline().strip()
    peso = ser.readline().strip()  

    try:
      peso = float(peso)
      print(peso)
      db.child(iMacaDB).update({"Peso": peso})
      #f.write("peso: %.2f \n" %peso)
      #f.flush()
    except ValueError :
      print("waiting for peso... ValueError: %s" %peso)
         
    try:
      temp = float(temp)
      print(temp)
      db.child(iMacaDB).update({"Temperatura": temp})
      #f.write("temp: %.2f \n" %temp)
      #f.flush()
    except:
      print("waiting for temp... ValueError: %s" %temp)

    try:
      ecg = float(ecg)
      print(ecg)
      db.child(iMacaDB).update({"ecg": ecg})
      #f.write("ecg: %.2f\n" %ecg)
      #f.flush()
    except:
      print("waiting for ecg... ValueError: %s" %ecg)
      
    try:
      bpm = int(bpm)
      print(bpm)
      db.child(iMacaDB).update({"BPM": bpm})
      #f.write("bpm: %d \n" %bpm)
      #f.flush()
    except:
      print("waiting for bpm... ValueError: %s" %bpm)
     
    try:
      ox = float(ox)
      print(ox)
      db.child(iMacaDB).update({"Spo2": ox})
      #f.write("spo2: %.2f \n" %ox)
      #f.flush()
    except:
      print("waiting for spo2... ValueError: %s" %ox)


  if(start == 'a'):

    air = ser.readline().strip() 
    count = 0;

    while(count < 50):

      print('[' + str(air) + ']')
      db.child(iMacaDB).update({"Air": int(air)})

      air = ser.readline().strip() 
      air = air.decode('utf-8')

      count = count+1
    print(air)

