from fastapi import FastAPI
from pydantic import BaseModel
from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel
from pyspark.sql.functions import lit
import os

from fastapi.middleware.cors import CORSMiddleware

# Initialize Spark session
spark = SparkSession.builder.appName("CarPriceAPI").getOrCreate()

# Load trained Spark ML pipeline model
model_path = os.path.join("model", "saved_model")
model = PipelineModel.load(model_path)

# Create FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Define input schema using Pydantic
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
    # Calculate Age from Year (same logic as in training)
    Age = 2025 - car.Year

    # Create a DataFrame for prediction
    input_data = [{
        "Brand": car.Brand,
        "model": car.model,
        "Year": car.Year,
        "Age": Age,
        "kmDriven": car.kmDriven,
        "Transmission": car.Transmission,
        "Owner": car.Owner,
        "FuelType": car.FuelType
    }]
    
    input_df = spark.createDataFrame(input_data)

    # Apply pipeline model to make prediction
    prediction = model.transform(input_df)
    predicted_price = prediction.select("prediction").first()[0]

    # Return result as JSON
    return {
        "predicted_price_in_inr": round(predicted_price, 2)
    }

# For local testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("model.main:app", host="0.0.0.0", port=5001, reload=True)
