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
    predictor_service = PredictorService()
    x_input = predictor_service.prepare_form(form)
    logger.info(x_input)
    obesity_level = str(predictor_service.predict(x_input)[0])

    paciente = ObesityMetrics(
        name = form.name,
        gender= form.gender,
        age= form.age,
        height= form.height,
        weight=form.weight,
        family_history= form.family_history,
        high_caloric_intake= form.high_caloric_intake,
        vegetable_consumption= form.vegetable_consumption,
        daily_meals_count= form.daily_meals_count,
        food_between_meals= form.food_between_meals,
        is_smoker= form.is_smoker,
        daily_water_intake= form.daily_water_intake,
        calorie_monitoring= form.calorie_monitoring,
        physical_activity_frequency= form.physical_activity_frequency,
        tech_usage_time= form.tech_usage_time,
        alcohol_consumption= form.alcohol_consumption,
        transportation_mode= form.transportation_mode,
        obesity_level= form.obesity_level
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

