import serial
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, iirnotch, welch
from datetime import datetime

# Configuración
PUERTO = 'COM9'
BAUDRATE = 115200
NOMBRE_ARCHIVO = 'captura_myo.csv'
FS_ESTIMADO = 1024  # Asumimos 1kHz, lo puedes ajustar luego

# Inicializar conexión
ser = serial.Serial(PUERTO, BAUDRATE, timeout=1)

# Preparar almacenamiento
datos = []
timestamps = []
print("[INFO] Capturando datos... (Ctrl+C para detener)")

try:
    while True:
        linea = ser.readline().decode('utf-8').strip()
        if linea:
            try:
                valor = float(linea)
                datos.append(valor)
                timestamps.append(datetime.now())
                print(f"[{len(datos)}] {valor}")
            except ValueError:
                print(f"[WARN] Valor no numérico: {linea}")
except KeyboardInterrupt:
    print("\n[STOP] Captura detenida por el usuario.")
    ser.close()

# Convertir datos
datos = np.array(datos)
tiempos = np.array([(t - timestamps[0]).total_seconds() for t in timestamps])

# Filtros
def butter_bandpass(lowcut, highcut, fs, order=4):
    nyq = 0.5 * fs
    b, a = butter(order, [lowcut / nyq, highcut / nyq], btype='band')
    return b, a

def apply_notch_filter(data, freq=50.0, fs=1024.0, Q=30.0):
    b, a = iirnotch(freq / (0.5 * fs), Q)
    return filtfilt(b, a, data)

# Aplicar pasabanda
b, a = butter_bandpass(20, 450, FS_ESTIMADO)
datos_filtrados = filtfilt(b, a, datos)

# Aplicar notch 50Hz
datos_notch = apply_notch_filter(datos_filtrados, freq=50, fs=FS_ESTIMADO)

# Guardar CSV
df = pd.DataFrame({
    'Timestamp': timestamps,
    'Tiempo (s)': tiempos,
    'EMG Crudo': datos,
    'EMG Pasabanda': datos_filtrados,
    'EMG Notch': datos_notch
})
df.to_csv(NOMBRE_ARCHIVO, index=False)
print(f"[INFO] Datos guardados en {NOMBRE_ARCHIVO}")

# Función para espectro
def plot_frequency_response(signal, fs, title):
    f, Pxx = welch(signal, fs=fs, nperseg=512)
    plt.semilogy(f, Pxx)
    plt.title(title)
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Potencia (dB)')
    plt.grid(True)

# Graficar
plt.figure(figsize=(16, 12))

plt.subplot(3, 2, 1)
plt.plot(tiempos, datos)
plt.title('EMG Crudo - Tiempo')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')

plt.subplot(3, 2, 2)
plot_frequency_response(datos, FS_ESTIMADO, 'EMG Crudo - Frecuencia')

plt.subplot(3, 2, 3)
plt.plot(tiempos, datos_filtrados)
plt.title('EMG Pasabanda 20-450Hz - Tiempo')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')

plt.subplot(3, 2, 4)
plot_frequency_response(datos_filtrados, FS_ESTIMADO, 'EMG Pasabanda - Frecuencia')

plt.subplot(3, 2, 5)
plt.plot(tiempos, datos_notch)
plt.title('EMG Pasabanda + Notch 50Hz - Tiempo')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')

plt.subplot(3, 2, 6)
plot_frequency_response(datos_notch, FS_ESTIMADO, 'EMG Notch - Frecuencia')

plt.tight_layout()
plt.show()
