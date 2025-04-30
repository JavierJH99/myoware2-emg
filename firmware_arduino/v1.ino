#include <BluetoothSerial.h>   // Bluetooth clásico
#include <MyoWare.h>           // Librería oficial MyoWare

BluetoothSerial SerialBT;     // Objeto para Bluetooth Serial

// Configuración de la señal que quieres leer
MyoWare::OutputType outputType = MyoWare::ENVELOPE; // o MyoWare::RAW

MyoWare myoware;              // Instancia de MyoWare

void setup() {
  Serial.begin(115200);       // Serial por cable USB (solo debug opcional)
  SerialBT.begin("MyoWareBT"); // Nombre visible del Bluetooth para emparejar
  
  myoware.setConvertOutput(false); // Si quieres en mV, pon true
  myoware.setGainPotentiometer(50.0); // Ajusta según tu potenciómetro
  myoware.setENVPin(A3);
  myoware.setRAWPin(A4);
  myoware.setREFPin(A5);

  pinMode(myoware.getStatusLEDPin(), OUTPUT); // LED de estado
}

void loop() {
  int value = myoware.readSensorOutput(outputType);
  
  // Enviar dato por Bluetooth serial
  SerialBT.println(value);

  // (opcional) también por USB para debug
  Serial.println(value);

  // delayMicroseconds(1000); // 1kHz de frecuencia aprox
}