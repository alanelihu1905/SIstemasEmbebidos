import RPi.GPIO as GPIO
import time

# Configuración
GPIO.setmode(GPIO.BCM)       # Usamos numeración BCM
GPIO.setwarnings(False)
GPIO.setup(4, GPIO.OUT)      # Pin GPIO 4 como salida

# Loop principal
try:
    while True:
        GPIO.output(4, GPIO.HIGH)  # Enciende LED
        time.sleep(1)              # Espera 1 segundo
        GPIO.output(4, GPIO.LOW)   # Apaga LED
        time.sleep(1)              # Espera 1 segundo

except KeyboardInterrupt:
    GPIO.cleanup()   # Limpia configuración al salir con CTRL+C
