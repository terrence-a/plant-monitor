#include <ArduinoWebsockets.h>

#include <WiFi.h>
#include <DHT22.h>

#define dhtpinDATA 32
#define moisture0pin 35

using namespace websockets;

DHT22 dht22(dhtpinDATA);


const char* ssid = "meshAirsonics_4L4D";
const char* password = "fpcdpp8339";
const char* server_host_ip = "10.88.111.13";
const uint16_t server_host_port = 8765;


WebsocketsClient client;

void setup() {
  Serial.begin(9600); // 1bit=10µs

  
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi ..");
  
  // Wait until connected
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("Connected to WiFi Network");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP()); // Print the IP address

  

}

void loop() {
  String report = "";

  float t = dht22.getTemperature();
  float h = dht22.getHumidity();
  float moisture0 = analogRead(dhtpinDATA);

  report += String(t, 2);
  report += ", ";
  report += String(h, 2);
  report += ", ";
  report += String(moisture0, 2);

  if (dht22.getLastError() != dht22.OK) {
    Serial.print("last error :");
    Serial.println(dht22.getLastError());
  }

  Serial.print(WiFi.localIP());
  Serial.print(" ,");
  Serial.println(report);
  

  bool connected = client.connect(server_host_ip, server_host_port, "/");
    if(connected) {
        Serial.println("Connected!");
        client.send(report);
    } else {
        Serial.println("Not Connected!");
    }
    
    // run callback when messages are received
    client.onMessage([&](WebsocketsMessage message){
        Serial.print("Got Message: ");
        Serial.println(message.data());
    });

  delay(2000);
}
