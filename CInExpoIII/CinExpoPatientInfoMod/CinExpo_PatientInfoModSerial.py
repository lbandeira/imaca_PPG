# coding=utf-8
import serial
import kivy
import random
import time
import pyrebase
import sys

from kivy.app import App
from kivy.uix.stacklayout import StackLayout
from kivy.uix.floatlayout import FloatLayout

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.core.window import Window

from datetime import datetime
from time import sleep

debug = 1

temp = ecg = ox = bpm = sis = dia = air = gcs = 0
dSis =  dAir = 0 # These variables measure the change of systolic blood pressure and respiratory rate

GCSmsg = 'GCS:'
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
iMacaDB = "/Type1/-KxUd8I_LI7h3558Gkga/"
Window.clearcolor = (0.92, 0.94, 0.96, 1)
pad = 0

def GCS_Points(GCS):
  if(GCS >= 13 and GCS <= 15): return 4
  elif(GCS >= 9 and GCS <= 12): return 3
  elif(GCS >= 6 and GCS <= 8 ): return 2
  elif(GCS <= 5): return 1
  return 0;

def SBP_Points(SBP):
  if(SBP > 89): return 4
  elif(SBP >= 76 and SBP <=89): return 3;
  elif(SBP >= 50 and SBP <= 75 ): return 2;
  elif(SBP >= 1 or SBP <= 49): return 1;
  else: return 0;

def RR_Points(RR):
  if(RR >= 10 and RR <= 29): return 4
  elif(RR > 29): return 3;
  elif(RR >= 6 and RR <= 9 ): return 2;
  elif(RR <= 5): return 1;
  else: return 0;

def RTS(GCS, SBP, RR):
  rts = 0.9368 * GCS_Points(GCS) + 0.7326 * SBP_Points(SBP) + 0.2908 * RR_Points(RR)
  print("in RTS function: ", 0.9368 * GCS_Points(GCS), 0.7326 * SBP_Points(SBP), 0.2908 * RR_Points(RR), rts)

  return rts

def Send_Alert(dSis, dAir, sis, air):
    msg = ""
    if(dSis < 0 or sis <= 75):
        msg = msg + "Pressão baixou, favor calcular GCS"
    elif(dAir < 0 and air <=9):
        msg = msg + "Respiração baixa, favor medir pressão e calcular GCS"
    elif(dAir > 0 and air > 29):
        msg = msg + "Respiração alta, favor medir pressão e calcular GCS"
    print(msg)
    return msg

class PatientInfoScreen(FloatLayout):

                def __init__(self, **kwargs):
                    global gcs, ser, RTS, GCSbox, sis, air, RTSBox, GCSbox, Temp, BPM, Ox, ECG, Air, Press, Alert, dSis, dAir
                    super(PatientInfoScreen, self).__init__(**kwargs)
                    
                    # Criação dos objetos graficos
                    
                    Temp = Button( pos = [10, 660], text='Temp:', background_normal= u'Buttons/bluBtn.jpg', font_size=34, size_hint= [.3, .1])
                    self.add_widget(Temp)
                    
                    ECG = Button( pos = [10, 540], text='ECG:', font_size=34, background_normal= u'Buttons/bluBtn.jpg', size_hint= [.3, .1])
                    self.add_widget(ECG)                  
                    
                    Ox = Button( pos = [10, 420], text='Spo2:', font_size=34, background_normal= u'Buttons/bluBtn.jpg', size_hint= [.3, .1])
                    self.add_widget(Ox)

                    BPM = Button( pos = [10, 300], text='BPM:', font_size=34, background_normal= u'Buttons/bluBtn.jpg', size_hint= [.3, .1])
                    self.add_widget(BPM)
                    
                    Air = Button( pos = [10, 180], text='Breathing \nRate:', background_normal= u'Buttons/bluBtn.jpg', font_size=34, size_hint= [.3, .1])
                    self.add_widget(Air)
                    
                    Press = Button( pos = [10, 60], text='Blood\nPressure:' , background_normal= u'Buttons/bluBtn.jpg',   font_size=34,size_hint= [.3, .1])
                    self.add_widget(Press)                               
                    
                    GCSbox = TextInput( pos = [520, 600], hint_text = GCSmsg, font_size = 36, multiline=False, size_hint= [.3, .1])
                    self.add_widget(GCSbox)

                    RTSBox = Button( pos = [500, 200], text='RTS:', font_size=48, background_normal= u'Buttons/greBtn.jpg', size_hint= [.3, .2])
                    self.add_widget(RTSBox)

                    Logo=  Button( pos = [500, 0], background_normal= u'Logo.png', background_down = u'Logo.png',size_hint= [.3, .3])
                    self.add_widget(Logo)
 
                    Alert = Button( pos = [380, 400], text='Alert:' , background_normal= u'Buttons/greBtn.jpg', font_size=34, size_hint= [.6, .1])
                    self.add_widget(Alert)
 
                    # This function is called when the user presses enter, updating the value of the gcs variable
                    def on_enter(instance):
                        global gcs
                        gcs = int(GCSbox.text)
                        
                    GCSbox.bind(on_text_validate = on_enter)
                    Clock.schedule_interval(self.update, 30 / 60.0)                   
	
                def update(self, dt):
                    global sis, air, gcs, ser, RTSBox, GCSbox, Temp, BPM, Ox, ECG, Air, Press, Alert, dSis, dAir

