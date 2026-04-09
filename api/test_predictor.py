import pytest
import pandas as pd
import numpy as np
from model.predictor_service import PredictorService
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


@pytest.fixture
def predictor():
    """Fixture para instanciar o serviço uma única vez para os testes"""
    return PredictorService()


def test_model_prediction_performance(predictor):
    """
    Teste de desempenho: Verifica se o modelo mantém a acurácia mínima 
    em um conjunto de dados de 'Gold Standard' (Casos conhecidos).
    """
    test_cases = [
        {
            "name": "Atleta_Saudavel",
            "data": {
                'Age': 25.0, 'Height': 1.85, 'Weight': 78.0, 'FCVC': 3.0, 'NCP': 3.0,
                'CH2O': 3.0, 'FAF': 3.0, 'TUE': 0.0, 'Gender_Male': 1.0,
                'family_history_with_overweight_yes': 0.0, 'FAVC_yes': 0.0,
                'CAEC_Frequently': 0.0, 'CAEC_Sometimes': 1.0, 'CAEC_no': 0.0,
                'SMOKE_yes': 0.0, 'SCC_yes': 1.0, 'CALC_Frequently': 0.0,
                'CALC_Sometimes': 0.0, 'CALC_no': 1.0, 'MTRANS_Bike': 0.0,
                'MTRANS_Motorbike': 0.0, 'MTRANS_Public_Transportation': 0.0, 'MTRANS_Walking': 1.0
            },
            "expected": "Normal_Weight"
        },
        {
            "name": "Sedentario_Risco",
            "data": {
                'Age': 40.0, 'Height': 1.65, 'Weight': 95.0, 'FCVC': 2.0, 'NCP': 3.0,
                'CH2O': 1.0, 'FAF': 0.0, 'TUE': 2.0, 'Gender_Male': 0.0,
                'family_history_with_overweight_yes': 1.0, 'FAVC_yes': 1.0,
                'CAEC_Frequently': 0.0, 'CAEC_Sometimes': 1.0, 'CAEC_no': 0.0,
                'SMOKE_yes': 0.0, 'SCC_yes': 0.0, 'CALC_Frequently': 0.0,
                'CALC_Sometimes': 1.0, 'CALC_no': 0.0, 'MTRANS_Bike': 0.0,
                'MTRANS_Motorbike': 1.0, 'MTRANS_Public_Transportation': 0.0, 'MTRANS_Walking': 0.0
            },
            "expected": "Obesity_Type_I"
        },
        {
            "name": "Baixo_Peso_Jovem",
            "data": {
                'Age': 19.0, 'Height': 1.78, 'Weight': 52.0, 'FCVC': 2.0, 'NCP': 2.0,
                'CH2O': 2.0, 'FAF': 1.0, 'TUE': 1.0, 'Gender_Male': 1.0,
                'family_history_with_overweight_yes': 0.0, 'FAVC_yes': 0.0,
                'CAEC_Frequently': 1.0, 'CAEC_Sometimes': 0.0, 'CAEC_no': 0.0,
                'SMOKE_yes': 0.0, 'SCC_yes': 0.0, 'CALC_Frequently': 0.0,
                'CALC_Sometimes': 0.0, 'CALC_no': 1.0, 'MTRANS_Bike': 0.0,
                'MTRANS_Motorbike': 0.0, 'MTRANS_Public_Transportation': 1.0, 'MTRANS_Walking': 0.0
            },
            "expected": "Insufficient_Weight"
        },
        {
            "name": "Sobrepeso_Moderado",
            "data": {
                'Age': 32.0, 'Height': 1.70, 'Weight': 82.0, 'FCVC': 2.0, 'NCP': 3.0,
                'CH2O': 2.0, 'FAF': 1.0, 'TUE': 1.0, 'Gender_Male': 0.0,
                'family_history_with_overweight_yes': 1.0, 'FAVC_yes': 1.0,
                'CAEC_Frequently': 0.0, 'CAEC_Sometimes': 1.0, 'CAEC_no': 0.0,
                'SMOKE_yes': 0.0, 'SCC_yes': 0.0, 'CALC_Frequently': 0.0,
                'CALC_Sometimes': 1.0, 'CALC_no': 0.0, 'MTRANS_Bike': 0.0,
                'MTRANS_Motorbike': 0.0, 'MTRANS_Public_Transportation': 1.0, 'MTRANS_Walking': 0.0
            },
            "expected": "Overweight_Level_II"
        },
        {
            "name": "Obesidade_III_Critica",
            "data": {
                'Age': 26.0, 'Height': 1.62, 'Weight': 125.0, 'FCVC': 3.0, 'NCP': 3.0,
                'CH2O': 1.5, 'FAF': 0.0, 'TUE': 2.0, 'Gender_Male': 0.0,
                'family_history_with_overweight_yes': 1.0, 'FAVC_yes': 1.0,
                'CAEC_Frequently': 0.0, 'CAEC_Sometimes': 1.0, 'CAEC_no': 0.0,
                'SMOKE_yes': 0.0, 'SCC_yes': 0.0, 'CALC_Frequently': 0.0,
                'CALC_Sometimes': 1.0, 'CALC_no': 0.0, 'MTRANS_Bike': 0.0,
                'MTRANS_Motorbike': 0.0, 'MTRANS_Public_Transportation': 1.0, 'MTRANS_Walking': 0.0
            },
            "expected": "Obesity_Type_III"
        }
    ]
    hits = 0
    total = len(test_cases)
    for case in test_cases:
        resultado = predictor.predict(case["data"])
        if resultado == case["expected"]:
            hits = hits + 1
    acuracia_final = (hits / total) * 100
    assert acuracia_final >= 80.0, f"Acurácia na predicao ({acuracia_final}%) abaixo do esperado!"


def test_prepare_form_output_shape(predictor):
    """Verifica se o prepare_form retorna o array com as 23 colunas esperadas"""
    class MockForm:
        age = 25
        height = 1.75
        weight = 80
        vegetable_consumption = 2
        daily_meals_count = 3
        daily_water_intake = 2
        physical_activity_frequency = 1
        tech_usage_time = 1
        gender = 'male'
        family_history = 'yes'
        high_caloric_intake = 'yes'
        is_smoker = 'no'
        calorie_monitoring = 'no'
        transportation_mode = 'public'

    result = predictor.prepare_form(MockForm())
    assert len(result) == 23
    assert isinstance(result, (list, np.ndarray))


def test_modelo_obesidade():
    service = PredictorService()

    data = pd.read_csv(
        "https://raw.githubusercontent.com/yatori17/burnout/refs/heads/main/ObesityDataSet_raw_and_data_sinthetic.csv", delimiter=',')
    X = data.drop('NObeyesdad', axis=1)
    Y_test = data['NObeyesdad']
    X_test = pd.get_dummies(X, drop_first=True)

    predicoes = service.model.predict(X_test)
    acuracia = accuracy_score(Y_test, predicoes)

    assert acuracia >= 0.85
