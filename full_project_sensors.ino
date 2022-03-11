#include <DHT.h>
#include <DHT_U.h>

#define TH 2 // Temp & Hum at Arduino digital pin D2
#define DHTTYPE DHT11

//Constants
const int pResistor = A3; // Photoresistor at Arduino analog pin A3

const int pH_pin = A2;  // pH at Arduino analog pin A2
//Variables
unsigned long int avgValue; 
int buf[10],temp;

DHT dht = DHT(TH, DHTTYPE);

void setup() {
  pinMode(TH, INPUT);
  pinMode(pResistor, INPUT);
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  
  float temperature = dht.readTemperature();
  float hum = dht.readHumidity();
  
  int photoresistor_value = analogRead(pResistor);
  
  int soil_sensorValue = analogRead(A1);  //connect soil humidity sensor to analog A1
  double final_soil_value = ((1024-soil_sensorValue)/1024.0) * 100;

  float pHVol;
  float phValue;

  //pH calculation
  for(int i=0;i<10;i++) { 
     buf[i]=analogRead(pH_pin);
     delay(10);
  }
  for(int i=0;i<9;i++){
     for(int j=i+1;j<10;j++){
        if(buf[i]>buf[j]){
        temp=buf[i];
        buf[i]=buf[j];
        buf[j]=temp;
        }
     }
  }
  avgValue=0;
  for(int i=2;i<8;i++)
      avgValue+=buf[i];
  pHVol = (float)avgValue*5.0/1024/6;
  phValue = -5.56 * pHVol + 26.89;

  Serial.print("The temperature now is: ");
  Serial.println(temperature);
  Serial.print("The humidity now is: ");
  Serial.println(hum);
  
  Serial.print("Photoresistor value: ");
  Serial.println(photoresistor_value);

  Serial.print("Soil humidity value: ");
  Serial.println(final_soil_value);

  Serial.print("pH = ");
  Serial.println(phValue);
  
  delay(5000);
}
