from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
import tensorflow as tf
import numpy as np
import joblib
from typing import List

model = tf.keras.models.load_model("./model/soc_prediction_model.keras")
scaler = joblib.load("./scaler/soc_minmax_scaler_new.pkl")  # Load saved scaler

app = FastAPI(    
    title="Battery SOC Prediction API",
    description="API to predict State of Charge (SOC) of battery cells using ML Models (FNN)",
    version="1.0.0"
)

class BatteryInput(BaseModel):
    voltage: float = Field(..., description="Battery Cell voltage (Volts). Ranged between 2.7 ~ 4.2. Below 2.7 SOC will 0 and above 4.1 && <= 4.2 would be 1 (100%)", example=3.)
    current: float = Field(..., description="Battery Cell Current (Ampere). Must be Negative", example=-0.02)
    temperature: float = Field(..., description="Battery voltage (Celcius)", example=-19.)

@app.post("/battery/cell/prediction/soc", tags=["SOC Prediction"])
async def predict_battery_cell_soc(request: BatteryInput):
    
    inputRequest = np.array([[request.voltage, request.current, request.temperature]])
    inputScaled = scaler.transform(inputRequest)
    if request.voltage < 2.7:
        prediction = 0
    else:
        print(scaler)
        print("Scaler min:", scaler.data_min_)
        print("Scaler max:", scaler.data_max_)
        print("Input before scaling:", inputRequest)
        print("Input after scaling:", inputScaled)
        predicted_soc = model.predict(inputScaled)[0][0]
        print(f"Raw model output: {predicted_soc:.8f}")
        prediction = np.clip(predicted_soc, 0, 1)  # Clamp to valid rang

    return {
        "voltage": request.voltage,
        "current": request.current,
        "temperature": request.temperature,
        "predictedSOC":  float(prediction)   
    }


batchBatteryCellSamplePayload = [
    {
        "voltage": 3,
        "current": -0.2,
        "temperature": -19
    },
    {
        "voltage": 2.8,
        "current": -0.03,
        "temperature": -19
    },
    {
        "voltage": 4.1,
        "current": -0.05,
        "temperature": -19
    }
]


@app.post("/battery/prediction/soc", tags=["SOC Prediction"])
async def predict_battery_soc(request: List[BatteryInput] = Body(..., example=batchBatteryCellSamplePayload)):
    results = []

    for item in request:
        inputRequest = np.array([[item.voltage, item.current, item.temperature]])
        inputScaled = scaler.transform(inputRequest)

        if item.voltage < 2.7:
            prediction = 0
        else:
            predicted_soc = model.predict(inputScaled)[0][0]
            prediction = np.clip(predicted_soc, 0, 1)

        results.append({
            "voltage": item.voltage,
            "current": item.current,
            "temperature": item.temperature,
            "predictedSOC":  float(prediction)
        })

    return {"predictions": results}