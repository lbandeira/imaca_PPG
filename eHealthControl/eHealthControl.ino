#include <eHealth.h>
#include <eHealthDisplay.h>


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

#include <PinChangeInt.h>
#include <Time.h>
#include <TimeLib.h>
#include "HX711.h"

HX711 scale(A5, A4);

int cont = 0, eStop = 12;
int air, readAir = 0, airCount = 0;

float calibration_factor = 17310; 
// the setup routine runs once when you press reset:

void setup() {
  Serial.begin(115200);  

  eHealth.initPulsioximeter();
    scale.set_scale();
  scale.tare(); //Reset the scale to 0
  pinMode(12, INPUT);


  //Attach the inttruptions for using the pulsioximeter.   
  PCintPort::attachInterrupt(6, readPulsioximeter, RISING);

}

// the loop routine runs over and over again forever:
void loop() {

    scale.set_scale(calibration_factor); //Adjust to this calibration factor

  if(digitalRead(eStop) == HIGH)
  {
    if(readAir == 0)
    {
      Serial.println('s');
    
      float temperature = eHealth.getTemperature();
      Serial.println(temperature, 4);  
  
    
      float ECG = eHealth.getECG();
      Serial.println(ECG, 2); 
      
      // o oximetro demora de 4 a 6 segundos para estabilizar
      //Serial.print("PRbpm : "); 
      Serial.println(eHealth.getBPM());
  
      //Serial.print("%SPo2 : ");
      Serial.println(eHealth.getOxygenSaturation());
    
      // 1 a 2 segundos para imprimir o peso 
      Serial.println(12); 
      delay(500);

    }
    
  if(readAir == 0)
  {
    Serial.println('a');
    readAir = 1; 

  }

if(readAir && airCount < 50)
{ air = eHealth.getAirFlow();  
  Serial.println(air);
  //eHealth.airFlowWave(air);  
  airCount++;
  
}
else if(airCount == 50)
{
  airCount = 0;
}
if(airCount == 0)
{
  Serial.println('r');
  readAir = 0;
}
  
}
else
{
    Serial.println("eStop Button LOW");
}
}


//Include always this code when using the pulsioximeter sensor
//=========================================================================
void readPulsioximeter(){  

  cont++;

  if (cont == 50) { //Get only of one 50 measures to reduce the latency
    eHealth.readPulsioximeter();  
    cont = 0;
  }
}


  
