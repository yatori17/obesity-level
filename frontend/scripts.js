async function predictObesityMetrics(obesityMetrics) {
    const formData = new FormData();

    formData.append("name", obesityMetrics.name);
    formData.append("gender", obesityMetrics.gender);
    formData.append("age", obesityMetrics.age);
    formData.append("height", obesityMetrics.height);
    formData.append("weight", obesityMetrics.weight);
    formData.append("family_history", obesityMetrics.family_history);
    formData.append("high_caloric_intake", obesityMetrics.high_caloric_intake);
    formData.append("vegetable_consumption", obesityMetrics.vegetable_consumption);
    formData.append("daily_meals_count", obesityMetrics.daily_meals_count);
    formData.append("food_between_meals", obesityMetrics.food_between_meals);
    formData.append("is_smoker", obesityMetrics.is_smoker);
    formData.append("daily_water_intake", obesityMetrics.daily_water_intake);
    formData.append("calorie_monitoring", obesityMetrics.calorie_monitoring);
    formData.append("physical_activity_frequency", obesityMetrics.physical_activity_frequency);
    formData.append("tech_usage_time", obesityMetrics.tech_usage_time);
    formData.append("alcohol_consumption", obesityMetrics.alcohol_consumption);
    formData.append("transportation_mode", obesityMetrics.transportation_mode);

    try {
        const response = await fetch(baseUrl + "/obesity-metrics", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || "Error processing the reqest");
        }
        return await response.json();
    } catch (err) {
        console.error("Error in the request:", err);
        throw err;
    }
}

async function getObesityMetricsById(id) {
    const res = await fetch(`${baseUrl}/obesity-metrics/${id}`);
    const data = await res.json();
    openObesityMetricsDetail(data);
}


const newPrediction = async (event) => {
    event.preventDefault();
    const patientData = {
        name: document.getElementById("name").value,
        gender: document.getElementById("gender").value,
        age: parseFloat(document.getElementById("age").value),
        height: parseFloat(document.getElementById("height").value),
        weight: parseFloat(document.getElementById("weight").value),
        family_history: document.getElementById("family_history_with_overweight").value,
        high_caloric_intake: document.getElementById("FAVC").value,
        vegetable_consumption: parseFloat(document.getElementById("FCVC").value),
        daily_meals_count: parseFloat(document.getElementById("NCP").value),
        calorie_monitoring: document.getElementById("SCC").value,
        daily_water_intake: parseFloat(document.getElementById("CH2O").value),
        physical_activity_frequency: parseFloat(document.getElementById("FAF").value),
        tech_usage_time: parseFloat(document.getElementById("TUE").value),
        alcohol_consumption: document.getElementById("CALC").value,
        transportation_mode: document.getElementById("MTRANS").value,
        is_smoker: document.getElementById("SMOKE").value,
        food_between_meals: parseFloat(document.getElementById("CAEC").value)
    };

    try {
        const result = await predictObesityMetrics(patientData);

        const fieldsToClear = [
            "name", "gender", "age", "height", "weight", "family_history_with_overweight",
            "FAVC", "FCVC", "NCP", "SCC", "CH2O", "FAF", "TUE", "CALC", "MTRANS", "SMOKE"
        ];
        fieldsToClear.forEach(id => document.getElementById(id).value = "");

        alert(`Resultado: ${translations[result.obesity_level]}`);

        await getList()

    } catch (error) {
        console.error("Erro ao processar predição:", error);
        alert("Erro ao processar predição: " + error);
    }
}


