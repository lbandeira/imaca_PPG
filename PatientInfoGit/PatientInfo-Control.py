import serial
import kivy
from kivy.app import App
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.textinput import TextInput
from kivy.core.window import Window

import random
import time
import pyrebase
import sys
from datetime import datetime
from time import sleep

debug = 1
gcs = temp = ecg = ox = bpm = sis = dia = 0
ser = serial.Serial('COM3', 115200, timeout=0)

fontName = r"C:\Users\Julia\Documents\HPx360\Documents\iMaca\Site\Fontes\Rise\FiraSans-ExtraBold.otf"
class PatientInfoApp(App):
 
    def build(self):

        Layout = StackLayout(padding =  [10, 10, 10, 10], spacing = [15, 10])


        self.Press=Button(font_name = fontName, text='Pressão:', font_size=36, background_down = r"C:\Users\Julia\Desktop\PatientInfoMod\Buttons\redBtn.jpg", background_normal = r"C:\Users\Julia\Desktop\PatientInfoMod\Buttons\redBtn.jpg", size_hint= [.3, .2])
        Layout.add_widget(self.Press)

        self.Temp=Button(font_name = fontName, text='Temp:', font_size=36, background_down = r"C:\Users\Julia\Desktop\PatientInfoMod\Buttons\yelBtn.jpg", background_normal = r"C:\Users\Julia\Desktop\PatientInfoMod\Buttons\yelBtn.jpg", size_hint= [.3, .2])
        Layout.add_widget(self.Temp)

        self.Ox=Button(font_name = fontName, text='Spo2:', font_size=36, background_down = r"C:\Users\Julia\Desktop\PatientInfoMod\Buttons\purBtn.jpg", background_normal = r"C:\Users\Julia\Desktop\PatientInfoMod\Buttons\purBtn.jpg", size_hint= [.3, .2])
        Layout.add_widget(self.Ox)

        self.Air=Button(font_name = fontName, text='Resp:', font_size=36, size_hint_x = None, background_down = r"C:\Users\Julia\Desktop\PatientInfoMod\Buttons\greBtn.jpg", background_normal = r"C:\Users\Julia\Desktop\PatientInfoMod\Buttons\greBtn.jpg", size_hint= [.3, .2])
        Layout.add_widget(self.Air)

        self.ECG=Button(font_name = fontName, text='ECG:', font_size=36, background_color= [1, 0, 0, 1], size_hint= [.3, .2])
        Layout.add_widget(self.ECG)

        self.BPM=Button(font_name = fontName, text='BPM:', font_size=36, background_color= [0, .6, 0, 1], size_hint= [.3, .2])
        Layout.add_widget(self.BPM)

        GCSmsg = "Digite o valor do GCS"
        self.GCSbox = TextInput(hint_text=GCSmsg, multiline=False, size_hint_y=None, height=30, size_hint_x=None, width = 313)
        Layout.add_widget(self.GCSbox)

        def on_text(instance, value):
        	print('texting...')
        	        	
        def on_enter(instance):
        	gcs = self.GCSbox.text
        	print(gcs)
        def on_focus(instance, value):
        	self.GCSbox.text = '\n'

        self.GCSbox.bind(text=on_text, focus = on_focus, on_text_validate=on_enter)

        Clock.schedule_interval(self.update, 30 / 60.0)
        return Layout

    def update(self, dt):

    	start = ser.readline().strip()
    	start = start.decode('utf-8')
    	if(start == 'b'):
    		print("begin")

    		temp = ser.readline().strip()
    		ecg  = ser.readline().strip()
    		ox   = ser.readline().strip()
    		bpm  = ser.readline().strip()

    		if(debug):

	    		print(temp)
	    		print(ecg)
	    		print(ox)
	    		print(bpm)

	    	try:
	    		temp = float(temp)
	    		temp = str(temp)
	    		self.Temp.text = temp[:-2] + "°C"
	    	except:
	    		self.Temp.text = self.Temp.text
	    	
	    	try:
	    		ecg = float(ecg)
	    		ecg = str(ecg)
	    		self.ECG.text = ecg
	    	except:
	    		self.ECG.text = self.ECG.text

	    	try:
	    		ox = int(ox)
	    		ox = str(ox)
	    		self.Ox.text = ox + "%"
	    	except:
	    		self.Ox.text = self.Ox.text
    		
    		try:
    			bpm = int(bpm)
    			bpm = str(bpm)
    			self.BPM.text = "BPM: " + bpm
    		except:
    			self.BPM.text = self.BPM.text
    	if(start == 'a'):

    		air = ser.readline().strip()
    		print(air)
    		try:
    			air = int(air)
    			air = str(air)
    			self.Air.text = "Respiratory rate: " + air + "/min"
    		except:
    			self.Air.text = self.Air.text
    	
    	if(start == 's'):
    		
    		sis = ser.readline().strip()
    		print(sis)
    		try:
    			sis = int(sis)
    			sis = str(sis)
    			self.Press.text = sis + '/' + str(dia)
    		except:
    			self.Press.text = self.Press.text

    	if(start == 'd'):
    		
    		dia = ser.readline().strip()
    		print(dia)
    		try:
    			dia = int(dia)
    			dia = str(dia)
    			self.Press.text = str(sis) + '/' + dia
    		except:
    			self.Press.text = self.Press.text

#Window.fullscreen = True	
PatientInfoApp().run()