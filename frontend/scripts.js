async function getAlbuns(params = new URLSearchParams()) {
    try {
        const url = params.toString()
            ? `${baseUrl}/obesity-metrics?${params.toString()}`
            : `${baseUrl}/obesity-metrics`;

        const res = await fetch(url);

        if (!res.ok) {
            throw new Error("Failed to load obesity-metrics report");
        }

        const data = await res.json();
        return data.obesity - metrics || [];

    } catch (err) {
        console.error(err);
        return [];
    }
}

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


const newPrediction = async (event) => {
    event.preventDefault();

    /* Captura os valores dos inputs e organiza em um objeto 
     seguindo o mapeamento do nosso ObesityMetricsSchema
  */
    const patientData = {
        gender: document.getElementById("gender").value,
        age: parseFloat(document.getElementById("age").value),
        height: parseFloat(document.getElementById("height").value),
        weight: parseFloat(document.getElementById("weight").value),
        family_history: document.getElementById("family_history_with_overweight").value === "yes",
        high_caloric_intake: document.getElementById("FAVC").value === "yes",
        vegetable_consumption: parseFloat(document.getElementById("FCVC").value),
        daily_meals_count: parseFloat(document.getElementById("NCP").value),
        calorie_monitoring: document.getElementById("SCC").value === "yes",
        daily_water_intake: parseFloat(document.getElementById("CH2O").value),
        physical_activity_frequency: parseFloat(document.getElementById("FAF").value),
        tech_usage_time: parseFloat(document.getElementById("TUE").value),
        alcohol_consumption: document.getElementById("CALC").value,
        transportation_mode: document.getElementById("MTRANS").value,
        is_smoker: document.getElementById("SMOKE").value === "yes",
        food_between_meals: parseFloat(document.getElementById("CAEC").value)
    };

    try {
        // Agora passamos apenas o objeto 'patientData'
        const result = await predictObesityMetrics(patientData);

        // Limpeza dos campos após o sucesso (usando seus IDs de input)
        const fieldsToClear = [
            "gender", "age", "height", "weight", "family_history_with_overweight",
            "FAVC", "FCVC", "NCP", "SCC", "CH2O", "FAF", "TUE", "CALC", "MTRANS", "SMOKE"
        ];
        fieldsToClear.forEach(id => document.getElementById(id).value = "");

        alert(`Resultado: ${result.obesity_level}`);

    } catch (error) {
        console.error("Erro ao processar predição:", error);
    }
}
