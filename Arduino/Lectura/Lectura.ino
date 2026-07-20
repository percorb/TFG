#include <Wire.h>

const byte MPU = 0x68;

// Sensores flexión
const int flexPins[5] = {A3, A2, A0, A1, A6};

void setup() {
  Serial.begin(115200);
  Wire.begin();

  // Despertar MPU6050
  Wire.beginTransmission(MPU);
  Wire.write(0x6B);
  Wire.write(0);
  Wire.endTransmission(true);

  Serial.println("Sistema iniciado");
}

void loop() {

  // ===== FLEX =====
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

  // ===== SALIDA =====

  //Serial.print("F1:");
  Serial.print(flex[0]);
  Serial.print(",");
  //Serial.print("\tF2:");
  Serial.print(flex[1]);
  Serial.print(",");
  //Serial.print("\tF3:");
  Serial.print(flex[2]);
  Serial.print(",");
  //Serial.print("\tF4:");
  Serial.print(flex[3]);
  Serial.print(",");
  //Serial.print("\tF5:");
  int valor = 0;
  if (flex[4]<3000){
    valor = flex[4] + 1260;
  }
  else{
    valor = flex[4] - 20;
  }
  Serial.print(valor);
  Serial.print(",");

  //Serial.print("\tAx:");
  Serial.print(Ax, 2);
  Serial.print(",");

  //Serial.print("\tAy:");
  Serial.print(Ay, 2);
  Serial.print(",");

  //Serial.print("\tAz:");
  Serial.print(Az, 2);
  Serial.print(",");

  //Serial.print("\tGx:");
  Serial.print(Gx, 2);
  Serial.print(",");

  //Serial.print("\tGy:");
  Serial.print(Gy, 2);
  Serial.print(",");

  //Serial.print("\tGz:");
  Serial.println(Gz, 2);

  delay(50);
}