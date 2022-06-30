#include <DHT.h>
#include <DHT_U.h>

#define TH 2 // Temp & Hum at Arduino digital pin D2
#define DHTTYPE DHT11
#define FAN_PIN 3

#define FAN '1'
#define DATA '2'
#define IDEAL '3'

//Initial
float temperature_ideal = 25;
float humidity_ideal =  50;
int light_ideal = 500;
int ph_ideal = 7.5;
float soil_ideal = 50;

//Constants
const int pResistor = A3; // Photoresistor at Arduino analog pin A3
const int pH_pin = A2;  // pH at Arduino analog pin A2
const int soil_pin = A1; //connect soil humidity sensor to analog A1

//Variables
unsigned long int avgValue; 
int buf[10],temp,op;

DHT dht = DHT(TH, DHTTYPE);

void setup() {
  pinMode(TH, INPUT);
  pinMode(pResistor, INPUT);
  pinMode(pH_pin, INPUT);
  pinMode(soil_pin, INPUT);
  pinMode(FAN_PIN, OUTPUT);
  Serial.begin(9600);
  Serial.println("Start");
  dht.begin();
}

void loop() {
  
  float temperature = dht.readTemperature();
  float hum = dht.readHumidity();
  
  int photoresistor_value = analogRead(pResistor);
  
  int soil_sensorValue = analogRead(soil_pin);  
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

  op = Serial.read();
  if (op == DATA){
    Serial.println(temperature);
    Serial.println(temperature);
    Serial.println(hum);
    Serial.println(hum);
    Serial.println(photoresistor_value);
    Serial.println(phValue);
    Serial.println(final_soil_value);
  }
  else if (op == FAN){
    while(!Serial.available());
    op = Serial.read();
    if (op == '1'){ // open fan
      digitalWrite(FAN_PIN, LOW);
      Serial.println("1"); // success
    }
    else if (op == '0'){ // close fan
      digitalWrite(FAN_PIN, HIGH);
      Serial.println("1"); // success
    }
    else
      Serial.println("0"); // failure
  }
  else if (op == IDEAL){
    Serial.println("IDEAL");
    while (!Serial.available());
    temperature_ideal = Serial.parseFloat();
    Serial.println(temperature_ideal);
    while (!Serial.available());
    humidity_ideal = Serial.parseFloat();
    Serial.println(humidity_ideal);
    while (!Serial.available());
    soil_ideal = Serial.parseFloat();
    Serial.println(soil_ideal);
    
    while (!Serial.available());
    light_ideal = Serial.parseInt();
    Serial.println(light_ideal);
    while (!Serial.available());
    ph_ideal = Serial.parseInt();
    Serial.println(ph_ideal);
    
  }

  delay(5000);
}