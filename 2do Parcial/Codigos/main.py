import RPi.GPIO as GPIO
import time
from flask import Flask, jsonify
from datetime import datetime
import threading
import logging
import signal
import sys

# -------------------------------
# CONFIGURACIÓN INICIAL
# -------------------------------
POT_PIN = 4
GPIO.setmode(GPIO.BCM)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

# -------------------------------
# VARIABLES GLOBALES
# -------------------------------
app = Flask(__name__)
datos_sensor = {
    "valor_crudo": 0,
    "porcentaje": '0%',
    "resistencia_aprox": "0Ω",
    "ultima_actualizacion": None
}
datos_sensor_lock = threading.Lock()
min_value = 0
max_value = 100
running = True  # Control del bucle del hilo

# -------------------------------
# FUNCIONES DEL SENSOR
# -------------------------------
def read_potentiometer():
    """Lee el valor del potenciómetro mediante carga/descarga del pin."""
    count = 0
    GPIO.setup(POT_PIN, GPIO.OUT)
    GPIO.output(POT_PIN, False)
    time.sleep(0.1)
    
    GPIO.setup(POT_PIN, GPIO.IN)
    
    while GPIO.input(POT_PIN) == GPIO.LOW:
        count += 1
        if count > 100000:  # Timeout
            break
    return count


def calibrate():
    """Calibra los valores mínimo y máximo del potenciómetro."""
    logging.info("Iniciando calibración para potenciómetro 10K...")
    
    logging.info("→ Gira completamente a la izquierda (mínimo)")
    time.sleep(3)
    min_val = read_potentiometer()
    
    logging.info("→ Gira completamente a la derecha (máximo)")
    time.sleep(3)
    max_val = read_potentiometer()

    if max_val <= min_val:
        logging.warning("Mínimo y máximo son iguales o inválidos. Ajustando...")
        max_val = min_val + 100  # Evitar división por cero
    
    logging.info(f"Calibración completada: Mínimo={min_val}, Máximo={max_val}")
    return min_val, max_val


def update_sensor():
    """Hilo en segundo plano que actualiza continuamente los valores del sensor."""
    global running
    while running:
        try:
            value = read_potentiometer()
            
            normalized = 0.0
            if (max_value - min_value) > 0:
                normalized = (value - min_value) / (max_value - min_value) * 100.0
                normalized = max(0, min(100, normalized))
            
            resistance_approx = (normalized / 100) * 10000  # 10k ohms
            
            # Actualizar datos globales con bloqueo
            with datos_sensor_lock:
                datos_sensor["valor_crudo"] = value
                datos_sensor["porcentaje"] = f"{normalized:5.1f}%"
                datos_sensor["resistencia_aprox"] = f"~{resistance_approx:4.0f}Ω"
                datos_sensor["ultima_actualizacion"] = datetime.now().isoformat()

            logging.info(f"Crudo={value:5d} | {normalized:5.1f}% | ~{resistance_approx:5.0f}Ω")
            time.sleep(0.3)

        except Exception as e:
            logging.error(f"Error en actualización del sensor: {e}")
            time.sleep(2)


# -------------------------------
# ENDPOINTS DE LA API
# -------------------------------
@app.route('/')
def home():
    """Muestra los endpoints disponibles."""
    return jsonify({
        "mensaje": "API del Sensor de Potenciómetro",
        "endpoints": ["/api/sensor", "/api/estado", "/api/calibrar"]
    })


@app.route('/api/sensor')
def get_sensor_data():
    """Devuelve los datos actuales del sensor."""
    with datos_sensor_lock:
        return jsonify(datos_sensor.copy())


@app.route('/api/estado')
def get_status():
    """Devuelve el estado general del sistema."""
    return jsonify({
        "estado": "sistema funcionando",
        "timestamp": datetime.now().isoformat()
    })


@app.route('/api/calibrar')
def recalibrate():
    """Permite recalibrar el sensor desde la API."""
    global min_value, max_value
    min_value, max_value = calibrate()
    return jsonify({
        "mensaje": "Recalibración completada",
        "nuevo_minimo": min_value,
        "nuevo_maximo": max_value
    })


# -------------------------------
# FUNCIONES PRINCIPALES
# -------------------------------
def signal_handler(sig, frame):
    """Maneja Ctrl+C para cerrar correctamente."""
    global running
    logging.info("\nInterrupción detectada. Cerrando programa...")
    running = False
    time.sleep(1)
    GPIO.cleanup()
    logging.info("GPIO limpiado. Bye Bye.")
    sys.exit(0)


def setup():
    """Configuración inicial del sistema."""
    global min_value, max_value
    
    signal.signal(signal.SIGINT, signal_handler)

    min_value, max_value = calibrate()
    
    logging.info("Iniciando hilo de actualización del sensor...")
    sensor_thread = threading.Thread(target=update_sensor, daemon=True)
    sensor_thread.start()

    logging.info("Iniciando servidor Flask en http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)


# -------------------------------
# PUNTO DE ENTRADA
# -------------------------------
if __name__ == "__main__":
    setup()