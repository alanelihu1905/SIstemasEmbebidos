import RPi.GPIO as GPIO
import time

LED_PIN = 4  # LED en GPIO4

# Configuración
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED_PIN, GPIO.OUT)

# Duraciones Morse
DOT = 0.2
DASH = DOT * 3
SYMBOL_SPACE = DOT
LETTER_SPACE = DOT * 3
WORD_SPACE = DOT * 7

def led_on(duration):
    GPIO.output(LED_PIN, GPIO.HIGH)
    time.sleep(duration)
    GPIO.output(LED_PIN, GPIO.LOW)
    time.sleep(SYMBOL_SPACE)

def punto(): led_on(DOT)
def raya(): led_on(DASH)

def sos():
    # S = · · ·
    for _ in range(3):
        punto()
    time.sleep(LETTER_SPACE)
    # O = — — —
    for _ in range(3):
        raya()
    time.sleep(LETTER_SPACE)
    # S = · · ·
    for _ in range(3):
        punto()
    time.sleep(WORD_SPACE)

try:
    while True:
        sos()
except KeyboardInterrupt:
    GPIO.cleanup()
    print("Programa finalizado")
# SOS en Morse: · · · — — — · · ·
# LED parpadea en patrón SOS (3 cortos, 3 largos, 3 cortos) repetidamente
# Detén el programa con Ctrl+C
    