const getList = async (name = '') => {
    let url = baseUrl + '/obesity-metrics';
    if (name) {
        url += "?name=" + name;
    }
    fetch(url, {
        method: 'get',
    })
        .then((response) => response.json())
        .then((data) => {
            const corpoTabela = document.getElementById('corpoTabela');
            corpoTabela.innerHTML = '';
            data.obesity_metrics_list.forEach(item => {
                insertList(item)
            });
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

const deleteItem = (id) => {
    if (confirm("Você tem certeza que deseja excluir este registro?")) {
        let url = baseUrl + `/obesity-metrics?id=${id}`;
        fetch(url, {
            method: 'delete'
        })
            .then((response) => {
                if (response.ok) {
                    alert("Registro removido!");
                    getList(); // Recarrega a tabela
                }
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }
}
getList();

const insertList = (item) => {
    const corpoTabela = document.getElementById('corpoTabela');
    let line = corpoTabela.insertRow();

    line.insertCell(0).innerHTML = item.name;

    const imc = (item.weight / (item.height * item.height)).toFixed(1);
    line.insertCell(1).innerHTML = `${item.weight}kg (${imc})`;

    line.insertCell(2).innerHTML = item.family_history ? "Sim" : " Não";

    const fafMap = ["Nunca", "Raramente", "Frequentemente", "Sempre"];
    line.insertCell(3).innerHTML = fafMap[Math.round(item.physical_activity_frequency)] || "N/A";

    line.insertCell(4).innerHTML = translations[item.alcohol_consumption] || item.alcohol_consumption;

    const cellLevel = line.insertCell(5);
    const obesity_level = translations[item.obesity_level] || item.obesity_level;
    cellLevel.innerHTML = `<span>${obesity_level}</span>`;
    cellLevel.className = "obesity-tag";
    let icon = document.createElement('i');
    icon.className = "fa-solid fa-trash-can";
    let btnDelete = document.createElement('button');
    btnDelete.innerHTML = "";
    btnDelete.appendChild(icon);
    btnDelete.className = "btn-delete";
    btnDelete.onclick = () => deleteItem(item.id);
    let iconView = document.createElement('i');
    iconView.className = "fa-solid fa-eye";

    let btnView = document.createElement('button');
    btnView.className = "btn-view";
    btnView.appendChild(iconView);

    btnView.onclick = () => getObesityMetricsById(item.id);

    let actionCell = line.insertCell(6);
    actionCell.appendChild(btnView);
    actionCell.appendChild(btnDelete);
}


const openObesityMetricsDetail = (item) => {

    const corpoModal = document.getElementById('detalhesCorpo');

    const fafTraduzido = item.physical_activity_frequency >= 2 ? "Frequente (Atleta)" :
        (item.physical_activity_frequency >= 1 ? "Moderada" : "Sedentário");
    const aguaMap = {
        "1": "Menos de 1 Litro",
        "2": "1 a 2 Litros",
        "3": "Mais de 2 Litros"
    };

    const fcvcMap = {
        "1": "Nunca consome vegetais",
        "2": "Consome às vezes",
        "3": "Consome sempre (em todas as refeições)"
    };

    const timeOnScreenMap = {
        "0": "0-2 horas",
        "1": "3 - 5 horas",
        "3": "Mais de 5 horas"
    };

    const waterConsuptionTranslated = aguaMap[item.daily_water_intake] || item.daily_water_intake

    const vegetableConsumption = fcvcMap[item.vegetable_consumption] || item.vegetable_consumption

    const timeOnScreen = timeOnScreenMap[item.tech_usage_time] || item.tech_usage_time

    corpoModal.innerHTML = `
        <div class="detail-item">
            <strong><i class="fas fa-id-card"></i> Paciente</strong>
            <span>${item.name} (${item.gender})</span>
        </div>
        <div class="detail-item">
            <strong><i class="fas fa-calendar-alt"></i> Idade</strong>
            <span>${item.age} anos</span>
        </div>
        <div class="detail-item">
            <strong><i class="fas fa-ruler-vertical"></i> Altura / Peso</strong>
            <span>${item.height}m / ${item.weight}kg</span>
        </div>
        <div class="detail-item">
            <strong><i class="fas fa-users"></i> Histórico Familiar</strong>
            <span>${translate(item.family_history)}</span>
        </div>
        <div class="detail-item">
            <strong><i class="fas fa-dumbbell"></i> Atividade Física</strong>
            <span>${fafTraduzido}</span>
        </div>
        <div class="detail-item">
            <strong><i class="fa-solid fa-droplet"></i> Consumo de Água</strong>
            <span>${waterConsuptionTranslated}</span>
        </div>
        <div class="detail-item">
            <strong><i class="fas fa-utensils"></i> Refeições Diárias</strong>
            <span>${item.daily_meals_count}</span>
        </div>
        <div class="detail-item">
            <strong><i class="fas fa-hamburger"></i> Comida calórica frequente</strong>
            <span>${translate(item.high_caloric_intake)}</span>
        </div>

        <div class="detail-item">
            <strong><i class="fas fa-weight-hanging"></i> Monitora Calorias</strong>
            <span>${translate(item.calorie_monitoring)}</span>
        </div>

        <div class="detail-item">
            <strong><i class="fas fa-leaf"></i> Vegetais nas refeiões</strong>
            <span>${vegetableConsumption}</span>
        </div>
        <div class="detail-item">
            <strong><i class="fas fa-cookie-bite"></i> Lanches entre refeições</strong>
            <span>${translate(item.food_between_meals)}</span>
        </div>

        <div class="detail-item">
            <strong><i class="fas fa-desktop"></i> Tempo em tela</strong>
            <span>${timeOnScreen}</span>
        </div>
        
        <div class="detail-item">
            <strong><i class="fas fa-glass-cheers"></i> Bebida alcoolica</strong>
            <span>${translate(item.alcohol_consumption)}</span>
        </div>

        <div class="detail-item">
            <strong><i class="fas fa-smoking"></i> Fuma</strong>
            <span>${translate(item.is_smoker)}</span>
        </div>
        <div class="detail-item">
            <strong><i class="fas fa-bus"></i> Meio de Transporte</strong>
            <span>${translate(item.transportation_mode)}</span>
        </div>
        <div class="detail-item" style="grid-column: span 2; margin-top: 15px; padding-top: 15px; border-top: 1px dashed #ddd;">
            <strong><i class="fas fa-stethoscope"></i> Resultado da Predição de Obesidade</strong>
            <span class="badge" style="font-size: 1.1rem; display: block; margin-top: 5px;">
                ${translate(item.obesity_level)}
            </span>
        </div>
    `;

    document.getElementById('modalDetalhes').style.display = 'block';
}

const closeModal = () => {
    document.getElementById('modalDetalhes').style.display = 'none';
}

window.onclick = function (event) {
    const modal = document.getElementById('modalDetalhes');
    if (event.target == modal) {
        closeModal();
    }
}

function translate(value) {
    if (value == null) {
        return 'N/A';
    }
    return translations[value] ? translations[value] : value;
}

const formInputs = document.querySelectorAll('input[required], select[required]');
const btnPredict = document.getElementById('btn-predict');

const validateForm = () => {
    let allValid = true;

    formInputs.forEach(input => {
        const errorSpan = document.getElementById(`error-${input.id}`);
        
        if (!input.value || input.value === "") {
            allValid = false;
            if (input.dataset.touched) {
                if (errorSpan) errorSpan.style.display = 'block';
                input.style.borderColor = '#ef4444';
            }
        } else {
            if (errorSpan) errorSpan.style.display = 'none';
            input.style.borderColor = '#e2e8f0';
        }
    });

    btnPredict.disabled = !allValid;
};

formInputs.forEach(input => {
    input.addEventListener('input', () => {
        input.dataset.touched = "true";
        validateForm();
    });
    
    input.addEventListener('blur', () => {
        input.dataset.touched = "true";
        validateForm();
    });
});

function handleSearch() {
    const searchTerm = document.getElementById('searchInput').value;
    getList(searchTerm);
}

document.getElementById('searchInput')?.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        handleSearch();
    }
});