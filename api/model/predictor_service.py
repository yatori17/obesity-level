import pandas as pd
from model.model_loader import ModelLoader

class PredictorService:
    def __init__(self):
        self.model = ModelLoader.load()

    def predict(self, data: dict):
        entrada = pd.DataFrame([data])
        return self.model.predict(entrada)[0]