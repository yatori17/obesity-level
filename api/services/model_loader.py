import joblib
import numpy
import sys

class ModelLoader:
    @staticmethod
    def load():
        return joblib.load("./model/obesity_model.pkl")