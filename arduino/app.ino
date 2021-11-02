#include <TinyGPS.h>
#include <SoftwareSerial.h>
#include <DHT.h>
#include <DHT_U.h>

TinyGPS gps;
// ss(TX, RX);
SoftwareSerial ss(11, 12);
DHT dht(A1, DHT11);
int CDS = A0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  dht.begin();
  ss.begin(9600);
  pinMode(A0, INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  bool newData = false;
  unsigned long chars;
  unsigned short sentences, failed;
  
  float humi, temp;
  temp = dht.readTemperature();
  humi = dht.readHumidity();
  CDS = analogRead(A0);
  
  for (unsigned long start = millis(); millis() - start < 1000;)
  {
    while (ss.available())
    {
      char c = ss.read();
      // Serial.write(c); // uncomment this line if you want to see the GPS data flowing
      if (gps.encode(c)) // Did a new valid sentence come in?
        newData = true;
    }
  }

  if (newData)
  {
    float flat, flon;
    unsigned long age;
    gps.f_get_position(&flat, &flon, &age);
    Serial.print(flat == TinyGPS::GPS_INVALID_F_ANGLE ? 0.0 : flat, 6);
    Serial.print(",");
    Serial.print(flon == TinyGPS::GPS_INVALID_F_ANGLE ? 0.0 : flon, 6);
    Serial.print(",");
    Serial.print(temp);
    Serial.print(",");
    Serial.print(humi);
    Serial.print(",");
    Serial.println(CDS);
    
    // delay(1000);
    delay(60000);
  }
  
  gps.stats(&chars, &sentences, &failed);
  if (chars == 0)
    Serial.println("** No characters received from GPS: check wiring **");
}