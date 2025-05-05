#define BLYNK_TEMPLATE_ID "TMPL6nhshCDLx"
#define BLYNK_TEMPLATE_NAME "SmartSecurity"
#define BLYNK_AUTH_TOKEN "YxJHvHFR3_xHeUL6O7SUezbR-N88IjDm"

#include <WiFi.h>
#include <HTTPClient.h>
#include <ESP32Servo.h>
#include <Adafruit_Fingerprint.h>
#include <LiquidCrystal_I2C.h>
#include <BlynkSimpleEsp32.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);
HardwareSerial serialPort(2);  // use UART2
Adafruit_Fingerprint finger = Adafruit_Fingerprint(&serialPort);
Servo myservo;

#define servoPin 23
#define LED1 26

float berat = 0.0;

const char* ssid = "Redmi";
const char* password = "kukuruyuk";
const char* device_label = "esp32";
const char* variable_label = "berat";

unsigned long previousBlynkMillis = 0;
const unsigned long blynkInterval = 3000;  // 3 detik
bool status = false;

double probsA = 0.0;
double probsB = 0.0;

String userIn;


float userA[] = { 46.1, 46.2, 46.3, 46.4, 46.5, 46.6, 46.7, 46.8, 46.9, 47.0,
                  47.1, 47.2, 47.3, 47.4, 47.5, 47.6, 47.7, 47.8, 47.9, 48.0 };
float userB[] = { 48.5, 48.6, 48.7, 48.8, 48.9, 49.0, 49.1, 49.2, 49.3, 49.4,
                  49.5, 49.6, 49.7, 49.8, 49.9, 50.0, 50.1, 50.2, 50.3, 50.4 };

// Fungsi ReLU (Rectified Linear Unit)
float relu(float x) {
  return x > 0 ? x : 0;
}

// Fungsi Sigmoid
float sigmoid(float x) {
  return 1.0 / (1.0 + exp(-x));
}

float classifyWeightML(float berat) {
  float x = (berat - 45.0) / 5.0;

  float hiddenWeights[4] = { -0.2615, 6.9337, 0.4836, 3.4599 };
  float hiddenBias[4] = { -0.7536, -2.0520, -0.9682, -1.5131 };

  float outputWeights[4] = { 0.2108, 4.6391, -0.9993, 0.3944 };
  float outputBias = -9.9034;

  float hiddenOutput[4];
  for (int i = 0; i < 4; i++) {
    hiddenOutput[i] = relu(x * hiddenWeights[i] + hiddenBias[i]);
  }

  float sum = outputBias;
  for (int i = 0; i < 4; i++) {
    sum += hiddenOutput[i] * outputWeights[i];
  }

  float y = sigmoid(sum);
  probsA = 1.0 - y;
  probsB = y;
  return y > 0.5 ? 1 : 0;  // 1 = User B, 0 = User A
}

void setup() {
  Serial.begin(9600);
  pinMode(LED1, OUTPUT);
  digitalWrite(LED1, HIGH);
  delay(200);
  digitalWrite(LED1, LOW);
  delay(200);
  lcd.backlight();
  lcd.init();
  lcd.setCursor(0, 0);
  lcd.print("Connecting To... ");
  lcd.setCursor(0, 1);
  lcd.print("Pressure Plate");

  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi connected!");

  Blynk.begin(BLYNK_AUTH_TOKEN, ssid, password);

  ESP32PWM::allocateTimer(0);
  ESP32PWM::allocateTimer(1);
  ESP32PWM::allocateTimer(2);
  ESP32PWM::allocateTimer(3);
  myservo.setPeriodHertz(50);
  myservo.attach(servoPin, 1000, 2000);
  myservo.write(90);

  serialPort.begin(57600, SERIAL_8N1, 16, 17);
  finger.begin(57600);
  delay(5);
  if (finger.verifyPassword()) {
    Serial.println("Found fingerprint sensor!");
  } else {
    Serial.println("Did not find fingerprint sensor :(");
    delay(1000);
  }

  finger.getParameters();
  finger.getTemplateCount();

  if (finger.templateCount == 0) {
    Serial.println("Sensor doesn't contain any fingerprint data.");
  } else {
    Serial.println("Waiting for valid finger...");
  }

  lcd.clear();
}

void sendToUbidots(float value) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    String url = "http://industrial.api.ubidots.com/api/v1.6/devices/";
    url += device_label;
    url += "/";
    url += variable_label;

    http.begin(url);
    http.addHeader("Content-Type", "application/json");

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

void loop() {
  Blynk.run();

  if (Serial.available() > 0) {
    String input = Serial.readString();
    berat = input.toFloat();
  }

  // Fingerprint check
  int fingerID = getFingerprintID();
  Serial.println("Waiting...");

  //Klasifikasi dengan ANN
  if (berat > 0.0) {
    classifyWeightML(berat);  // Hitung probsA dan probsB SEKALI saja

    if (fingerID != -1) {
      status = true;

      if (probsB > 0.5) {
        userIn = "User B";
        Serial.println("User B");
      } else {
        userIn = "User A";
        Serial.println("User A");
      }

      Serial.print("Probability: User A: ");
      Serial.println(probsA);
      Serial.print("Probability: User B: ");
      Serial.println(probsB);

    } else {
      status = false;
      userIn = "-";
    }
  }


  if (status) {
    Blynk.virtualWrite(V1, "Welcome Home!");
    Blynk.virtualWrite(V0, berat);
    Blynk.virtualWrite(V2, userIn);

    if (probsA > probsB) {
      Blynk.virtualWrite(V3, probsA);
    } else {
      Blynk.virtualWrite(V3, probsB);
    }

    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("WELCOME HOME     ");
    lcd.setCursor(0, 1);
    lcd.print("Berat: ");
    lcd.print(berat, 1);
    lcd.print(" kg  ");

    digitalWrite(LED1, HIGH);
    myservo.write(160);
    Serial.print("Welcome Home! ID: ");
    Serial.println(fingerID);

    delay(6000);
    userIn = "-";
    probsA = 0.0;
    probsB = 0.0;
    berat = 0.0;
    status = false;
    lcd.clear();
  }

  lcd.setCursor(0, 0);
  lcd.print("- TEAM 39 HOME -");

  myservo.write(15);
  digitalWrite(LED1, LOW);

  unsigned long currentMillis = millis();
  if (currentMillis - previousBlynkMillis >= blynkInterval) {
    previousBlynkMillis = currentMillis;
    Blynk.virtualWrite(V0, berat);
    Blynk.virtualWrite(V1, "Waiting...");
    Blynk.virtualWrite(V2, "No User");
    Blynk.virtualWrite(V3, 0.0);
  }

  delay(500);
}

int getFingerprintID() {
  uint8_t p = finger.getImage();
  if (p != FINGERPRINT_OK) return -1;

  p = finger.image2Tz();
  if (p != FINGERPRINT_OK) return -1;

  p = finger.fingerSearch();
  if (p != FINGERPRINT_OK) return -1;

  Serial.print("Found ID #");
  Serial.print(finger.fingerID);
  Serial.print(" with confidence of ");
  Serial.println(finger.confidence);

  return finger.fingerID;
}