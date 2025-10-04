import RPi.GPIO as GPIO
import time

LED_PIN = 4       # LED en GPIO4
BUTTON_PIN = 17   # Botón en GPIO17

# Configuración
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Botón a 3.3V

try:
    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.HIGH:   # Botón presionado
            GPIO.output(LED_PIN, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(LED_PIN, GPIO.LOW)
            time.sleep(0.5)
        else:
            GPIO.output(LED_PIN, GPIO.LOW)        # LED apagado si no se presiona
            time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()
    print("Programa finalizado")
# Ley 1Hz con botón: El LED parpadea una vez por segundo (0.5s encendido, 0.5s apagado) solo cuando se presiona el botón
