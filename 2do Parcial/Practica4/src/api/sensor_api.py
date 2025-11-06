from flask import Flask, jsonify
from datetime import datetime, timezone
import logging
import os

from .schemas import SensorReading
from src.hardware.potentiometer import Potentiometer

log = logging.getLogger("sensor_api")

def create_app():
    app = Flask(__name__)
    pot = Potentiometer()

    @app.get("/health")
    def health():
        return {"status": "ok", "ts": datetime.now(timezone.utc).isoformat()}

    @app.get("/sensor")
    def sensor():
        try:
            raw = pot.read_value()
            reading = SensorReading(
                value=raw,
                unit="adc_raw",
                timestamp=datetime.now(timezone.utc).isoformat()
            )
            return jsonify(reading.model_dump())
        except Exception as e:
            log.exception("Error leyendo potenciómetro: %s", e)
            return jsonify({"error": str(e)}), 500

    return app
