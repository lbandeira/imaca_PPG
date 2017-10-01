import time
import serial
import pyrebase
import random
import sys
from datetime import datetime;

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
iMacaDB = "Médico Regulador/Atendimento/ID Maca"
ctrPeso = False

while 1:

  start = ser.readline().strip()
  start = start.decode('utf-8')
  print(start)

  if(start == "s"):
    print("comecou medicao")
    peso = ser.readline().strip()  
    temp = ser.readline().strip()
    ecg  = ser.readline().strip()
    bpm  = ser.readline().strip()
    ox   = ser.readline().strip()

    try:
      peso = float(peso)
      db.child(iMacaDB).update({"Peso": peso})
      print("peso: %.2f " %peso)
    except ValueError :
      print("waiting for peso... ValueError: %s" %peso)
         
    try:
      temp = float(temp)
      db.child(iMacaDB).update({"Temperatura": temp})
      print("temp: %.2f " %temp)
    except:
      print("waiting for temp... ValueError: %s" %temp)

    try:
      ecg = float(ecg)
      db.child(iMacaDB).update({"ecg": ecg})
      print("ecg: %.2f" %ecg)
    except:
      print("waiting for ecg... ValueError: %s" %ecg)
      
    try:
      bpm = float(bpm)
      db.child(iMacaDB).update({"BPM": bpm})
      print("bpm: %.2f " %bpm)
    except:
      print("waiting for bpm... ValueError: %s" %bpm)
     
    try:
      ox = float(ox)
      db.child(iMacaDB).update({"Spo2": ox})
      print("spo2: %.2f " %ox)
    except:
      print("waiting for spo2... ValueError: %s" %ox)