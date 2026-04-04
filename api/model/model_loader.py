import joblib
import numpy
import sys

print(numpy.__version__)


class ModelLoader:
    @staticmethod
    def load():
        return joblib.load("./model/obesity_model.pkl")