from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mangum import Mangum
import onnxruntime as ort
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this in production to restrict access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define input schema
class CarFeatures(BaseModel):
    Brand: str
    model: str
    Year: int
    kmDriven: float
    Transmission: str
    Owner: str
    FuelType: str

# Load ONNX model with error handling
try:
    model_path = os.path.join("model", "model.onnx")
    session = ort.InferenceSession(model_path)
    input_names = [input.name for input in session.get_inputs()]
    output_names = [output.name for output in session.get_outputs()]
except Exception as e:
    session = None
    print(f"Error loading model: {e}")

@app.post("/predict")
def predict_price(car: CarFeatures):
    if session is None:
        raise HTTPException(status_code=500, detail="Model is not loaded.")

    try:
        Age = 2025 - car.Year

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

        filtered_input = {name: input_dict[name] for name in input_dict if name in input_names}

        prediction = session.run(output_names, filtered_input)
        predicted_price = float(prediction[0][0])

        return {"predicted_price_in_inr": round(predicted_price, 2)}
    
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing or unexpected input feature: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")

# AWS Lambda compatibility
handler = Mangum(app)

# For local testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
