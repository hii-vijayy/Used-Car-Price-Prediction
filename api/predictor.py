from fastapi import FastAPI
from pydantic import BaseModel
from mangum import Mangum
import joblib
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware

# Load the trained model pipeline (includes all preprocessing)
model = joblib.load("model/saved_model/sklearn_model.joblib")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can set this to your frontend URL for better security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define input structure (matches training data schema)
class CarFeatures(BaseModel):
    Brand: str
    model: str
    Year: int
    kmDriven: float
    Transmission: str
    Owner: str
    FuelType: str

@app.post("/predict")
def predict_price(car: CarFeatures):
    # Create input DataFrame with same structure as training data
    input_data = pd.DataFrame([{
        "Brand": car.Brand,
        "model": car.model,
        "Year": car.Year,
        "kmDriven": car.kmDriven,
        "Transmission": car.Transmission,
        "Owner": car.Owner,
        "FuelType": car.FuelType
    }])
    
    # Calculate Age (same as training)
    input_data['Age'] = 2025 - input_data['Year']
    
    # Let the model pipeline handle all preprocessing
    predicted_price = model.predict(input_data)[0]
    
    return {"predicted_price_in_inr": round(predicted_price, 2)}

# AWS Lambda handler
handler = Mangum(app)
