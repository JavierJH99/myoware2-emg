#include <BluetoothSerial.h>
#include <MyoWare.h>

BluetoothSerial SerialBT;

MyoWare myoware;

void setup() {
  Serial.begin(115200);
  SerialBT.begin("MyoWareBT");

  myoware.setConvertOutput(true);    
  myoware.setGainPotentiometer(50.0);  
  myoware.setENVPin(A3);
  myoware.setRAWPin(A4);
  myoware.setREFPin(A5);

  pinMode(myoware.getStatusLEDPin(), OUTPUT);
}

void loop() {
  uint16_t envValue = (uint16_t)myoware.readSensorOutput(MyoWare::ENVELOPE);
  uint16_t rawValue = (uint16_t)myoware.readSensorOutput(MyoWare::RAW);
  uint16_t refValue = (uint16_t)analogRead(myoware.getREFPin());

  // Enviar en binario puro
  SerialBT.write((uint8_t *)&envValue, sizeof(envValue));
  SerialBT.write((uint8_t *)&rawValue, sizeof(rawValue));
  SerialBT.write((uint8_t *)&refValue, sizeof(refValue));

  // Sin delay para máximo muestreo
}