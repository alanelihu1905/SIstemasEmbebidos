from pydantic import BaseModel, Field

class SensorReading(BaseModel):
    value: int = Field(..., ge=0, le=1023, description="Valor ADC crudo del potenciómetro")
    unit: str = Field(default="adc_raw", description="Unidad de medida")
    timestamp: str = Field(..., description="ISO8601 timestamp")
