import RPi.GPIO as GPIO
import time

LED_PIN = 4       # LED en GPIO4
BUTTON_PIN = 17   # Botón en GPIO17 (conectado a 3.3V)

# Configuración
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Botón con pull-down

# Duraciones Morse
DOT = 0.2
DASH = DOT * 3
SYMBOL_SPACE = DOT
LETTER_SPACE = DOT * 3
WORD_SPACE = DOT * 7

def led_on(duration):
    """Enciende el LED durante 'duration' segundos, se corta si se suelta el botón."""
    start = time.time()
    while time.time() - start < duration:
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:  # Botón suelto → salir
            GPIO.output(LED_PIN, GPIO.LOW)
            return False
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(0.01)
    GPIO.output(LED_PIN, GPIO.LOW)
    time.sleep(SYMBOL_SPACE)
    return True

def punto(): return led_on(DOT)
def raya(): return led_on(DASH)

def sos():
    # S = · · ·
    for _ in range(3):
        if not punto(): return False
    time.sleep(LETTER_SPACE)
    # O = — — —
    for _ in range(3):
        if not raya(): return False
    time.sleep(LETTER_SPACE)
    # S = · · ·
    for _ in range(3):
        if not punto(): return False
    time.sleep(WORD_SPACE)
    return True

try:
    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.HIGH:  # Botón presionado
            sos()
        else:
            GPIO.output(LED_PIN, GPIO.LOW)
            time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()
    print("Programa finalizado")
# SOS con botón: Mantén presionado el botón para enviar SOS en código Morse
# Suelta el botón para detener el envío inmediatamente  
# Si el botón se suelta durante un punto o raya, el LED se apaga inmediatamente
# Detén el programa con Ctrl+C
