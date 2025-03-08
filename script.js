document.getElementById("predictionForm").addEventListener("submit", async function(event) {
    event.preventDefault();
    
    const data = {
        HomePlanet: document.getElementById("HomePlanet").value,
        CryoSleep: document.getElementById("CryoSleep").value.toLowerCase() === "true",
        Age: parseFloat(document.getElementById("Age").value),
        VIP: document.getElementById("VIP").value.toLowerCase() === "true",
        RoomService: parseFloat(document.getElementById("RoomService").value),
        FoodCourt: parseFloat(document.getElementById("FoodCourt").value),
        ShoppingMall: parseFloat(document.getElementById("ShoppingMall").value),
        Spa: parseFloat(document.getElementById("Spa").value),
        VRDeck: parseFloat(document.getElementById("VRDeck").value)
    };
    
    const resultElement = document.getElementById("result");
    resultElement.textContent = "Obteniendo predicción...";
    
    try {
        const response = await fetch("https://prediction-f2cq.onrender.com/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            throw new Error("Error en la respuesta del servidor");
        }
        
        const responseData = await response.json();
        resultElement.textContent = `Predicción de Transported: ${responseData.prediction}`;
    } catch (error) {
        resultElement.textContent = "Error al obtener la predicción.";
        console.error("Error:", error);
    }
});
