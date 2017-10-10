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
int point = 1;

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
  if(point)
    Serial.print('.');
    
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
  
  point = 0;
  
  //Decodcat(); //Para testar a codificacao
  //Serial.println();
}


/***************************FUNCAO DE CODIFICACAO DE COORDENADAS******************************
* float_latitude, float_latitude => Latitude e Longitude originais, recebidas pelo GPS       *
*                                                                                            *
* Funcionamento da Codificação:                                                              *
* 1) Multiplica o numero float por 100, para que seja salvo as casas decimais                *
* 2) Colocará a nova parte inteira no vetor coords[0-2] (Latitude) e coords[3-5] (Longitude) *
* 3) Após isso, será enviado o número codificado via serial, o qual o inicio do envio está   *
*    indicado com o char 'a' e o fim com o char 'z'.                                         *
*                                                                                            *
*********************************************************************************************/

void Codcat(){
  int ordemlong = 100;
  int ordemlat = 100;
  
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






