# Required External Library
from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel, Field
import tensorflow as tf
import numpy as np
import joblib
import os
from typing import List
# Required Internal module
from sklearn.preprocessing import MinMaxScaler
from app.interfaces.battery_soc_interface import BatterySOCPredictionRequest, BatterySOCPredictionResponse
from app.models.battery_soc_model import BatterySOCModel

class BatterySOCRoutes:

    def __init__(self, app : FastAPI):
        # API Metadata
        self.apiName = "SOC Prediction"
        self.apiMainPath = "/battery/soc"
        # Model & Scaler
        model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "mlmodel", "soc_prediction_model.keras")
        scaler_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "mlscaler", "soc_minmax_scaler_new.pkl")
        self.model : tf.keras.Model = tf.keras.models.load_model(model_path)
        self.scaler : MinMaxScaler  = joblib.load(scaler_path)
        # Register Applicable Route
        self.getBatteryCellSOC(app)
        self.getBatchBatteryCellSOC(app)

    def getBatteryCellSOC(self, app : FastAPI):
        @app.post(self.apiMainPath+"/cell/predict", 
            summary="predict battery cell state of charge",
            description="given three battery telemetry parameter (voltage, current and temperature), SDBMS ML models will return predicted state of charge",
            response_model=BatterySOCPredictionResponse,
            responses={500: {"description": "Internal Server Error"}},
            tags=[self.apiName]
        )
        async def predict_soc(request: BatterySOCPredictionRequest):
            try:
                # Request Handler
                inputRequest = np.array([[request.voltage, request.current, request.temperature]])
                inputScaled = self.scaler.transform(inputRequest)

                prediction = 0
                if request.voltage < 2.7:
                    prediction = 0
                elif request.voltage >= 3.8:
                    prediction = 1
                else:
                    prediction = BatterySOCModel(self.model).predictSOC(inputScaled)

                return BatterySOCPredictionResponse (
                    voltage=request.voltage,
                    current=request.current,
                    temperature=request.temperature,
                    predictedSOC=prediction
                )
             
            except Exception as e:
                print(f"Error occurred: {e}")
                raise HTTPException(
                    status_code=500,
                    detail={"statusCode": 500, "message": "Internal Server Error"}
                )
            

    def getBatchBatteryCellSOC(self, app : FastAPI):
            @app.post(self.apiMainPath+"/cells/predict", 
                summary="predict batch  battery cell state of charge",
                description="given multiple lines of three battery telemetry parameter (voltage, current and temperature), SDBMS ML models will return multiple predicted state of charge",
                responses={500: {"description": "Internal Server Error"}},
                tags=[self.apiName]
            )

            async def predict_soc(request: List[BatterySOCPredictionRequest] = Body(..., example=[
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
                ])):
                try:
                    results = []
                    # Request Handler
                    for item in request:
                        inputRequest = np.array([[item.voltage, item.current, item.temperature]])
                        inputScaled = self.scaler.transform(inputRequest)

                        if item.voltage < 2.7:
                            prediction = 0
                        else:
                            predicted_soc = BatterySOCModel(self.model).predictSOC(inputScaled)
                            prediction = np.clip(predicted_soc, 0, 1)

                            results.append({
                                "voltage": item.voltage,
                                "current": item.current,
                                "temperature": item.temperature,
                                "predictedSOC":  float(prediction)
                            })
                    print(results)
                    return {"predictions": results}
                
                except Exception as e:
                    print(f"Error occurred: {e}")
                    raise HTTPException(
                        status_code=500,
                        detail={"statusCode": 500, "message": "Internal Server Error"}
                    )