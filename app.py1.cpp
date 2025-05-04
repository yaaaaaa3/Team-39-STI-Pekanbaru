/***************************************************
  This is an example sketch for our optical Fingerprint sensor

  Designed specifically to work with the Adafruit BMP085 Breakout
  ----> http://www.adafruit.com/products/751

  These displays use TTL Serial to communicate, 2 pins are required to
  interface
  Adafruit invests time and resources providing this open source code,
  please support Adafruit and open-source hardware by purchasing
  products from Adafruit!

  Written by Limor Fried/Ladyada for Adafruit Industries.
  BSD license, all text above must be included in any redistribution
 ****************************************************/




//FINGERPRINT 
#include <WiFi.h>
#include <HTTPClient.h>

#include <Adafruit_Fingerprint.h>

const char* ssid = "Redmi"; // ini udah bener?
const char* password = "kukuruyuk "; // atau ini, ga connect2 itu WiFinya, udah benar pak, atau coba pakai hospot hp?iya
const char* UBIDOTS_TOKEN = "BBUS-12k3H1t3siSKFWPyeh0k0jc4mdjmkN"; // Token kamu
const char* device_label = "esp32"; // Ubah jika perlu
const char* variable_label = "jarak"; // Ubah jika perlu

void setup(){
  Serial.begin(9600);
  pinMode(ECHOPIN, INPUT);
  pinMode(TRIGPIN, OUTPUT);
  pinMode(LED1, OUTPUT);
  lcd.backlight(); lcd.init();
  lcd.setCursor(0,0); lcd.print("Connecting");
  lcd.setCursor(0,1); lcd.print("Hello, world!");

  
    WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi connected!");

  
 Serial.println("Scanning for WiFi networks...");
 int n = WiFi.scanNetworks();
  for (int i = 0; i < n; ++i) {
  Serial.println(WiFi.SSID(i));
}


  ESP32PWM::allocateTimer(0);
	ESP32PWM::allocateTimer(1);
	ESP32PWM::allocateTimer(2);
	ESP32PWM::allocateTimer(3);
	myservo.setPeriodHertz(50);    // standard 50 hz servo
	myservo.attach(servoPin, 1000, 2000); 
  myservo.write(90); //nilai derajatnya
  
  
  Serial.println("\n\nAdafruit finger detect test");  // Coba cabut USBnya trus colok lg   ok pak

  // set the data rate for the sensor serial port
  finger.begin(57600);
  delay(5);
  if (finger.verifyPassword()) {
    Serial.println("Found fingerprint sensor!");
  } else {
    Serial.println("Did not find fingerprint sensor :(");
    delay(1000);
  }

  Serial.println(F("Reading sensor parameters"));
  finger.getParameters();
  Serial.print(F("Status: 0x")); Serial.println(finger.status_reg, HEX);
  Serial.print(F("Sys ID: 0x")); Serial.println(finger.system_id, HEX);
  Serial.print(F("Capacity: ")); Serial.println(finger.capacity);
  Serial.print(F("Security level: ")); Serial.println(finger.security_level);
  Serial.print(F("Device address: ")); Serial.println(finger.device_addr, HEX);
  Serial.print(F("Packet len: ")); Serial.println(finger.packet_len);
  Serial.print(F("Baud rate: ")); Serial.println(finger.baud_rate);

  finger.getTemplateCount();

  if (finger.templateCount == 0) {
    Serial.print("Sensor doesn't contain any fingerprint data. Please run the 'enroll' example.");
  }
  else {
    Serial.println("Waiting for valid finger...");
      Serial.print("Sensor contains "); Serial.print(finger.templateCount); Serial.println(" templates");
  }
}

void baca_ultrasonik() {
  digitalWrite(TRIGPIN, LOW);                   
  delayMicroseconds(2);
  digitalWrite(TRIGPIN, HIGH);                  
  delayMicroseconds(10);
  digitalWrite(TRIGPIN, LOW);                   

  timer = pulseIn(ECHOPIN, HIGH);
  jarak = timer/58.0;

  sendToUbidots(jarak);  // ini udah masuk ke ubidotsnya? udah -pak

}

