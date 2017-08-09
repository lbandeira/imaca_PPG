/*
 *  eHealth sensor platform for Arduino and Raspberry from Cooking-hacks.
 *
 *  Description: "The e-Health Sensor Shield allows Arduino and Raspberry Pi 
 *  users to perform biometric and medical applications by using 9 different 
 *  sensors: Pulse and Oxygen in Blood Sensor (SPO2), Airflow Sensor (Breathing),
 *  Body Temperature, Electrocardiogram Sensor (ECG), Glucometer, Galvanic Skin
 *  Response Sensor (GSR - Sweating), Blood Pressure (Sphygmomanometer) and 
 *  Patient Position (Accelerometer)."  
 *
 *  In this example we use the temperature sensor to measure the 
 *  corporal temperature of the body.
 *
 *  Copyright (C) 2012 Libelium Comunicaciones Distribuidas S.L.
 *  http://www.libelium.com
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 *  Version 0.1
 *  Author: Luis Martin & Ahmad Saad
 */

#include <eHealth.h>
#include <PinChangeInt.h>
#include <Time.h>
#include <TimeLib.h>
#include <TinyGPS++.h>
#include <SoftwareSerial.h>

int cont = 0;
//Pinos utilizados para conexao do modulo GY-NEO6MV2
static const int RXPin = 4, TXPin = 3;

//Objeto TinyGPS++
TinyGPSPlus gps;

//Conexao serial do modulo GPS
SoftwareSerial Serial_GPS(RXPin, TXPin);

//Ajuste o timezone de acordo com a regiao
const int UTC_offset = -3;

// the setup routine runs once when you press reset:
void setup() {
  Serial.begin(115200);  

  eHealth.initPulsioximeter();

  //Attach the inttruptions for using the pulsioximeter.   
  PCintPort::attachInterrupt(6, readPulsioximeter, RISING);
  Serial_GPS.begin(9600);

  //Mostra informacoes iniciais no serial monitor
  Serial.println(F("Data, Hora, Latitude e Longitude"));
  Serial.println(F("Modulo GPS GY-NEO6MV2"));
  Serial.print(F("Biblioteca TinyGPS++ v. ")); 
  Serial.println(TinyGPSPlus::libraryVersion());
  Serial.println();
}

// the loop routine runs over and over again forever:
void loop() {
  float temperature = eHealth.getTemperature();

  Serial.print("Temperature Celsius: ");       
  Serial.print(temperature, 4);  
  Serial.println(""); 

  
  float ECG = eHealth.getECG();

  Serial.print("ECG value :  ");
  Serial.print(ECG, 2); 
  Serial.print(" V"); 
  Serial.println(""); 

  Serial.print("PRbpm : "); 
  Serial.print(eHealth.getBPM());

  Serial.print("    %SPo2 : ");
  Serial.print(eHealth.getOxygenSaturation());

  Serial.print("\n");  
  Serial.println("============================="); 

   //Conexao com modulo GPS
  while (Serial_GPS.available() > 0)
    if (gps.encode(Serial_GPS.read()))
      displayInfo();

  if (millis() > 5000 && gps.charsProcessed() < 10)
  {
    Serial.println(F("No GPS detected: check wiring."));
    while (true);
  }
  delay(500);
}


//Include always this code when using the pulsioximeter sensor
//=========================================================================
void readPulsioximeter(){  

  cont ++;

  if (cont == 50) { //Get only of one 50 measures to reduce the latency
    eHealth.readPulsioximeter();  
    cont = 0;
  }
}

void displayInfo()
{
  //Mostra informacoes no Serial Monitor
  Serial.print(F("Location: "));
  if (gps.location.isValid())
  {
    Serial.print(gps.location.lat(), 6); //latitude
    Serial.print(F(","));
    Serial.print(gps.location.lng(), 6); //longitude
  }
  else
  {
    Serial.print(F("INVALID"));
  }

  Serial.print(F("  Date/Time: "));
  if (gps.date.isValid())
  {
    Serial.print(gps.date.day()); //dia
    Serial.print(F("/"));
    Serial.print(gps.date.month()); //mes
    Serial.print(F("/"));
    Serial.print(gps.date.year()); //ano
  }
  else
  {
    Serial.print(F("INVALID"));
  }

  Serial.print(F(" "));
  if (gps.time.isValid())
  {
    if (gps.time.hour() < 10) Serial.print(F("0"));
    Serial.print(gps.time.hour()-3); //hora
    Serial.print(F(":"));
    if (gps.time.minute() < 10) Serial.print(F("0"));
    Serial.print(gps.time.minute()); //minuto
    Serial.print(F(":"));
    if (gps.time.second() < 10) Serial.print(F("0"));
    Serial.print(gps.time.second()); //segundo
    Serial.print(F("."));
    if (gps.time.centisecond() < 10) Serial.print(F("0"));
    Serial.print(gps.time.centisecond());
  }
  else
  {
    Serial.print(F("INVALID"));
  }
  Serial.println();
}

void GPS_Timezone_Adjust()
{
  while (Serial_GPS.available())
  {
    if (gps.encode(Serial_GPS.read()))
    {
      int Year = gps.date.year();
      byte Month = gps.date.month();
      byte Day = gps.date.day();
      byte Hour = gps.time.hour();
      byte Minute = gps.time.minute();
      byte Second = gps.time.second();
    }
  }
}



