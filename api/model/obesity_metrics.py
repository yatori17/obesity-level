from sqlalchemy import Column, Integer, String, Float, Boolean, CheckConstraint
from  model import Base

class ObesityMetrics(Base):
    __tablename__ = 'obesity_metrics'

    # Primary Key
    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String(50), nullable = False)
    gender = Column(String(10), nullable=False)
    age = Column(Float, nullable=False)
    height = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)

    family_history = Column(Boolean, default=False)
    high_caloric_intake = Column(Boolean, default=False) # Original: FAVC
    is_smoker = Column(Boolean, default=False)           # Original: SMOKE
    calorie_monitoring = Column(Boolean, default=False)  # Original: SCC

    vegetable_consumption = Column(Float) # FCVC: 1 to 3
    daily_meals_count = Column(Float)     # NCP: 1 to 4
    daily_water_intake = Column(Float)    # CH2O: 1 to 3
    
    food_between_meals = Column(String(20)) # CAEC: No, Sometimes, Frequently, Always
    alcohol_consumption = Column(String(20)) # CALC: No, Sometimes, Frequently, Always
    transportation_mode = Column(String(30)) # MTRANS: Public_Tr, Walking, Automobile, etc.

    # --- Physical Activity & Tech ---
    physical_activity_frequency = Column(Float) # FAF: 0 to 3 (days)
    tech_usage_time = Column(Float)             # TUE: 0 to 2 (hours)

    # --- Target Variable ---
    obesity_level = Column(String(50), nullable=False) # NObeyesdad: Normal, Obesity I, II, etc.

    from datetime import datetime

    def __init__(self, 
             name: str, 
             gender: str, 
             age: float, 
             height: float, 
             weight: float, 
             family_history: bool,
             high_caloric_intake: bool,
             is_smoker: bool,
             calorie_monitoring: bool,
             vegetable_consumption: float,
             daily_meals_count: float,
             daily_water_intake: float,
             food_between_meals: str,
             alcohol_consumption: str,
             transportation_mode: str,
             physical_activity_frequency: float,
             tech_usage_time: float,
             obesity_level: str):
        """
        Cria uma nova instância de métricas de obesidade.
    
        Args:
        name: Nome do usuário.
        gender: Gênero (Masculino/Feminino).
        age: Idade em anos.
        height: Altura em metros.
        weight: Peso em quilogramas.
        family_history: Histórico familiar de sobrepeso (True/False).
        high_caloric_intake: Consumo frequente de alimentos calóricos (FAVC).
        is_smoker: Se o usuário é fumante.
        calorie_monitoring: Se monitora calorias (SCC).
        vegetable_consumption: Frequência de consumo de vegetais (FCVC).
        daily_meals_count: Número de refeições principais (NCP).
        daily_water_intake: Consumo de água diário (CH2O).
        food_between_meals: Consumo de comida entre refeições (CAEC).
        alcohol_consumption: Consumo de álcool (CALC).
        transportation_mode: Meio de transporte principal (MTRANS).
        physical_activity_frequency: Frequência de atividade física (FAF).
        tech_usage_time: Tempo de uso de dispositivos tecnológicos (TUE).
        obesity_level: Resultado da predição do modelo (Target).
        """
        self.name = name
        self.gender = gender
        self.age = age
        self.height = height
        self.weight = weight
        self.family_history = family_history
        self.high_caloric_intake = high_caloric_intake
        self.is_smoker = is_smoker
        self.calorie_monitoring = calorie_monitoring
        self.vegetable_consumption = vegetable_consumption
        self.daily_meals_count = daily_meals_count
        self.daily_water_intake = daily_water_intake
        self.food_between_meals = food_between_meals
        self.alcohol_consumption = alcohol_consumption
        self.transportation_mode = transportation_mode
        self.physical_activity_frequency = physical_activity_frequency
        self.tech_usage_time = tech_usage_time
        self.obesity_level = obesity_level