#include <DHT.h>
#include <DHT_U.h>

#define DATA 2
#define LED1 5
#define DHTTYPE DHT11

DHT dht = DHT(DATA, DHTTYPE);

void setup() {
  pinMode(DATA, INPUT);
  Serial.begin(9600);
  pinMode(LED1, OUTPUT);
  dht.begin();
}

void loop() {
  float temp = dht.readTemperature();
  float hum = dht.readHumidity();

  if (temp>26.5) {
    digitalWrite(LED1, HIGH);
  }
  else {
    digitalWrite(LED1, LOW);
  }
  Serial.print("T: ");
  Serial.print(temp);
  Serial.print(", H: ");
  Serial.println(hum);
  delay(2000);
}
