import serial
import serial.tools.list_ports
import sounddevice as sd
import numpy as np
import time

# --- CONFIGURAÇÃO ---
GANHO = 120  # Ajuste conforme a altura da sua voz/música

# Auto-detecção da porta no Mac
ports = list(serial.tools.list_ports.comports())
arduino_port = ""
for p in ports:
    if "usbmodem" in p.device or "usbserial" in p.device:
        arduino_port = p.device
        break

if not arduino_port:
    print("❌ Arduino não encontrado! Verifique o cabo.")
    exit()

try:
    # IMPORTANTE: 115200 para bater com o código do Arduino
    arduino = serial.Serial(arduino_port, 115200, timeout=0.01)
    time.sleep(2)
    print(f"✅ Conectado em: {arduino_port} a 115200 baud")
except Exception as e:
    print(f"❌ Erro: {e}")
    exit()

def audio_callback(indata, frames, time_info, status):
    # Calcula volume RMS para suavidade
    volume_norm = np.sqrt(np.mean(indata**2)) * GANHO
    level = int(np.clip(volume_norm, 0, 5))
    try:
        arduino.write(str(level).encode())
    except:
        pass

# Inicia a escuta do microfone
with sd.InputStream(callback=audio_callback):
    print("\n🎤 MUNDO DA LUA TURBO ATIVO!")
    print("Efeito Fade/Rastro habilitado.")
    print("Pressione Ctrl+C para parar.")
    try:
        while True:
            time.sleep(0.01)
    except KeyboardInterrupt:
        print("\nDesligando...")
        arduino.close()
