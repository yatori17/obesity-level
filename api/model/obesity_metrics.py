from sqlalchemy import Column, Integer, String, Float, Boolean, CheckConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class ObesityMetrics(Base):
    """
    Schema for the UCI Obesity Levels Dataset
    Refactored for Clean Code and Frontend Integration
    """
    __tablename__ = 'obesity_metrics'

    # Primary Key
    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String(50), nullable = False)
    gender = Column(String(10), nullable=False)
    age = Column(Float, nullable=False)
    height = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)

    # Converting 'yes/no' of dataset to real Boolean
    family_history = Column(Boolean, default=False)
    high_caloric_intake = Column(Boolean, default=False) # Original: FAVC
    is_smoker = Column(Boolean, default=False)           # Original: SMOKE
    calorie_monitoring = Column(Boolean, default=False)  # Original: SCC

    # --- Dietary Habits (Numeric/Frequency) ---
    vegetable_consumption = Column(Float) # FCVC: 1 to 3
    daily_meals_count = Column(Float)     # NCP: 1 to 4
    daily_water_intake = Column(Float)    # CH2O: 1 to 3
    
    # --- Categories (Categorical/String) ---
    food_between_meals = Column(String(20)) # CAEC: No, Sometimes, Frequently, Always
    alcohol_consumption = Column(String(20)) # CALC: No, Sometimes, Frequently, Always
    transportation_mode = Column(String(30)) # MTRANS: Public_Tr, Walking, Automobile, etc.

    # --- Physical Activity & Tech ---
    physical_activity_frequency = Column(Float) # FAF: 0 to 3 (days)
    tech_usage_time = Column(Float)             # TUE: 0 to 2 (hours)

    # --- Target Variable ---
    obesity_level = Column(String(50), nullable=False) # NObeyesdad: Normal, Obesity I, II, etc.

    def __repr__(self):
        return f"<ObesityMetrics(id={self.id}, level='{self.obesity_level}')>"