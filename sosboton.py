import RPi.GPIO as GPIO
import time

# Configuración
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

LED_PIN = 4
BUTTON_PIN = 17

GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Duraciones Morse
DOT = 0.2   # punto
DASH = 0.6  # raya
SYMBOL_SPACE = 0.2
LETTER_SPACE = 0.6
WORD_SPACE = 1.4

def led_on(duration):
    """Enciende el LED y verifica si se soltó el botón."""
    start_time = time.time()
    while time.time() - start_time < duration:
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            GPIO.output(LED_PIN, GPIO.LOW)
            return False
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(0.01)
    GPIO.output(LED_PIN, GPIO.LOW)
    time.sleep(SYMBOL_SPACE)
    return True

def sos():
    # S = · · ·
    for _ in range(3):
        if not led_on(DOT): return False
    time.sleep(LETTER_SPACE)

    # O = — — —
    for _ in range(3):
        if not led_on(DASH): return False
    time.sleep(LETTER_SPACE)

    # S = · · ·
    for _ in range(3):
        if not led_on(DOT): return False
    time.sleep(WORD_SPACE)

    return True

try:
    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.HIGH:
            if not sos():  # ejecuta SOS pero interrumpe si sueltas
                continue
        else:
            GPIO.output(LED_PIN, GPIO.LOW)

except KeyboardInterrupt:
    GPIO.cleanup()
