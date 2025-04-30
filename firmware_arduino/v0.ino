#include <BluetoothSerial.h>

// Instancia de BluetoothSerial
BluetoothSerial SerialBT;

void setup() {
  Serial.begin(115200);
  SerialBT.begin("MyoWare_EMG_Javier"); // Nombre del dispositivo Bluetooth
  Serial.println("El dispositivo Bluetooth está listo para emparejarse");

  // Configuración de los pines del sensor
  pinMode(34, INPUT); // ENV
  pinMode(35, INPUT); // RAW
  pinMode(32, INPUT); // REF
}

void loop() {
  // Leer datos del sensor EMG
  int envValue = analogRead(34); // Pin A3 en el ejemplo original
  int rawValue = analogRead(35); // Pin A4 en el ejemplo original
  int refValue = analogRead(32); // Pin A5 en el ejemplo original

  // Imprimir valores en el Monitor Serial
  //Serial.println("ENV: " + String(envValue) + " RAW: " + String(rawValue) + " REF: " + String(refValue));
  
  // Crear una cadena con los valores leídos
  String emgData = "ENV: " + String(envValue) + " RAW: " + String(rawValue) + " REF: " + String(refValue);
  
  // Pinta datos en la consola
  SerialBT.println(emgData);
  // delay(); // Ajusta el retraso según sea necesario
}
