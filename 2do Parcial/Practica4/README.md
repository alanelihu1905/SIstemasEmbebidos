<div align="center">

# Proyecto Sensor–Servo  
### **Práctica 4 — Sistemas Embebidos**

**Universidad Autónoma de Campeche**  
**Ingeniería en Tecnología de Software**  

---

### **Equipo de Trabajo**

| Integrante |
|-------------|
| **Daniel Esquivel** |
| **Miranda Amaro** |
| **Fernando Sabido** |
| **Alan Flores** |
| **Iker Sánchez** |

---

</div>

##  Objetivo del Proyecto

Desarrollar un sistema embebido modular que integre:
- Un **potenciómetro** como sensor analógico.  
- Un **servo motor** como actuador.  
- Una **API Flask** para exponer los datos del sensor.  
- Un **cliente Python** que consume la API y controla el servo.  

Todo esto puede ejecutarse en **modo simulado** (sin hardware) o en **modo real** (en Raspberry Pi).  

---


### Estructura del Proyecto

```bash
proyecto_sensor_servo/
├── main.py
├── requirements.txt
├── src/
│   ├── api/
│   ├── hardware/
│   └── client/
└── docs/
    └── api_documentation.md


## Modo de Ejecución

El sistema tiene dos modos principales:

| Modo | Descripción |
|------|--------------|
| **Simulado** | Genera valores del potenciómetro con una onda senoidal y mueve el servo virtualmente (solo logs). |
| **Real (Raspberry Pi)** | Usa componentes físicos: ADC (para leer el potenciómetro) y PWM (para el servo). |

---

### 🔹 Activar el modo simulado (por defecto)
```bash
export SIMULATED=true

### 🔹 Activar el modo real (solo en Raspberry Pi)
```bash
export SIMULATED=false