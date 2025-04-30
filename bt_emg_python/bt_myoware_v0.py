import serial
import csv
from datetime import datetime

# Configuración
puerto_serial = 'COM9'  # Cambia esto si tu COM es otro
baudrate = 115200
nombre_archivo = 'datos_sensor.csv'

try:
    print(f"[INFO] Intentando abrir el puerto {puerto_serial}...")
    with serial.Serial(puerto_serial, baudrate, timeout=1) as ser:
        print(f"[OK] Puerto {puerto_serial} abierto.")
        print("[INFO] Esperando datos del sensor...")

        with open(nombre_archivo, mode='w', newline='') as archivo_csv:
            escritor = csv.writer(archivo_csv, delimiter='\t')

            # Encabezado CSV
            escritor.writerow(['sep=\t'])
            escritor.writerow(['Shimmer_Timestamp', 'Shimmer_EMG_ENV', 'Shimmer_EMG_RAW', 'Shimmer_EMG_REF'])
            escritor.writerow(['hh:mm:ss', 'env', 'raw', 'ref'])

            while True:
                linea = ser.readline().decode('utf-8', errors='ignore').strip()
                
                if linea:
                    print(f"[RECEIVED] Línea cruda: {linea}")

                if linea.startswith("ENV:"):
                    try:
                        partes = linea.split()
                        env = partes[1]
                        raw = partes[3]
                        ref = partes[5]
                        timestamp = datetime.now().strftime('%H:%M:%S')

                        print(f"[PARSED] ENV={env}, RAW={raw}, REF={ref}")

                        escritor.writerow([timestamp, env, raw, ref])
                        print(f"[SAVED] {timestamp}\t{env}\t{raw}\t{ref}")
                    except Exception as e:
                        print(f"[ERROR] Error al procesar línea: '{linea}' → {e}")
except serial.SerialException as e:
    print(f"[FAIL] No se pudo abrir el puerto {puerto_serial}: {e}")
except KeyboardInterrupt:
    print("\n[STOP] Captura detenida por el usuario.")