# coding=utf-8
import serial
import kivy
from kivy.app import App
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.core.window import Window

import random
import time
import pyrebase
import sys
from datetime import datetime
from time import sleep

debug = 1
gcs = temp = ecg = ox = bpm = sis = dia = air = 0
GCSmsg = 'Type GCS value here'
#ser = serial.Serial('/dev/ttyACM0', 115200, timeout=0)

Window.clearcolor = (0.92, 0.94, 0.96, 1)

#fontName = r"C:UsersJuliaDocumentsHPx360DocumentsiMacaSiteFontesRiseFiraSans-ExtraBold.otf"

def GCS_Points(GCS):
  if(GCS >= 13 and GCS <= 15): return 4
  elif(GCS >= 9 and GCS <= 12): return 3
  elif(GCS >= 6 and GCS <= 8 ): return 2
  elif(GCS == 4 or GCS == 5): return 1
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
  elif(RR >= 1 or RR <= 5): return 1;
  else: return 0;

def RTS(GCS, SBP, RR):
  rts = 0.9368 * GCS_Points(GCS) + 0.7326 * SBP_Points(SBP) + 0.2908 * RR_Points(RR)
  return rts

class PatientInfoApp(App):

                def build(self):
                    global gcs, ser
                    Layout = StackLayout(padding =  [10, 10, 10, 10], spacing = [15, 10])
                    self.GCSbox = TextInput(hint_text = GCSmsg, size_hint_y=None, multiline=False, height=120, font_size = 36)

                    self.Press=Button( text='Blood\nPressure:' , background_normal= u'/home/pi/Área de Trabalho/PatientInfoMod/Buttons/bluBtn.jpg',   font_size=36,size_hint= [.2, .2])
                    Layout.add_widget(self.Press)

                    self.Temp=Button( text='Temp:', background_normal= u'/home/pi/Área de Trabalho/PatientInfoMod/Buttons/bluBtn.jpg', font_size=36, size_hint= [.2, .2])
                    Layout.add_widget(self.Temp)
                    
                    self.Air=Button( text='Breathing \nRate:', background_normal= u'/home/pi/Área de Trabalho/PatientInfoMod/Buttons/bluBtn.jpg', font_size=36, size_hint= [.2, .2])
                    Layout.add_widget(self.Air)	

                    self.Ox=Button( text='Spo2:', font_size=36, background_normal= u'/home/pi/Área de Trabalho/PatientInfoMod/Buttons/bluBtn.jpg', size_hint= [.2, .2])
                    Layout.add_widget(self.Ox)

                    self.ECG=Button( text='ECG:', font_size=36, background_color= [1, 0, 0, 1], size_hint= [.2, .2])
                    Layout.add_widget(self.ECG)

                    self.BPM=Button( text='BPM:', font_size=36, background_color= [0, .6, 0, 1], size_hint= [.2, .2])
                    Layout.add_widget(self.BPM)

                    self.RTS=Button( text='RTS:', font_size=36, background_normal= u'/home/pi/Área de Trabalho/PatientInfoMod/Buttons/greBtn.jpg', size_hint= [.2, .2])
                    Layout.add_widget(self.RTS)
                    Layout.add_widget(self.GCSbox)
                    
                    Clock.schedule_interval(self.update, 30 / 60.0)
                    return Layout
                                  

                    def on_text(instance, value):
                        print('Typing GCS')
						
                    def on_enter(instance):
                        gcs = self.GCSbox.text
                        print("GCS: " + str(gcs) )		

                    self.GCSbox.bind(text=on_text, on_text_validate=on_enter)

		

                def update(self, dt):
                    global sis, air

##                    start = ser.readline().strip()
##                    start = start.decode('utf-8')
                    start = 'b'
                    if(start == 'b'):
                        print("begin")
                        start = 'a'

                        temp = round(random.uniform(0, 63 ), 2) 
                        ecg  = round(random.uniform(0, 5), 2) 
                        bpm  = random.randint(40, 110)
                        ox   = random.randint(0, 100)
                        air  = random.randint(10,40)
                        sis  = random.randint(40, 160)
                        dia = random.randint(30, 120)

                        if(debug):

                            print(temp)
                            print(ecg)
                            print(ox)
                            print(bpm)

                        try:  
                            temp = float(temp)
                            temp = str(temp)
                            self.Temp.text = str(gcs)
                        except:
                            self.Temp.text = str(gcs)
			
                        try:
                            ecg = float(ecg)
                            ecg = str(ecg)
                            self.ECG.text = ecg
                        except:
                            self.ECG.text = self.ECG.text

                        try:
                            ox = int(ox)
                            ox = str(ox)
                            self.Ox.text = "Spo2: " + ox + "%"
                        except:
                            self.Ox.text = self.Ox.text
			
                        try:
                            bpm = int(bpm)
                            bpm = str(bpm)
                            self.BPM.text = "BPM: " + bpm
                        except:
                            self.BPM.text = self.BPM.text
                    if(start == 'a'):

                            #air = ser.readline().strip()
                            start = 's'
                            print(air)
                            try:
                                    air = int(air)
                                    air = str(air)
                                    self.Air.text = air + "\nbreaths/min"
                            except:
                                    self.Air.text = self.Air.text
		
                    if(start == 's'):
			
                            #sis = ser.readline().strip()
                            start = 'd'
                            print(sis)
                            try:
                                    sis = int(sis)
                                    sis = str(sis)
                                    self.Press.text = sis + '/' + str(dia)
                            except:
                                    self.Press.text = self.Press.text

                    if(start == 'd'):
			
                            #dia = ser.readline().strip()
                            start = 'b'
                            print(dia)
                            try:
                                    dia = int(dia)
                                    dia = str(dia)
                                    self.Press.text = str(sis) + '/' + dia
                            except:
                                    self.Press.text = self.Press.text
                    rts = round(random.uniform(3, 7.84), 2)
                    self.RTS.text = "RTS: " + str(rts)
		
                    if(rts < 10 and rts > 4):
                        self.RTS.background_normal = u'/home/pi/Área de Trabalho/PatientInfoMod/Buttons/yelBtn.jpg'
                    elif(rts < 4):
                        self.RTS.background_normal = u'/home/pi/Área de Trabalho/PatientInfoMod/Buttons/redBtn.jpg'
                    else:
                        self.RTS.background_normal = u'/home/pi/Área de Trabalho/PatientInfoMod/Buttons/greBtn.jpg'
                

PatientInfoApp().run()

			