void sendToUbidots(float value) {
  if(WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    String url = "http://industrial.api.ubidots.com/api/v1.6/devices/";
    url += device_label;
    url += "/";
    url += variable_label;

    http.begin(url);
    http.addHeader("Content-Type", "application/json");
    http.addHeader("X-Auth-Token", UBIDOTS_TOKEN);

    String json = "{\"value\": " + String(value, 2) + "}";
    int httpResponseCode = http.POST(json);

    if (httpResponseCode > 0) {
      Serial.print("Data sent. Response code: ");
      Serial.println(httpResponseCode);
    } else {
      Serial.print("Error sending data: ");
      Serial.println(http.errorToString(httpResponseCode).c_str());
    }
    http.end();
  } else {
    Serial.println("WiFi not connected");
  }
}

void loop()  {                   // run over and over again

  getFingerprintID();
  delay(50);            //don't ned to run this at full speed.

  baca_ultrasonik();
  Serial.print("Jarak = ");
  Serial.print(jarak);
  Serial.print(" cm");
  Serial.println();
  
  myservo.write(80); //nilai derajatnya
  lcd.setCursor(0,1); lcd.print("jarak:");
  lcd.print(jarak,1); lcd.print("cm  ");
  pinMode(LED1, HIGH);
  delay(500);
  myservo.write(150); //nilai derajatnya
  pinMode(LED1, LOW);
  delay(1000); 
}

uint8_t getFingerprintID() {
  uint8_t p = finger.getImage();
  switch (p) {
    case FINGERPRINT_OK:
      Serial.println("Image taken");
      break;
    case FINGERPRINT_NOFINGER:
      Serial.println("No finger detected");
      return p;
    case FINGERPRINT_PACKETRECIEVEERR:
      Serial.println("Communication error");
      return p;
    case FINGERPRINT_IMAGEFAIL:
      Serial.println("Imaging error");
      return p;
    default:
      Serial.println("Unknown error");
      return p;
  }

  // OK success!

  p = finger.image2Tz();
  switch (p) {
    case FINGERPRINT_OK:
      Serial.println("Image converted");
      break;
    case FINGERPRINT_IMAGEMESS:
      Serial.println("Image too messy");
      return p;
    case FINGERPRINT_PACKETRECIEVEERR:
      Serial.println("Communication error");
      return p;
    case FINGERPRINT_FEATUREFAIL:
      Serial.println("Could not find fingerprint features");
      return p;
    case FINGERPRINT_INVALIDIMAGE:
      Serial.println("Could not find fingerprint features");
      return p;
    default:
      Serial.println("Unknown error");
      return p;
  }

  // OK converted!
  p = finger.fingerSearch();
  if (p == FINGERPRINT_OK) {
    Serial.println("Found a print match!");
  } else if (p == FINGERPRINT_PACKETRECIEVEERR) {
    Serial.println("Communication error");
    return p;
  } else if (p == FINGERPRINT_NOTFOUND) {
    Serial.println("Did not find a match");
    return p;
  } else {
    Serial.println("Unknown error");
    return p;
  }

  // found a match!
  Serial.print("Found ID #"); Serial.print(finger.fingerID);
  Serial.print(" with confidence of "); Serial.println(finger.confidence);

  return finger.fingerID;
}

// returns -1 if failed, otherwise returns ID #
int getFingerprintIDez() {
  uint8_t p = finger.getImage();
  if (p != FINGERPRINT_OK)  return -1;

  p = finger.image2Tz();
  if (p != FINGERPRINT_OK)  return -1;

  p = finger.fingerFastSearch();
  if (p != FINGERPRINT_OK)  return -1;

  // found a match!
  Serial.print("Found ID #"); Serial.print(finger.fingerID);
  Serial.print(" with confidence of "); Serial.println(finger.confidence);
  return finger.fingerID;
}