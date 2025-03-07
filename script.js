document.getElementById("predictionForm").addEventListener("submit", async function(event) {
    event.preventDefault();
    
    const input1 = document.getElementById("input1").value;
    const input2 = document.getElementById("input2").value;
    
    const resultElement = document.getElementById("result");
    resultElement.textContent = "Obteniendo predicción...";
    
    try {
        const response = await fetch("https://prediction-f2cq.onrender.com/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ input1, input2 })
        });
        
        if (!response.ok) {
            throw new Error("Error en la respuesta del servidor");
        }
        
        const data = await response.json();
        resultElement.textContent = `Predicción: ${data.prediction}`;
    } catch (error) {
        resultElement.textContent = "Error al obtener la predicción.";
        console.error("Error:", error);
    }
});
