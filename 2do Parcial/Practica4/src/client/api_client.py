import time
import logging
from dataclasses import dataclass
from typing import Optional
import requests

log = logging.getLogger("api_client")

@dataclass
class SensorReadingDTO:
    value: int
    unit: str
    timestamp: str

class SensorAPIClient:
    def __init__(self, base_url: str, timeout: float = 2.0, max_retries: int = 3, backoff: float = 0.5):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff = backoff

    def get_reading(self) -> SensorReadingDTO:
        url = f"{self.base_url}/sensor"
        last_err: Optional[Exception] = None
        for attempt in range(1, self.max_retries + 1):
            try:
                resp = requests.get(url, timeout=self.timeout)
                resp.raise_for_status()
                data = resp.json()
                return SensorReadingDTO(value=int(data["value"]), unit=data.get("unit", "adc_raw"), timestamp=data["timestamp"])
            except Exception as e:
                last_err = e
                log.warning("Intento %s/%s falló: %s", attempt, self.max_retries, e)
                time.sleep(self.backoff * attempt)
        # si se agotan reintentos
        raise RuntimeError(f"No se pudo obtener lectura del API: {last_err}")
