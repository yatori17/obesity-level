import pandas as pd
from model.model_loader import ModelLoader
import numpy as np

class PredictorService:
    def __init__(self):
        self.model = ModelLoader.load()

    def predict(self, data: dict):
        entrada = pd.DataFrame([data])
        return self.model.predict(entrada)[0]

    def prepare_form(self, form):
        # Dicionário base com todas as 23 colunas zeradas
        # Isso garante que se o usuário não selecionar 'Bike', a coluna 'MTRANS_Bike' continue 0
        input_dict = {col: 0.0 for col in [
            'Age', 'Height', 'Weight', 'FCVC', 'NCP', 'CH2O', 'FAF', 'TUE', 
            'Gender_Male', 'family_history_with_overweight_yes', 'FAVC_yes', 
            'CAEC_Frequently', 'CAEC_Sometimes', 'CAEC_no', 'SMOKE_yes', 'SCC_yes', 
            'CALC_Frequently', 'CALC_Sometimes', 'CALC_no', 'MTRANS_Bike', 
            'MTRANS_Motorbike', 'MTRANS_Public_Transportation', 'MTRANS_Walking'
        ]}

        # 1. Preenchendo valores numéricos diretos (com conversão segura)
        input_dict['Age'] = float(form.age or 0)
        input_dict['Height'] = float(form.height or 0)
        input_dict['Weight'] = float(form.weight or 0)
        input_dict['FCVC'] = float(form.vegetable_consumption or 0)
        input_dict['NCP'] = float(form.daily_meals_count or 0)
        input_dict['CH2O'] = float(form.daily_water_intake or 0)
        input_dict['FAF'] = float(form.physical_activity_frequency or 0)
        input_dict['TUE'] = float(form.tech_usage_time or 0)

        # 2. Preenchendo colunas binárias (One-Hot Encoding Manual)
        if str(form.gender).lower() in ['masculino', 'male']: input_dict['Gender_Male'] = 1.0
        if str(form.family_history).lower() in ['true', 'yes', 'sim']: input_dict['family_history_with_overweight_yes'] = 1.0
        if str(form.high_caloric_intake).lower() in ['true', 'yes', 'sim']: input_dict['FAVC_yes'] = 1.0
        if str(form.is_smoker).lower() in ['true', 'yes', 'sim']: input_dict['SMOKE_yes'] = 1.0
        if str(form.calorie_monitoring).lower() in ['true', 'yes', 'sim']: input_dict['SCC_yes'] = 1.0

        # 3. Categorias Múltiplas (CAEC, CALC, MTRANS)
        # Exemplo para MTRANS:
        mtrans = str(form.transportation_mode).lower()
        if 'bike' in mtrans: input_dict['MTRANS_Bike'] = 1.0
        elif 'public' in mtrans: input_dict['MTRANS_Public_Transportation'] = 1.0
        elif 'walking' in mtrans: input_dict['MTRANS_Walking'] = 1.0
        elif 'motor' in mtrans: input_dict['MTRANS_Motorbike'] = 1.0

        # 4. Transformar o dicionário em Array na ordem correta das colunas
        X_input = np.array([input_dict[col] for col in input_dict.keys()])
    
        return X_input