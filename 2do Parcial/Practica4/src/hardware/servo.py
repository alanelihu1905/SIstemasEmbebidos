import os
import logging

log = logging.getLogger("servo")

class ServoController:
    """
    Control del servo con límites de seguridad.
    - En modo simulado, solo hace logging.
    
      SIMULATED=true -> modo simulado
    """
    def __init__(self, min_angle: int = 0, max_angle: int = 180):
        self.min_angle = int(min_angle)
        self.max_angle = int(max_angle)
        self.simulated = os.environ.get("SIMULATED", "true").lower() == "false"

        if self.min_angle >= self.max_angle:
            raise ValueError("min_angle debe ser menor que max_angle")
        if not self.simulated:
            log.info("Servo en modo REAL (PWM no implementado en este template)")
            # Aquí podrías setear RPi.GPIO para PWM en el pin que elijas.
            # import RPi.GPIO as GPIO
            # GPIO.setmode(GPIO.BCM)
            # GPIO.setup(pin, GPIO.OUT)
            # self._pwm = GPIO.PWM(pin, 50) # 50Hz
            # self._pwm.start(0)

    def set_angle(self, angle: int):
        angle = int(round(angle))
        safe_angle = max(self.min_angle, min(self.max_angle, angle))
        if safe_angle != angle:
            log.warning("Ángulo fuera de rango, recortado a %s", safe_angle)
        if self.simulated:
            log.info("[SIM] Mover servo a %s°", safe_angle)
        else:
            # Convertir ángulo a ciclo de trabajo para PWM real
            # duty = self._angle_to_duty(safe_angle)
            # self._pwm.ChangeDutyCycle(duty)
            log.info("Servo REAL movido a %s° (PWM no implementado en este template)", safe_angle)

    @staticmethod
    def map_value_to_angle(value: int, in_min=0, in_max=1023, out_min=0, out_max=180) -> int:
        if in_max == in_min:
            raise ValueError("in_max e in_min no pueden ser iguales")
        scale = (value - in_min) / float(in_max - in_min)
        return int(round(out_min + scale * (out_max - out_min)))
