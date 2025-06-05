import tensorflow as tf

class BatterySOCModel:

    def __init__(self, mlmodel : tf.keras.Model):
        self.model : tf.keras.Model = mlmodel

    def predictSOC(self, scaledInput) -> float:
        return float(self.model.predict(scaledInput)[0][0])
