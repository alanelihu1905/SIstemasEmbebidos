import RPi.GPIO as GPIO
import time

# Configuración inicial
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4, GPIO.OUT)  # Pin GPIO4

# Duraciones Morse
DOT = 0.2   # Punto = 0.2 segundos
DASH = 0.6  # Raya = 3 veces el punto
SYMBOL_SPACE = 0.2  # Pausa entre símbolos de una letra
LETTER_SPACE = 0.6  # Pausa entre letras
WORD_SPACE = 1.4    # Pausa entre palabras

def led_on(duration):
    GPIO.output(4, GPIO.HIGH)
    time.sleep(duration)
    GPIO.output(4, GPIO.LOW)
    time.sleep(SYMBOL_SPACE)

def sos():
    # S = · · ·
    for i in range(3):
        led_on(DOT)
    time.sleep(LETTER_SPACE)
    
    # O = — — —
    for i in range(3):
        led_on(DASH)
    time.sleep(LETTER_SPACE)
    
    # S = · · ·
    for i in range(3):
        led_on(DOT)
    time.sleep(WORD_SPACE)

try:
    while True:
        sos()   # Repite continuamente el mensaje SOS

except KeyboardInterrupt:
    GPIO.cleanup()
