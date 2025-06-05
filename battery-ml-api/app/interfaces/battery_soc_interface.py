from pydantic import BaseModel, Field

class BatterySOCPredictionRequest(BaseModel):
    voltage: float = Field(..., description="Battery Cell voltage (Volts). Ranged between 2.7 ~ 4.2. Below 2.7 SOC will 0 and above 4.1 && <= 4.2 would be 1 (100%)", example=3.)
    current: float = Field(..., description="Battery Cell Current (Ampere). Must be Negative", example=-0.02)
    temperature: float = Field(..., description="Battery voltage (Celcius)", example=-19.)

class BatterySOCPredictionResponse(BaseModel):
    voltage: float
    current: float
    temperature: float
    predictedSOC: float  # The predicted state of charge (SOC)