import serial
import struct
import csv
from datetime import datetime

# Configuración
puerto_serial = 'COM9'  # Ajustar si es necesario
baudrate = 115200
nombre_archivo = 'datos_sensor_binario.csv'

# Inicializar conexión
ser = serial.Serial(puerto_serial, baudrate, timeout=1)

print(f"[INFO] Capturando datos en binario desde {puerto_serial}... (Ctrl+C para detener)")

try:
    with open(nombre_archivo, mode='w', newline='') as archivo_csv:
        escritor = csv.writer(archivo_csv, delimiter='\t')

        # Escribir encabezados exactos
        escritor.writerow(['sep=\t'])
        escritor.writerow(['Shimmer_Timestamp', 'Shimmer_EMG_ENV', 'Shimmer_EMG_RAW', 'Shimmer_EMG_REF'])
        escritor.writerow(['hh:mm:ss', 'env', 'raw', 'ref'])

        while True:
            paquete = ser.read(6)  # Leer 6 bytes
            if len(paquete) == 6:
                env, raw, ref = struct.unpack('<HHH', paquete)
                timestamp = datetime.now().strftime('%H:%M:%S')

                # Escribir línea con 4 decimales en los valores
                escritor.writerow([timestamp,
                                   f"{env:.4f}",
                                   f"{raw:.4f}",
                                   f"{ref:.4f}"])

                print(f"[RECEIVED] {timestamp} - ENV={env}, RAW={raw}, REF={ref}")
except KeyboardInterrupt:
    print("\n[STOP] Captura detenida por el usuario.")
    ser.close()
finally:
    if ser.is_open:
        ser.close()