## Descomentar tudo que tem "ser." para ler coisas da serial e depois comentar todos os "start =" e comentar o que tem random.
                    start = ser.readline().strip()
                    start = start.decode('utf-8')
##                    start = 'b'
                    if(start == 'b'):
                        print("begin")
##                        start = 'a'

##                        temp = round(random.uniform(0, 63 ), 2) 
##                        ecg  = round(random.uniform(0, 5), 2) 
##                        bpm  = random.randint(40, 110)
##                        ox   = random.randint(0, 100)
##                        air  = random.randint(0,40)
##                        sis  = random.randint(1, 160)
##                        dia = random.randint(30, 120)

## Descomentar aqui para pegar da serial                        
                        temp = ser.readline().strip()
                        ecg  = ser.readline().strip()
                        bpm  = ser.readline().strip()
                        ox   = ser.readline().strip()
                        

                        if(debug):

                            print(temp)
                            print(ecg)
                            print(ox)
                            print(bpm)
                            
                        try:
                           ecg = float(ecg)
                           ecg = str(ecg)
                           ECG.text = "ECG: " + ecg
                           db.child(iMacaDB).update({"ecg": float(ecg)})
                        except:
                           ECG.text = ECG.text
                        
                        try:
                           temp = float(temp)
                           temp = str(temp)
                           Temp.text = "Temp: " + temp + "°C"
                           db.child(iMacaDB).update({"Temperatura": temp})
                        except:
                           Temp.text = Temp.text
                    

                        try:
                            ox = int(ox)
                            ox = str(ox)
                            Ox.text = "Spo2: " + ox + "%"
                            db.child(iMacaDB).update({"Spo2": ox})
                        except:
                            Ox.text = Ox.text
			
                        try:
                            bpm = int(bpm)
                            bpm = str(bpm)
                            BPM.text = "BPM: " + bpm
                            db.child(iMacaDB).update({"BPM": int(bpm)})
                            Alert.text = "Verificando taxa respiratória"
                        except:
                            BPM.text = BPM.text
                            
                    if(start == 'a'):

                            air = ser.readline().strip()
##                            start = 's'
                            print(air)
                            try:
                                    air = int(air)
                                    dAir = air - dAir
                                    msg = Send_Alert(dSis, dAir, sis, air)
                                    dAir = air
                                    Alert.text = msg
                                    
                                    air = str(air)
                                    Air.text = air + "\nbreaths/min"
                                    db.child(iMacaDB).update({"Air": int(air)})
                                    
                            except:
                                    Air.text = Air.text
		
                    if(start == 's'):
			
                            sis = ser.readline().strip()
##                            start = 'd'
                            print(sis)
                            try:
                                    sis = int(sis)
                                    dSis = sis - dsis
                                    msg = Send_Alert(dSis, dAir, sis, air)
                                    dSis = sis
                                    Alert.text = msg
                                    sis = str(sis)
                                    Press.text = "Pressão:\n" + sis + '/' + str(dia)
                                    db.child(iMacaDB).update({"Sis": sis})

                            except:
                                    Press.text = Press.text

                    if(start == 'd'):
			
                            dia = ser.readline().strip()
                        
##                            start = 'b'
                            print(dia)
                            try:
                                    dia = int(dia)
                                    dia = str(dia)
                                    Press.text = "Pressão:\n" + str(sis) + '/' + dia
                                    press = str(sis) + '-' + dia
                                    db.child(iMacaDB).update({"Diastolica": press})                                    
                                    
                            except:
                                    Press.text = Press.text
                    if(start == 'p'):
                            peso   = ser.readline().strip() 

                            try:
                              peso = float(peso)
                              print(peso)
                              #db.child(iMacaDB).update({"Peso": peso})
                            except ValueError :
                              print("waiting for peso... ValueError: %s" %peso)  
                    
                                    
                    rts = RTS(gcs, sis, air)
                    RTSBox.text = "RTS: " + str(rts)
                    frts = str(rts)
                    frts = frts[0:4]
                    RTSBox.text = "RTS: " + frts

                    db.child(iMacaDB).update({"RTS": frts})
                                        
                    # This part here changes the RTS box color according to the value, red -> urgent, yellow -> not good, green -> good
                    
                    if(rts < 6 and rts > 4):
                        RTSBox.background_normal = u'Buttons/yelBtn.jpg'
                        Alert.background_normal = u'Buttons/yelBtn.jpg'
                        
                    elif(rts < 4):
                        RTSBox.background_normal = u'Buttons/redBtn.jpg'
                        Alert.background_normal = u'Buttons/redBtn.jpg'
                        
                    else:
                        RTSBox.background_normal = u'Buttons/greBtn.jpg'
                        Alert.background_normal = u'Buttons/greBtn.jpg'
                        
                
class PatientInfoApp(App):

    def build(self):
        return PatientInfoScreen()

PatientInfoApp().run()