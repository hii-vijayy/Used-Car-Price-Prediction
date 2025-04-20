from fastapi import FastAPI
from pydantic import BaseModel
from mangum import Mangum
import onnxruntime as ort
import numpy as np
from fastapi.middleware.cors import CORSMiddleware

# Load the ONNX model
session = ort.InferenceSession("model/model.onnx")
input_names = [input.name for input in session.get_inputs()]
output_names = [output.name for output in session.get_outputs()]

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
    # Calculate Age (same as in training)
    Age = 2025 - car.Year
    
    # Prepare input data in the format expected by ONNX
    input_dict = {
        'Brand': np.array([car.Brand]).reshape(-1, 1),
        'model': np.array([car.model]).reshape(-1, 1),
        'Year': np.array([car.Year], dtype=np.float32).reshape(-1, 1),
        'Age': np.array([Age], dtype=np.float32).reshape(-1, 1),
        'kmDriven': np.array([car.kmDriven], dtype=np.float32).reshape(-1, 1),
        'Transmission': np.array([car.Transmission]).reshape(-1, 1),
        'Owner': np.array([car.Owner]).reshape(-1, 1),
        'FuelType': np.array([car.FuelType]).reshape(-1, 1)
    }
    
    # Filter to only include required inputs based on the model
    filtered_input = {name: input_dict[name] for name in input_dict if name in input_names}
    
    # Make prediction
    prediction = session.run(output_names, filtered_input)
    predicted_price = float(prediction[0][0])
    
    return {"predicted_price_in_inr": round(predicted_price, 2)}

# AWS Lambda handler
handler = Mangum(app)

# For local testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)