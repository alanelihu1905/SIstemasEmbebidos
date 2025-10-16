import RPi.GPIO as GPIO
import time

# Configuración del pin del servo
SERVO_PIN = 18  # GPIO 18 = pin físico 12
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Frecuencia típica de servos: 50 Hz
pwm = GPIO.PWM(SERVO_PIN, 50)
pwm.start(0)

def set_servo_angle(angle):
    """Mueve el servo al ángulo especificado (-90° a 90°)."""
    # Mapeo lineal del ángulo al duty cycle (~2.5 a ~12.5)
    duty = (angle + 90) / 18 + 2.5
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)
    pwm.ChangeDutyCycle(0)  # evita vibración

try:
    while True:
        # Posición -90°
        set_servo_angle(-90)
        print("🔹 Servo en -90°")
        time.sleep(3)

        # Posición 90°
        set_servo_angle(90)
        print("🔹 Servo en 90°")
        time.sleep(3)

except KeyboardInterrupt:
    print("\n🛑 Programa detenido por el usuario.")

finally:
    pwm.stop()
    GPIO.cleanup()
    print("✅ GPIO limpio y servo apagado correctamente.")
