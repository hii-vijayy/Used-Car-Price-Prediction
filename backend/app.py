"""
Car Price Prediction API
Endpoint: /predict (POST)
Handles Spark-based price predictions for used cars.
"""

import os
import tempfile
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from pyspark.ml import PipelineModel
from pyspark.sql import SparkSession, Row
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
import findspark  # Import findspark

# Initialize findspark before SparkSession
findspark.init()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
# CORS(app)

CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
# Create a temp directory with proper permissions
temp_dir = tempfile.mkdtemp()
os.environ['SPARK_LOCAL_DIRS'] = temp_dir

# Define the schema for the input data
PREDICTION_SCHEMA = StructType([
    StructField("brand", StringType(), nullable=False),
    StructField("model", StringType(), nullable=False),
    StructField("year", IntegerType(), nullable=False),
    StructField("fuel", StringType(), nullable=False),
    StructField("transmission", StringType(), nullable=False),
    StructField("kms_driven", IntegerType(), nullable=False)
])

def initialize_spark():
    """Initialize and configure Spark session with production settings."""
    logger.info("Initializing Spark Session...")
    
    return SparkSession.builder \
        .appName("CarPriceAPI") \
        .config("spark.driver.memory", os.getenv("DRIVER_MEMORY", "2g")) \
        .config("spark.executor.memory", os.getenv("EXECUTOR_MEMORY", "2g")) \
        .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
        .config("spark.submit.deployMode", "client") \
        .config("spark.ui.showConsoleProgress", "false") \
        .config("spark.driver.extraJavaOptions", "-XX:+UseG1GC") \
        .config("spark.sql.warehouse.dir", os.path.join(temp_dir, "spark-warehouse")) \
        .master("local[1]") \
        .getOrCreate()

# Initialize Spark
spark = initialize_spark()

# Load ML model
def load_model():
    """Load the trained PySpark ML model."""
    logger.info("Loading ML model...")
    model_path = os.getenv("MODEL_PATH", "./saved_model")
    try:
        pipeline_model = PipelineModel.load(model_path)  # renamed from `model`
        logger.info("Model loaded successfully")
        return pipeline_model
    except Exception as load_error:
        logger.error("Model loading failed: %s", str(load_error))
        raise RuntimeError("Model initialization failed") from load_error

ml_model = load_model()  # renamed from `model`

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for deployment validation."""
    return jsonify({
        "status": "healthy",
        "spark_status": "active" if spark else "inactive",
        "model_loaded": bool(ml_model)
    })

@app.route('/predict', methods=['OPTIONS'])
def options_predict():
    return '', 204


@app.route('/predict', methods=['POST'])
def predict_price():
    """Main prediction endpoint
    
    Expects JSON payload with car features:
    {
        "brand": "Toyota",
        "model": "Corolla",
        "year": 2018,
        "fuel": "Petrol",
        "transmission": "Manual",
        "kms_driven": 45000
    }
    """
    try:
        data = request.json
        logger.info("Received prediction request: %s", data)
        
        # Validate input data
        required_fields = ['brand', 'model', 'year', 'fuel', 'transmission', 'kms_driven']
        if not all(field in data for field in required_fields):
            raise ValueError("Missing required fields in input data")

        # Create Spark DataFrame
        features = spark.createDataFrame([
            Row(
                brand=data['brand'],
                model=data['model'],
                year=int(data['year']),
                fuel=data['fuel'],
                transmission=data['transmission'],
                kms_driven=int(data['kms_driven'])
            )
        ], schema=PREDICTION_SCHEMA)

        # Make prediction
        prediction = ml_model.transform(features).first().prediction

        return jsonify({
            "price": round(float(prediction), 2),
            "currency": "INR",
            "confidence": 0.95  # Example value
        })
    
    except ValueError as ve:
        logger.error("Validation error: %s", ve)
        return jsonify({"error": str(ve)}), 400
    except Exception as e:  # pylint: disable=broad-except
        logger.error("Prediction failed: %s", e)
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    port = int(os.getenv("PORT", "5001"))  # default value as string
    logger.info("Starting application on port %d", port)
    app.run(host='0.0.0.0', port=port)
