from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, ObesityMetrics
from model.predictor_service import PredictorService
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Obesity Report", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentation", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
obesity_metrics_tag = Tag(name="ObesityMetrics", description="CRD (Create/Read/Delete) for obesity metrics and prediction of obesity")

@app.get('/', tags=[home_tag])
def home():
    return redirect("/frontend/index.html")

@app.post("/obesity-metrics", tags=[obesity_metrics_tag],
          responses={"200": ObesityMetricsSchema, "400": ErrorSchema})
def predict_obesity_level(form: ObesityMetricsSchema):
    gender = form.gender
    age = form.age
    height = form.height
    weight = form.weight
    family_history = form.family_history
    high_caloric_intake = form.high_caloric_intake
    is_smoker = form.is_smoker
    calorie_monitoring = form.calorie_monitoring
    veg_cons = form.vegetable_consumption
    meals = form.daily_meals_count
    water = form.daily_water_intake
    phys_act = form.physical_activity_frequency
    tech_usage = form.tech_usage_time
    food_between = form.food_between_meals
    alcohol = form.alcohol_consumption
    transport = form.transportation_mode
    predictor_service = PredictorService()
    
    obesity_level = str(predictor_service.predict(X_input)[0])

    paciente = ObesityMetrics(
        name = form.name,
        gender=gender,
        age=age,
        height=height,
        weight=weight,
        family_history=family_history,
        high_caloric_intake=high_caloric_intake,
        vegetable_consumption=veg_cons,
        daily_meals_count=meals,
        food_between_meals=food_between,
        is_smoker=is_smoker,
        daily_water_intake=water,
        calorie_monitoring=calorie_monitoring,
        physical_activity_frequency=phys_act,
        tech_usage_time=tech_usage,
        alcohol_consumption=alcohol,
        transportation_mode=transport,
        obesity_level=obesity_level
    )

    logger.debug(f"Processando predição para paciente de idade: '{paciente.age}'")

    try:
        session = Session()

        # Adicionando o registro ao banco
        session.add(paciente)
        session.commit()
        
        logger.debug(f"Adicionado registro de obesidade ID: '{paciente.id}'")
        
        # Retorna usando a função de visualização que criamos anteriormente
        return apresenta_paciente_obesidade(paciente), 200

    except Exception as e:
        error_msg = f"Não foi possível salvar os dados de métricas: {str(e)}"
        logger.warning(f"Erro ao processar métricas, {error_msg}")
        return {"message": "Erro interno ao salvar os dados."}, 400


@app.get('/obesity-metrics', tags=[obesity_metrics_tag],
         responses={"200": ObesityMetricsSearchSchema, "404": ErrorSchema})
def get_obesity_metrics(query: ObesityMetricsSearchSchema):
    logger.debug("Retrieving ObesityMetricsSearchSchema")
    session = Session()
    searchQuery = session.query(ObesityMetrics)
    searchQuery = searchQuery.filter(ObesityMetrics.name.ilike(f"%{query.name}%"))

    obesityMetrics = searchQuery.all()

    if not obesityMetrics:
        return {"obesityMetrics": []}, 200

    logger.debug(f"{len(obesityMetrics)} obesityMetrics found")
    return present_obesity_metrics(obesityMetrics), 200

