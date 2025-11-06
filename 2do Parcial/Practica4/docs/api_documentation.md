# Documentación de la API

## Endpoints

### `GET /health`
**Respuesta 200**
```json
{ "status": "ok", "ts": "2025-01-01T00:00:00Z" }
```

### `GET /sensor`
Retorna la lectura actual del potenciómetro.

**Respuesta 200**
```json
{
  "value": 512,
  "unit": "adc_raw",
  "timestamp": "2025-01-01T00:00:00Z"
}
```

**Respuesta 500**
```json
{ "error": "Descripción del error" }
```

## Esquemas
- `value`: entero [0, 1023]
- `unit`: cadena (por defecto `adc_raw`)
- `timestamp`: ISO8601
