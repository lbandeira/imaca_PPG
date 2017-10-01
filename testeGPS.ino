#include <TimeLib.h>
#include <TinyGPS++.h>
#include <SoftwareSerial.h>

//Pinos utilizados para conexao do modulo GY-NEO6MV2
static const int RXPin = 2, TXPin = 3;

//Objeto TinyGPS++
TinyGPSPlus gps;

//Conexao serial do modulo GPS
SoftwareSerial Serial_GPS(RXPin, TXPin);

float float_latitude, float_longitude;
int32_t lat;
int32_t lon;
uint8_t coords[6]; // 6*8 bits = 48
  
void setup()
{
  //Baud rate Arduino
  Serial.begin(9600);
  //Baud rate Modulo GPS
  Serial_GPS.begin(9600);

}
void loop()
{
  //Serial.println("Loop");
  //Conexao com modulo GPS
  while (Serial_GPS.available() > 0)
    if (gps.encode(Serial_GPS.read())){
      //Serial.println("Displayinfo");
      displayInfo();
    }
  if (millis() > 5000 && gps.charsProcessed() < 10)
  {
    Serial.println(F("No GPS detected: check wiring."));
    while (true);
  }

  delay(1000);
}

void displayInfo()
{
  //Mostra informacoes no Serial Monitor
  //Serial.print(F("L:"));
  if (gps.location.isValid())
  {
    float_latitude = gps.location.lat();
    //Serial.print(gps.location.lat(), 6); //latitude
    //Serial.print(F(","));
    float_longitude = gps.location.lng();
    //Serial.print(gps.location.lng(), 6); //longitude
    //Serial.print(F(" "));
    Codcat();
  }
  else
  {
    Serial.print(F("INVALID "));
  }
  
  
  delay(200);
  //Decodcat();
  //Serial.println();
}


/*FUNCAO DE CODIFICACAO DE COORDENADAS*/
void Codcat(){
  int ordemlong = 1000;
  int ordemlat = 1000;
  if(float_latitude >= 10 || float_latitude <= -10){
    ordemlat = 100;
  }
  if(float_longitude >= 10 || float_longitude <= -10 ){
    ordemlong = 100;
  }
  //Serial.println(ordemlong);
  lat = float_latitude*ordemlat;
  lon = float_longitude*ordemlong;
  
  // Pad 2 int32_t to 6 8uint_t, skipping the last byte (x >> 24)
  coords[0] = lat;
  coords[1] = lat >> 8;
  coords[2] = lat >> 16;
  
  coords[3] = lon;
  coords[4] = lon >> 8;
  coords[5] = lon >> 16;

  
  Serial.print('a');  
  for(int i = 0; i <= 5; i++)
    Serial.print(coords[i]);
  Serial.print('z');  
  
  //LMIC_setTxData2(1, coords, sizeof(coords), 0);
}

/*FUNCAO DE DECODIFICACAO DE COORDENADAS*/
void Decodcat(){
  //Serial.println(coords[0]); 
  //Serial.println(coords[1]); 
  //Serial.println(coords[2]); 
  
  int32_t latd = (coords[0]+(coords[1] << 8)+(coords[2] << 16)) ;

  //Serial.println(coords[3]); 
  //Serial.println(coords[4]); 
  //Serial.println(coords[5]); 
  
  int32_t lond = (coords[3]+(coords[4] << 8)+(coords[5] << 16)); 
  
  //Serial.println(); 
  //Serial.print(latd);
  //Serial.print(F(","));
  //Serial.print(lond);
}






