#include <ESP8266WiFi.h>
#include <ArduinoJson.h>
#include <Wire.h>
#include <ESP8266WebServer.h>


#include <Adafruit_BMP085.h>
#include "DHT.h"

Adafruit_BMP085 bmp;

#define DHTPIN 12  
#define DHTTYPE DHT11 

DHT dht(DHTPIN, DHTTYPE);



//https://arduinojson.org/v5/doc/encoding/

const int capacity = JSON_OBJECT_SIZE(4);
StaticJsonBuffer<capacity> jb;

JsonObject& obj = jb.createObject(); //create json object

const char* ssid = "your_wifi_name";
const char* password = "your_wifi_password";



ESP8266WebServer server(80);

void setup() {
  

WiFi.begin(ssid, password);

  int i =0;
 while (WiFi.status() != WL_CONNECTED) { // Wait for the Wi-Fi to connect
    delay(1000);
    Serial.print(++i); Serial.print(' ');
  }

  Serial.println('\n');
  Serial.println("Connection established!");  
  Serial.print("IP address:\t");
  Serial.println(WiFi.localIP());         // Send the IP address of the ESP8266 to the computer

Wire.begin(5,4);
Serial.begin(9600);
delay(10);

 if (!bmp.begin()) {

  Serial.println("Could not find a valid BMP sensor, check wiring!");

  

  }

  dht.begin();


server.on("/weather", HTTP_GET, handleWea);
server.begin();

}

void loop() {
  // put your main code here, to run repeatedly:
 
  obj["BMP_Temperature"] = bmp.readTemperature();
  obj["BMP_Pressure"] = bmp.readPressure();
  obj["DHT_Temperature"] = dht.readTemperature();
  obj["DHT_Humidity"] = dht.readHumidity();
  
  server.handleClient();
  obj.printTo(Serial);
  Serial.println("");

  delay(2000);
}

void handleWea(){
 String output;
 obj.printTo(output);
  server.send(200, "text/plain", output);
  }

  
