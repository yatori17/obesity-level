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
    logger.info(form)
    predictor_service = PredictorService()
    x_input = predictor_service.prepare_form(form)
    logger.info(x_input)
    obesity_level = str(predictor_service.predict(x_input))

    paciente = ObesityMetrics(
        name = form.name,
        gender= form.gender,
        age= form.age,
        height= form.height,
        weight=form.weight,
        family_history= bool(form.family_history),
        high_caloric_intake= bool(form.high_caloric_intake),
        vegetable_consumption= form.vegetable_consumption,
        daily_meals_count= form.daily_meals_count,
        food_between_meals= form.food_between_meals,
        is_smoker= bool(form.is_smoker),
        daily_water_intake= form.daily_water_intake,
        calorie_monitoring= bool(form.calorie_monitoring),
        physical_activity_frequency= form.physical_activity_frequency,
        tech_usage_time= form.tech_usage_time,
        alcohol_consumption= form.alcohol_consumption,
        transportation_mode= form.transportation_mode,
        obesity_level= obesity_level
    )

    logger.info(f"Processando predição para paciente de idade: '{paciente.age}'")

    try:
        session = Session()

        if session.query(ObesityMetrics).filter(ObesityMetrics.name == form.name).first():
            error_msg = "Métricas já existente para esse nome"
            logger.warning(
                f"Erro ao adicionar paciente '{paciente.name}', {error_msg}"
            )
            return {"message": error_msg}, 409   
             
        session.add(paciente)
        session.commit()
        
        logger.debug(f"Adicionado registro de obesidade ID: '{paciente.id}'")
        
        return present_obesity_metrics(paciente), 200

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
    if query.name:
        searchQuery = searchQuery.filter(ObesityMetrics.name.ilike(f"%{query.name}%"))
    logger.info(query.name)
    obesityMetrics = searchQuery.all()

    if not obesityMetrics:
        return {"obesityMetrics": []}, 200

    logger.debug(f"{len(obesityMetrics)} obesityMetrics found")
    return present_obesity_metrics_list(obesityMetrics), 200

@app.get(
    "/obesity-metrics/<int:id>",
    tags=[obesity_metrics_tag],
    responses={
        "200": ObesityMetricsSchema,
        "404": ErrorSchema,
    },
)
def get_obesity_metrics_by_id(path: ObesityMetricsPath):
    logger.debug(f"Retrieving obesityMetrics with id={path.id}")
    session = Session()

    obesity_metrics = session.query(ObesityMetrics).filter(ObesityMetrics.id == path.id).first()

    if not obesity_metrics:
        logger.warning(f"ObesityMetrics report with id={id} not found")
        return {"error": "ObesityMetrics report not found!"}, 404

    logger.debug(f"ObesityMetrics found: {obesity_metrics.name}")
    return present_obesity_metrics(obesity_metrics), 200



@app.delete(
    "/obesity-metrics",
    tags=[obesity_metrics_tag],
    responses={"200": ObesityMetricsSchema, "404": ErrorSchema},
)
def delete_paciente(query: ObesityMetricsDeleteSchema):
    """Removes a obesity metrics from the database

    Args:
        id (integer) the id of the report

    Returns:
        msg: Success message or error
    """
    obesity_metrics_id = query.id
    logger.debug(f"Deleting report with id #{obesity_metrics_id}")

    session = Session()
    obesity_metrics = (
        session.query(ObesityMetrics).filter(ObesityMetrics.id == obesity_metrics_id).first()
    )

    if not obesity_metrics:
        error_msg = "ObesityMetrics Report not found :/"
        logger.warning(
            f"Error deleting the report with id '{obesity_metrics_id}', {error_msg}"
        )
        return {"message": error_msg}, 404
    else:
        session.delete(obesity_metrics)
        session.commit()
        logger.debug(f"Deleting obesity metrics report with id#{obesity_metrics_id}")
        return {
            "message": f"Obesity Metrics with id {obesity_metrics_id} was removed successfully!"
        }, 200