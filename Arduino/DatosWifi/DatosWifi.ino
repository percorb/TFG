#include <WiFi.h>
#include <Wire.h>

const char* ssid = "vodafone8309";
const char* password = "6WTCLZZDQVCN3M";

WiFiServer server(5000);
WiFiClient client;

// Sensores de flexión
const int flexPins[5] = {A3, A2, A0, A1, A6};
const byte MPU = 0x68;
void setup() {

  Serial.begin(115200);
  Serial.print("Wifi begin...");
  WiFi.begin(ssid, password);

  Serial.print("Conectando");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi conectado");

  Serial.print("IP: ");
  Serial.println(WiFi.localIP());

  server.begin();
  Wire.begin();


  // Despertar MPU6050
  Wire.beginTransmission(MPU);
  Wire.write(0x6B);
  Wire.write(0);
  Wire.endTransmission(true);

  Serial.println("Sistema iniciado");
}

void loop() {

  if (!client || !client.connected()) {
    client = server.available();
    return;
  }

  /// ===== FLEX =====
  int flex[5];

  for (int i = 0; i < 5; i++) {
    flex[i] = analogRead(flexPins[i]);
  }

  // ===== MPU6050 =====
  Wire.beginTransmission(MPU);
  Wire.write(0x3B);
  Wire.endTransmission(false);

  Wire.requestFrom(MPU, 14, true);

  if (Wire.available() < 14) {
    Serial.println("Error leyendo MPU6050");
    return;
  }

  int16_t AcX = Wire.read() << 8 | Wire.read();
  int16_t AcY = Wire.read() << 8 | Wire.read();
  int16_t AcZ = Wire.read() << 8 | Wire.read();

  // Temperatura (no se usa)
  Wire.read();
  Wire.read();

  int16_t GyX = Wire.read() << 8 | Wire.read();
  int16_t GyY = Wire.read() << 8 | Wire.read();
  int16_t GyZ = Wire.read() << 8 | Wire.read();

  // ===== CONVERSIÓN =====

  // Acelerómetro (±2g)
  float Ax = AcX / 16384.0;
  float Ay = AcY / 16384.0;
  float Az = AcZ / 16384.0;

  // Giroscopio (±250°/s)
  float Gx = GyX / 131.0;
  float Gy = GyY / 131.0;
  float Gz = GyZ / 131.0;

  // ================================================

  String mensaje =
      String(flex[0]) + "," +
      String(flex[1]) + "," +
      String(flex[2]) + "," +
      String(flex[3]) + "," +
      String(flex[4]) + "," +
      String(Ax, 2) + "," +
      String(Ay, 2) + "," +
      String(Az, 2) + "," +
      String(Gx, 2) + "," +
      String(Gy, 2) + "," +
      String(Gz, 2);

  client.println(mensaje);

  delay(50);
}