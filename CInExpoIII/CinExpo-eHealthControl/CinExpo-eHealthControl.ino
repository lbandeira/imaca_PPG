#include <eHealth.h>
#include <eHealthDisplay.h>
#include <PinChangeInt.h>
#include <Time.h>
#include <TimeLib.h>
#include "HX711.h"
#include <SoftwareSerial.h>


HX711 scale(A5, A4);
SoftwareSerial bpSerial(7, 9); // RX, TX
char buffy[15], ch;


int i = 1, cont = 0, eStop = 12;
int air, readWeight = 0;

float calibration_factor = 17310;
// the setup routine runs once when you press reset:

void setup() {
  Serial.begin(115200);
  bpSerial.begin(9600);

  eHealth.initPulsioximeter();

  scale.set_scale();
  scale.tare(); //Reset the scale to 0
  scale.set_scale(calibration_factor); //Adjust to this calibration factor

  pinMode(eStop, INPUT);

  //Attach the inttruptions for using the pulsioximeter.
  PCintPort::attachInterrupt(6, readPulsioximeter, RISING);

}

void getBloodPressure() {
  char buffy[15], ch;

  // send data only when you receive data:
  while (bpSerial.available() > 0) {
    ch = bpSerial.read();
    if (ch == 0x0A)
    {
      Serial.println('s');
      Serial.println(sis);

      Serial.println('d');
      Serial.println(dis);
      i = 1;
    }

    else
    {
      buffy[i] = ch;
      Serial.print("i: "); Serial.print(i); Serial.print(" fetched: ");
      Serial.println(buffy[i]);
      
      if(i == 2 || i == 3 || i == 4)
      {        
        sis = sis * 10 + (buffy[i] - '0');
      }
      
      if(i == 7 || i == 8 || i == 9)
      {
        dis = dis * 10 + (buffy[i] - '0');
      }
       i++;
    }
  }
  return;
}

void getRespRate() {
  unsigned long ElapsedTime = 0;
  int air, peak = 0, pCount = 0, lock = 1;
  unsigned long StartTime = millis(), CurrentTime;

  while (ElapsedTime <= 5000)
  {
    air = eHealth.getAirFlow();

    if (air > peak)
    {
      peak = air;
      lock = 1;
    }
    if (air == 0 && lock && peak > 20 )
    {
      pCount++;
      peak = 0;
      lock = 0;
    }
    //    Serial.print("    air = ");
    //    Serial.println(air);
    //
    //    Serial.print("peaks = ");
    //    Serial.println(pCount);

    CurrentTime = millis();
    ElapsedTime = CurrentTime - StartTime;
  }
  Serial.println('a');
  Serial.println( pCount * 6);
}

void loop() {

  while (digitalRead(eStop) == HIGH)  {
    getBloodPressure();

    while ((bpSerial.available() <= 0)) {
      Serial.println('b');

      float temperature = eHealth.getTemperature();
      //    Serial.print("temp: ");
      Serial.println(temperature, 4);

      float ECG = eHealth.getECG();
      //    Serial.print("ecg: ");
      Serial.println(ECG, 2);

      // o oximetro demora de 4 a 6 segundos para estabilizar
      //    Serial.print("bpm: ");
      Serial.println(eHealth.getBPM());
      //    Serial.print("spo2: ");

      Serial.println(eHealth.getOxygenSaturation());

      //    if (readWeight == 0) {
      //      //      Serial.println('p');
      //      Serial.print("peso: ");
      //
      //      Serial.println(scale.get_value(5));
      //      scale.power_down();
      //      readWeight = 1;
      //    }

      getRespRate();
      delay(800);
    }
  }
}

//Include always this code when using the pulsioximeter sensor
//=========================================================================
void readPulsioximeter() {

  cont++;

  if (cont == 50) { //Get only of one 50 measures to reduce the latency
    eHealth.readPulsioximeter();
    cont = 0;
  }
}

  

