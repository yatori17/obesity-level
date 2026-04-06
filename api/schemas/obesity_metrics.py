from pydantic import BaseModel
from typing import List, Optional, Literal
from model.obesity_metrics import ObesityMetrics
from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class ObesityMetricsSchema(BaseModel):
    id: Optional[int] = None
    
    name: str
    gender: str
    age: float
    height: float
    weight: float
    
    family_history: bool = False
    high_caloric_intake: bool = False
    is_smoker: bool = False
    calorie_monitoring: bool = False
    
    vegetable_consumption: float
    daily_meals_count: float
    daily_water_intake: float
    physical_activity_frequency: float
    tech_usage_time: float
    
    food_between_meals: str
    alcohol_consumption: str
    transportation_mode: str
    obesity_level: Optional[str]
    model_config = ConfigDict(from_attributes=True)

class ObesityMetricsSearchSchema(BaseModel):
    name: Optional[str]

class ObesityMetricsDeleteSchema(BaseModel):
    id: int

def present_obesity_metrics(obesity_metrics: ObesityMetrics):
    """ Returns a representation of the obesity_metric table
    """
    return {
        "id": obesity_metrics.id,
        "name": obesity_metrics.name,
        "gender": obesity_metrics.gender,
        "age": obesity_metrics.age,
        "height": obesity_metrics.height,
        "weight": obesity_metrics.weight,
        "family_history": obesity_metrics.family_history,
        "high_caloric_intake": obesity_metrics.high_caloric_intake,
        "vegetable_consumption": obesity_metrics.vegetable_consumption,
        "daily_meals_count": obesity_metrics.daily_meals_count,
        "food_between_meals": obesity_metrics.food_between_meals,
        "is_smoker": obesity_metrics.is_smoker,
        "daily_water_intake": obesity_metrics.daily_water_intake,
        "calorie_monitoring": obesity_metrics.calorie_monitoring,
        "physical_activity_frequency": obesity_metrics.physical_activity_frequency,
        "tech_usage_time": obesity_metrics.tech_usage_time,
        "alcohol_consumption": obesity_metrics.alcohol_consumption,
        "transportation_mode": obesity_metrics.transportation_mode,
        "obesity_level": obesity_metrics.obesity_level
    }

def present_obesity_metrics_list(obesity_metrics_list: List[ObesityMetrics]):
    result = []
    for obesity_metrics in obesity_metrics_list:
        result.append({
        "id": obesity_metrics.id,
        "name": obesity_metrics.name,
        "gender": obesity_metrics.gender,
        "age": obesity_metrics.age,
        "height": obesity_metrics.height,
        "weight": obesity_metrics.weight,
        "family_history": obesity_metrics.family_history,
        "high_caloric_intake": obesity_metrics.high_caloric_intake,
        "vegetable_consumption": obesity_metrics.vegetable_consumption,
        "daily_meals_count": obesity_metrics.daily_meals_count,
        "food_between_meals": obesity_metrics.food_between_meals,
        "is_smoker": obesity_metrics.is_smoker,
        "daily_water_intake": obesity_metrics.daily_water_intake,
        "calorie_monitoring": obesity_metrics.calorie_monitoring,
        "physical_activity_frequency": obesity_metrics.physical_activity_frequency,
        "tech_usage_time": obesity_metrics.tech_usage_time,
        "alcohol_consumption": obesity_metrics.alcohol_consumption,
        "transportation_mode": obesity_metrics.transportation_mode,
        "obesity_level": obesity_metrics.obesity_level
    })
    return {"obesity_metrics_list": result}