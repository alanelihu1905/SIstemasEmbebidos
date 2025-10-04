import RPi.GPIO as GPIO
import time

LED_PIN = 4  # GPIO4

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED_PIN, GPIO.OUT)

try:
    while True:
        GPIO.output(LED_PIN, GPIO.HIGH)  # Enciende el LED
        time.sleep(0.5)
        GPIO.output(LED_PIN, GPIO.LOW)   # Apaga el LED
        time.sleep(0.5)
except KeyboardInterrupt:
    GPIO.cleanup()
    print("Programa finalizado")
# Ley 1Hz: El LED parpadea una vez por segundo (0.5s encendido, 0.5s apagado)