import RPi.GPIO as GPIO
import time

PIN_SENSOR = 17  # GPIO conectado al pin central del potenciómetro

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def leer_rc(pin):
    """Mide el tiempo de carga del capacitor según la resistencia del potenciómetro."""
    count = 0

    # 1️⃣ Descarga el capacitor
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(0.1)  # Espera a que se descargue

    # 2️⃣ Cambia a modo entrada y mide el tiempo que tarda en cargarse
    GPIO.setup(pin, GPIO.IN)
    while GPIO.input(pin) == GPIO.LOW:
        count += 1
    return count

try:
    while True:
        valor = leer_rc(PIN_SENSOR)
        print(f"Lectura del potenciómetro: {valor}")
        time.sleep(0.5)
except KeyboardInterrupt:
    GPIO.cleanup()
    print("Lectura finalizada")
# Lee el valor del potenciómetro conectado al pin GPIO17
# Imprime el valor medido en la consola cada 0.5 segundos   