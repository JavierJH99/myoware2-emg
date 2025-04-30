#include <BluetoothSerial.h>   // Bluetooth clásico
#include <MyoWare.h>           // Librería oficial MyoWare

BluetoothSerial SerialBT;      // Instancia Bluetooth Serial

MyoWare myoware;               // Instancia de MyoWare

void setup() {
  Serial.begin(115200);         // Serial USB (opcional para debug)
  SerialBT.begin("MyoWareBT");  // Nombre Bluetooth visible para emparejar

  // Configuración de MyoWare
  myoware.setConvertOutput(false);      // false = salida en ADC puro; true = salida en mV
  myoware.setGainPotentiometer(50.0);    // Ajusta a tu potenciómetro real
  myoware.setENVPin(A3);
  myoware.setRAWPin(A4);
  myoware.setREFPin(A5);

  pinMode(myoware.getStatusLEDPin(), OUTPUT); // LED de estado
}

void loop() {
  // Leer usando la función readSensorOutput con el tipo que quieras
  double envValue = myoware.readSensorOutput(MyoWare::ENVELOPE);
  double rawValue = myoware.readSensorOutput(MyoWare::RAW);
  double refValue = analogRead(myoware.getREFPin());  // REF es lectura directa de ADC, no calibrada

  // Formatear salida como "ENV: x RAW: y REF: z"
  String output = "ENV: " + String(envValue, 4) +  // 4 decimales
                  " RAW: " + String(rawValue, 4) +
                  " REF: " + String(refValue, 0);   // REF es un int

  SerialBT.println(output);    // Enviar por Bluetooth
  Serial.println(output);      // (opcional) también por USB para debug

  // delayMicroseconds(1000);     // 1kHz de muestreo aproximado
}