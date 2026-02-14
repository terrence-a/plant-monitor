#include <DHT22.h>

#define pinDATA 5

DHT22 dht22(pinDATA);

void setup() {
  Serial.begin(9600); // 1bit=10µs
  Serial.println("\ntest capteur DTH22");
}

void loop() {

  float t = dht22.getTemperature();
  float h = dht22.getHumidity();
  float moisture0 = analogRead(15);

  if (dht22.getLastError() != dht22.OK) {
    Serial.print("last error :");
    Serial.println(dht22.getLastError());
  }

  
  Serial.print(h, 1);
  Serial.print(",");
  Serial.print(t);
  Serial.print(",");
  Serial.println(moisture0, 1);

  delay(2000);
}
