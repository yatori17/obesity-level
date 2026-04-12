---

# 🩺 Obesity Level Predictor — MVP

Este projeto consiste em um sistema inteligente para a predição do nível de obesidade de indivíduos com base em seus hábitos alimentares e características físicas. O projeto integra um modelo de **Machine Learning** (treinado via Scikit-Learn), uma **API REST** (Flask) e uma interface responsiva (**Frontend**).

---

## 📁 Estrutura do Projeto

* **`Obesity_Model_.ipynb`**: Notebook contendo todo o processo de criação do modelo de machine learning (Carga, Separação entre treino e teste (*holdout*), Pré-processamento, Validação Cruzada, Otimização e Exportação do Modelo).
* **`ObesityDataSet_raw_and_data_sinthetic.csv`**: Base de dados utilizada para o treinamento.
* **`api/`**: Backend em Python (Flask) que serve o modelo preditivo.
    * `app.py`: Ponto de entrada da API.
    * `model/`: Contém o arquivo `.pkl` exportado e o modelo do banco de dados da aplicação.
    * `services/`: Lógica de processamento e predição.
    * `test_api.py`: Testes automatizados da API.
* **`frontend/`**: Interface web para interação com o usuário.

---

## 🚀 Como Executar

### 1. Backend (API)
Navegue até a pasta da API e configure o ambiente:

```bash
cd api
python -m venv venv
source venv/bin/activate  # (No Windows: venv\Scripts\activate)
pip install -r requirements.txt
flask run --host 0.0.0.0 --port 5000 --reload
```
> A API estará disponível em: `http://localhost:5000`

### 2. Frontend
Basta abrir o arquivo `index.html` (ou o comando de execução do seu framework) na pasta `frontend`. 

> **Nota:** Certifique-se de que a API esteja rodando para que as predições funcionem corretamente.

---

## 🧪 Testes Automatizados

Foram implementados testes automatizados para garantir a integridade da API e a precisão das predições. Os testes cobrem as chamadas da API, validações e também desde a carga do modelo até o processamento dos dados de entrada.

**Para rodar os testes:**

```bash
cd api
python -m pytest -v ./tests/test_predictor.py
```

*Os testes verificam se o modelo responde corretamente a entradas válidas e se lida adequadamente com dados inconsistentes.*

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.x
* **Machine Learning:** Scikit-Learn (Algoritmo CART / Decision Tree)
* **Processamento de Dados:** Pandas & Numpy
* **Backend:** Flask
* **Frontend:** HTML / CSS / JS

---

## 🛡️ Considerações de Segurança

O projeto segue boas práticas de **Software Seguro**, como a separação de responsabilidades, sanitização de entradas no backend e anonimização de dados sensíveis durante o treinamento do modelo, conforme preconizado na disciplina.

---