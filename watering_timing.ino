#define LED_PIN 5 

int init_hour, init_min;

void convert_millis(int* hrs, int* mins){
  unsigned long mil = millis();
  *hrs = (mil / (60*60000) ) % 24;
  *mins = (mil % (60*60000) ) / 60000;
}

void time_now(int* hrs_now, int* mins_now){
  int hrs, mins;
  
  convert_millis(&hrs, &mins);
  *hrs_now  = init_hour + hrs;
  *mins_now = init_min + mins;
  if(*mins_now >= 60){
    *hrs_now += 1;
    *mins_now -= 60;
  }
  if(*hrs_now >= 24){
    *hrs_now -= 24;
  }
}

void setup() {
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(9600);
  //communicate with Gateway to receive init_hour, init_minute
  init_hour = 23;
  init_min  = 59;
}

void loop() {
  int hour_now, minute_now;
  
  time_now(&hour_now, &minute_now);
  
  if(hour_now == 21 && minute_now >= 58 && minute_now <= 59)
    digitalWrite(LED_PIN, HIGH);
  else
    digitalWrite(LED_PIN, LOW);
  
  Serial.print(hour_now);
  Serial.print(":");
  Serial.println(minute_now);
  
  delay(1000);
}
