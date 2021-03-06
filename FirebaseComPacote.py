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
 
db = firebase.database()
iMacaDB = "M"
ctrPhoto= False
f = open('packet.txt', 'wb')

while 1:

  start = "s"
  #start = start.decode('utf-8')
  print(start)

  if(start == "s"):
    print("comecou medicao")
    photo = random.randint(0, 15)
    peso = random.randint(0, 255)
    temp = round(random.uniform(0, 63 ), 2) 
    ecg  = round(random.uniform(0, 5), 2) 
    bpm  = random.randint(40, 110)
    ox   = random.randint(0, 100) 
    sis = random.randint(0, 31)
    dia = random.randint(0, 31)

    
    pesoBit = BitArray(uint=int(peso), length = 8)

    bpmBit = BitArray(uint=int(bpm), length=7)
    oxBit = BitArray(uint=int(ox), length = 7)
  
    sisBit = BitArray(uint=int(sis), length = 5)
    diaBit = BitArray(uint=int(dia), length = 5)
    photoBit = BitArray(uint=int(photo), length=4)
    fill = BitArray (uint=0, length = 60)

    payload = pesoBit + bpmBit + oxBit + sisBit + diaBit + photoBit + fill

    print (str(pesoBit.bin) + "|" + str(bpmBit.bin) + "|" + str(oxBit.bin) + "|" + str(sisBit.bin) + "|" + str(diaBit.bin) + "|" + str(photoBit.bin) + "|" + str(fill.bin))

    
    print(payload.bin)
    print("\n========\n")
    payload.tofile(f)
    sys.stdout.flush()


    if(ctrPhoto == False):

      photo = int(photo)
      if(photo == 1):
        cx = cy = 11

        #f.write("cx: " + str(cx) + "\n")
        #f.write("cy: " +  str(cy) + "\n")
        #f.flush()
        ctrPhoto = True
    
    try:
      peso = float(peso)
      #db.child(iMacaDB).update({"Peso": peso})
      #f.write("peso: %.2f \n" %peso)
      #f.flush()
    except ValueError :
      print("waiting for peso... ValueError: %s" %peso)
         
    try:
      temp = float(temp)
      #db.child(iMacaDB).update({"Temperatura": temp})
      #f.write("temp: %.2f \n" %temp)
      #f.flush()
    except:
      print("waiting for temp... ValueError: %s" %temp)

    try:
      ecg = float(ecg)
      #db.child(iMacaDB).update({"ecg": ecg})
      #f.write("ecg: %.2f\n" %ecg)
      #f.flush()
    except:
      print("waiting for ecg... ValueError: %s" %ecg)
      
    try:
      bpm = int(bpm)
      #db.child(iMacaDB).update({"BPM": bpm})
      #f.write("bpm: %d \n" %bpm)
      #f.flush()
    except:
      print("waiting for bpm... ValueError: %s" %bpm)
     
    try:
      ox = float(ox)
      #db.child(iMacaDB).update({"Spo2": ox})
      #f.write("spo2: %.2f \n" %ox)
      #f.flush()
    except:
      print("waiting for spo2... ValueError: %s" %ox)
    #f.write("\n==================\n")
    #f.flush()
    time.sleep(0.8)