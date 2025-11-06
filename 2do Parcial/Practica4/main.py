import os
import time
import threading
import logging
import argparse

from src.api.sensor_api import create_app
from src.client.api_client import SensorAPIClient
from src.hardware.servo import ServoController

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "INFO"),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
log = logging.getLogger("main")

def run_api(host: str, port: int):
    app = create_app()
    app.run(host=host, port=port, debug=False, use_reloader=False)

def run_control_loop(api_url: str, interval: float, min_angle: int, max_angle: int):
    client = SensorAPIClient(base_url=api_url, timeout=2.0, max_retries=3)
    servo = ServoController(min_angle=min_angle, max_angle=max_angle)
    log.info("Control loop iniciado: %s -> servo [%s, %s] grados", api_url, min_angle, max_angle)
    while True:
        try:
            reading = client.get_reading()
            # reading.value is expected in [0,1023]
            val = reading.value
            angle = ServoController.map_value_to_angle(val, in_min=0, in_max=1023, out_min=min_angle, out_max=max_angle)
            servo.set_angle(angle)
            log.info("Pot=%s -> Angle=%s", val, angle)
        except Exception as e:
            log.error("Error en control loop: %s", e)
        time.sleep(interval)

def parse_args():
    p = argparse.ArgumentParser(description="Proyecto Sensor-Servo (API + Control)")
    p.add_argument("--mode", choices=["api", "control", "both"], default="both",
                   help="Qué ejecutar: servidor API, lazo de control o ambos")
    p.add_argument("--host", default=os.environ.get("API_HOST", "0.0.0.0"))
    p.add_argument("--port", type=int, default=int(os.environ.get("API_PORT", "5050")))
    p.add_argument("--api-url", default=os.environ.get("API_URL", "http://127.0.0.1:5050"))
    p.add_argument("--interval", type=float, default=float(os.environ.get("CONTROL_INTERVAL", "0.5")),
                   help="Segundos entre lecturas al API")
    p.add_argument("--min-angle", type=int, default=int(os.environ.get("MIN_ANGLE", "0")))
    p.add_argument("--max-angle", type=int, default=int(os.environ.get("MAX_ANGLE", "180")))
    return p.parse_args()

if __name__ == "__main__":
    args = parse_args()

    if args.mode == "api":
        run_api(args.host, args.port)
    elif args.mode == "control":
        run_control_loop(args.api_url, args.interval, args.min_angle, args.max_angle)
    else:
        # both
        t = threading.Thread(target=run_api, args=(args.host, args.port), daemon=True)
        t.start()
        # espera un poco a que levante
        time.sleep(1.0)
        run_control_loop(args.api_url, args.interval, args.min_angle, args.max_angle)
