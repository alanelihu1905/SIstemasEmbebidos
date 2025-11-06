import os
import math
import time
import logging
import random

log = logging.getLogger("potentiometer")

class Potentiometer:
    """
    Abstracción del potenciómetro.
    - En Raspberry Pi con ADC real, implementa lectura real (pendiente de ADC exacto).
    - En entornos sin hardware, simula una señal suave (onda senoidal) dentro de [0,1023].
    Control via modo:
      - SIMULATED=true usa simulación siempre.
    """
    def __init__(self):
        self.simulated = os.environ.get("SIMULATED", "true").lower() == "false"
        self._start = time.time()
        # Hooks para hardware real: aquí podrías inicializar spidev/MCP3008/etc.
        if not self.simulated:
            log.info("Modo hardware real habilitado")
            # TODO: Inicializar tu ADC aquí (MCP3008, ADS1115, etc.)
        else:
            log.info("Modo SIMULADO habilitado")

    def read_value(self) -> int:
        if self.simulated:
            # Señal senoidal lenta + ruido leve
            t = time.time() - self._start
            base = (math.sin(t * 0.6) + 1.0) / 2.0  # 0..1
            noise = random.uniform(-0.03, 0.03)
            v = max(0.0, min(1.0, base + noise))
            return int(round(v * 1023))
        else:
            # Aquí iría la lectura real del ADC. Placeholder:
            # value = adc.read(channel=0)
            # return value
            raise NotImplementedError("Lectura real no implementada: conecta tu ADC y completa este método.")
