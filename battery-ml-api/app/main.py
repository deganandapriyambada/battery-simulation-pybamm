from fastapi import FastAPI
from app.routers.battery_soc_route import BatterySOCRoutes

class Main:

    def __init__(self):
        self.app = FastAPI(    
            title="Battery SOC Prediction API",
            description="API to predict State of Charge (SOC) of battery cells using ML Models (FNN)",
            version="1.0.0"
        )

    def getRoutes(self, app):
        return BatterySOCRoutes(app)

batteryAPI = Main()
app : FastAPI = batteryAPI.app
batteryAPI.getRoutes(app)