from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import joblib
import pandas as pd
from fastapi.staticfiles import StaticFiles

# Cargar el modelo/pipeline completo
model = joblib.load('pipeline_model.pkl')  # Asegúrate de tener el pipeline completo aquí

# Crear la app
app = FastAPI(title="Spaceship Titanic Predictor")

# Montar la carpeta "static"
app.mount("/static", StaticFiles(directory="static"), name="static")

# Directorio de templates HTML
templates = Jinja2Templates(directory="templates")

# Ruta de prueba: muestra el formulario
@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

# Ruta para procesar el formulario
@app.post("/predict_form", response_class=HTMLResponse)
async def predict_form(
    request: Request,
    PassengerId: str = Form(...),
    HomePlanet: str = Form(...),
    CryoSleep: str = Form(...),
    Age: float = Form(...),
    VIP: str = Form(...),
    RoomService: float = Form(...),
    FoodCourt: float = Form(...),
    ShoppingMall: float = Form(...),
    Spa: float = Form(...),
    VRDeck: float = Form(...)
):
    # Convertir cadenas "true"/"false" a booleanos
    CryoSleep_bool = CryoSleep.lower() == 'true'
    VIP_bool = VIP.lower() == 'true'
    
    # Estructurar el dataframe con todos los datos (incluyendo PassengerId porque el modelo lo usa)
    input_data = pd.DataFrame([{
        "PassengerId": PassengerId,
        "HomePlanet": HomePlanet,
        "CryoSleep": CryoSleep_bool,
        "Age": Age,
        "VIP": VIP_bool,
        "RoomService": RoomService,
        "FoodCourt": FoodCourt,
        "ShoppingMall": ShoppingMall,
        "Spa": Spa,
        "VRDeck": VRDeck
    }])

    # Hacemos la predicción directamente, sin eliminar PassengerId
    try:
        prediction = model.predict(input_data)
        result = "Transported" if prediction[0] else "Not Transported"
    except Exception as e:
        result = f"Error en la predicción: {e}"
        
    # Mostrar el resultado en el HTML
    return templates.TemplateResponse("form.html", {
        "request": request,
        "result": result,
        "passenger_id": PassengerId
    })