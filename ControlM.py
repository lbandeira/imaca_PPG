import time
import serial
import pyrebase
import random
import sys
from datetime import datetime
from time import sleep
from bitstring import BitArray

def GCS_Points(GCS):
  if(GCS >= 13 and GCS <= 15): return 4
  elif(GCS >= 9 and GCS <= 12): return 3
  elif(GCS >= 6 and GCS <= 8 ): return 2
  elif(GCS == 4 or GCS == 5): return 1
  return 0;

def SBP_Points(SBP):
  if(SBP > 89): return 4
  elif(SBP >= 76 and SBP <= 89): return 3;
  elif(SBP >= 50 and SBP <= 75 ): return 2;
  elif(SBP >= 1 or SBP <= 49): return 1;
  else: return 0;

def RR_Points(RR):
  if(RR >= 10 and RR <= 29): return 4
  elif(RR > 29): return 3;
  elif(RR >= 6 and RR <= 9 ): return 2;
  elif(RR >= 1 or RR <= 5): return 1;
  else: return 0;

def RTS(GCS, SBP, RR):
  rts = 0.9368 * GCS_Points(GCS) + 0.7326 * SBP_Points(SBP) + 0.2908 * RR_Points(RR)
  return rts


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

  if(start == "b"):
    print("comecou medicao")
    temp = ser.readline().strip()
    ecg  = ser.readline().strip()
    bpm  = ser.readline().strip()
    ox   = ser.readline().strip()  
         
    try:
      temp = float(temp)
      print(temp)
      #db.child(iMacaDB).update({"Temperatura": temp})
    except:
      print("waiting for temp... ValueError: %s" %temp)

    try:
      ecg = float(ecg)
      print(ecg)
      #db.child(iMacaDB).update({"ecg": ecg})
    except:
      print("waiting for ecg... ValueError: %s" %ecg)
      
    try:
      bpm = int(bpm)
      print(bpm)
      #db.child(iMacaDB).update({"BPM": bpm})
    except:
      print("waiting for bpm... ValueError: %s" %bpm)
     
    try:
      ox = float(ox)
      print(ox)
      #db.child(iMacaDB).update({"Spo2": ox})
    except:
      print("waiting for spo2... ValueError: %s" %ox)


  if(start == 'a'):

    air = ser.readline().strip() 
    try:
      air = int(air)
      print(air)
      #db.child(iMacaDB).update({"Air": int(air)})
    except:
      print("waiting for air")

  
  if(start == 'p'):
    peso   = ser.readline().strip() 

    try:
      peso = float(peso)
      print(peso)
      #db.child(iMacaDB).update({"Peso": peso})
    except ValueError :
      print("waiting for peso... ValueError: %s" %peso)  

  if(start == 's'):
    sis   = ser.readline().strip() 

    try:
      sis = int(sis)
      print(sis)
      #db.child(iMacaDB).update({"Sistolica": sis})
    except ValueError :
      print("waiting for sisotlica... ValueError: %s" %sis)  

  if(start == 'd'):
    dia   = ser.readline().strip() 

    try:
      dia = int(dia)
      print(dia)
      if(sis != 0 and dia !=0):
        pulse_pressure = sis - dia
      #db.child(iMacaDB).update({"Sistolica": dia})
    except ValueError :
      print("waiting for diasotlica... ValueError: %s" %dia)  


  time.sleep(0.5)

# sem BP = 11s, com BP = 13s, com peso = 15s