import pytest
import json
from app import app
from model import Session, ObesityMetrics


@pytest.fixture
def client():
    """Configura o cliente de teste para a aplicação Flask"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def sample_metrics_data():
    """Dados de exemplo baseados no caso do Leonardo Andrade"""
    return {
        "name": "Leonardo Teste API",
        "gender": "Masculino",
        "age": 29,
        "height": 1.73,
        "weight": 84.0,
        "family_history": False,
        "high_caloric_intake": False,
        "vegetable_consumption": 3,
        "daily_meals_count": 4.0,
        "food_between_meals": "2",
        "is_smoker": False,
        "daily_water_intake": 1.5,
        "calorie_monitoring": False,
        "physical_activity_frequency": 1.0,
        "tech_usage_time": 1.0,
        "alcohol_consumption": "Frequently",
        "transportation_mode": "Public_Transportation"
    }

def test_home_redirect(client):
    """Testa se a rota "/" redireciona para o frontend"""
    response = client.get('/')
    assert response.status_code == 302
    assert '/frontend/index.html' in response.location

def test_add_obesity_prediction(client, sample_metrics_data):
    """Testa a criação de um registro e a predição do modelo"""
    session = Session()
    session.query(ObesityMetrics).filter(ObesityMetrics.name == sample_metrics_data['name']).delete()
    session.commit()
    session.close()

    response = client.post('/obesity-metrics', data=sample_metrics_data)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert data['name'] == sample_metrics_data['name']
    assert data['weight'] == sample_metrics_data['weight']
    
    assert 'obesity_level' in data
    assert isinstance(data['obesity_level'], str)
    assert len(data['obesity_level']) > 0

def test_get_metrics_list(client, sample_metrics_data):
    """Testa a listagem de todos os registros"""
    res_post = client.post('/obesity-metrics', data=sample_metrics_data)
    assert res_post.status_code == 200    
    response = client.get('/obesity-metrics')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'obesity_metrics_list' in data
    assert isinstance(data['obesity_metrics_list'], list)

def test_get_metrics_by_name(client, sample_metrics_data):
    """Testa a busca filtrada por nome"""
    res_post = client.post('/obesity-metrics', data=sample_metrics_data)
    assert res_post.status_code == 200
    name = sample_metrics_data['name']
    response = client.get(f'/obesity-metrics?name={name}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'obesity_metrics_list' in data
    
    assert data['obesity_metrics_list'][0]['name'] == name

def test_delete_obesity_metrics(client, sample_metrics_data):
    """Testa a remoção pelo ID correto"""
    res_post = client.post('/obesity-metrics', data=sample_metrics_data)
    assert res_post.status_code == 200
    
    data = json.loads(res_post.data)
    id_to_delete = data["id"]
    
    response = client.delete(f'/obesity-metrics?id={id_to_delete}')
    assert response.status_code == 200
    assert "removed successfully" in response.json['message']
    
def test_cleanup_database():
    """Limpa os registros criados durante os testes"""
    session = Session()
    session.query(ObesityMetrics).filter(
        ObesityMetrics.name.ilike('%Teste API%')
    ).delete(synchronize_session=False)
    session.commit()
    session.close()