#include <eHealth.h>
#include <eHealthDisplay.h>
#include <PinChangeInt.h>
#include <Time.h>
#include <TimeLib.h>
#include "HX711.h"
#include <SoftwareSerial.h>


HX711 scale(A5, A4);
SoftwareSerial bpSerial(8, 9); // RX, TX
char buffy[15], ch;


int i = 1, cont = 0, eStop = 12;
int air, readAir = 0, airCount = 0, readWeight = 0;

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
  unsigned char sis, dis, pul;

  while (bpSerial.available() > 0) {
    ch = bpSerial.read();
    if (ch == 0x0A)
    {
      sis = ((buffy[2] - '0') * 100) + ((buffy[3] - '0') * 10) + (buffy[4] - '0');
      dis = ((buffy[7] - '0') * 100) + ((buffy[8] - '0') * 10) + (buffy[9] - '0');
      pul = ((buffy[12] - '0') * 100) + ((buffy[13] - '0') * 10) + (buffy[14] - '0');

      Serial.println('s');
      Serial.println(sis);

      Serial.println('d');
      Serial.println(dis);
      i = 1;
    }

    else
    {
      buffy[i] = ch;
      i++;
    }
  }
  return;
}

int getRespRate() {
  unsigned long ElapsedTime = 0;
  int air, peak = 0, pCount = 0, lock = 1;
  unsigned long StartTime = millis(), CurrentTime;

  while (ElapsedTime <= 10000)
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

  return pCount * 6;
}

void loop() {

  while (digitalRead(eStop) == HIGH)  {
    getBloodPressure();

    Serial.println('b');

    float temperature = eHealth.getTemperature();
    Serial.print("temp: ");
    Serial.println(temperature, 4);

    float ECG = eHealth.getECG();
    Serial.print("ecg: ");
    Serial.println(ECG, 2);

    // o oximetro demora de 4 a 6 segundos para estabilizar
    Serial.print("bpm: ");
    Serial.println(eHealth.getBPM());
    Serial.print("spo2: ");

    Serial.println(eHealth.getOxygenSaturation());

    // 1 a 2 segundos para imprimir o peso
    if (readWeight == 0) {
      //      Serial.println('p');
      Serial.print("peso: ");

      Serial.println(scale.get_value(5));
      scale.power_down();
      readWeight = 1;
    }

    Serial.println('a');
    Serial.println(getRespRate());
    delay(490);

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



