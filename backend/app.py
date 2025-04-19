import os
import tempfile
import logging
import datetime
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from pyspark.ml import PipelineModel
from pyspark.sql import SparkSession, Row
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
import findspark  # Import findspark

# Initialize findspark before SparkSession
findspark.init()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# More specific CORS configuration
CORS(app, 
     resources={r"/*": {"origins": ["http://localhost:5173", "http://localhost:5001", "https://your-frontend-domain.com"]}},
     supports_credentials=True,
     methods=["GET", "POST", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization"],
     expose_headers=["Content-Type", "X-Total-Count"])

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

    spark = SparkSession.builder \
        .appName("CarPriceAPI") \
        .config("spark.driver.memory", os.getenv("DRIVER_MEMORY", "1g")) \
        .config("spark.executor.memory", os.getenv("EXECUTOR_MEMORY", "1g")) \
        .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
        .config("spark.submit.deployMode", "client") \
        .config("spark.ui.showConsoleProgress", "false") \
        .config("spark.driver.extraJavaOptions", "-XX:+UseG1GC -XX:MaxHeapFreeRatio=50") \
        .config("spark.sql.warehouse.dir", os.path.join(temp_dir, "spark-warehouse")) \
        .config("spark.memory.fraction", "0.6") \
        .config("spark.memory.storageFraction", "0.5") \
        .master("local[1]") \
        .getOrCreate()

    # Set log level to reduce noise
    spark.sparkContext.setLogLevel("WARN")
    
    logger.info(f"Spark version: {spark.version}")
    logger.info(f"Spark app name: {spark.sparkContext.appName}")
    return spark

# Initialize Spark
spark = initialize_spark()

# Load ML model
def load_model():
    """Load the trained PySpark ML model."""
    logger.info("Loading ML model...")

    # Fix path: default is now backend/saved_model
    model_path = os.getenv("MODEL_PATH", "backend/saved_model")

    if not os.path.exists(model_path):
        logger.error("Model path does not exist: %s", model_path)
        logger.info("Checking current directory for model...")
        # Try alternative paths
        alternative_paths = ["saved_model", "./saved_model", "../saved_model"]
        for alt_path in alternative_paths:
            if os.path.exists(alt_path):
                logger.info(f"Found model at alternative path: {alt_path}")
                model_path = alt_path
                break
        else:
            raise FileNotFoundError(f"Model not found at {model_path} or alternative locations")

    try:
        pipeline_model = PipelineModel.load(model_path)
        logger.info("Model loaded successfully")
        return pipeline_model
    except Exception as load_error:
        logger.error("Model loading failed: %s", str(load_error))
        raise RuntimeError("Model initialization failed") from load_error

# Try to load the model, with a fallback for simplified testing
try:
    ml_model = load_model()
except Exception as e:
    logger.warning(f"Failed to load model: {str(e)}. Running in test mode.")
    ml_model = None

@app.route('/health', methods=['GET'])
def health_check():
    """Enhanced health check endpoint for deployment validation."""
    try:
        # Test Spark connection
        spark_active = False
        try:
            # Simple Spark operation to verify it's functioning
            spark.sql("SELECT 1").collect()
            spark_active = True
        except Exception as spark_error:
            logger.error(f"Spark health check failed: {str(spark_error)}")
        
        # Test model
        model_loaded = False
        try:
            # Check if model is accessible
            model_loaded = ml_model is not None
        except Exception as model_error:
            logger.error(f"Model health check failed: {str(model_error)}")
            
        status_code = 200 if spark_active and model_loaded else 503
        
        return jsonify({
            "status": "healthy" if spark_active and model_loaded else "unhealthy",
            "spark_status": "active" if spark_active else "inactive",
            "model_loaded": model_loaded,
            "environment": os.getenv("FLASK_ENV", "production"),
            "timestamp": datetime.now().isoformat()
        }), status_code
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 503

@app.route('/predict', methods=['OPTIONS'])
def options_predict():
    """Handle CORS preflight for prediction endpoint."""
    response = app.make_default_options_response()
    return response

@app.route('/predict', methods=['POST'])
def predict_price():
    """Main prediction endpoint"""
    try:
        # Check if the request has valid JSON content
        if not request.is_json:
            logger.error("Invalid request format: not JSON")
            return jsonify({"error": "Request must be JSON", "status": "error"}), 400
            
        data = request.json
        logger.info("Received prediction request: %s", data)

        # Validate input data
        required_fields = ['brand', 'model', 'year', 'fuel', 'transmission', 'kms_driven']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            error_msg = f"Missing required fields: {', '.join(missing_fields)}"
            logger.error(error_msg)
            return jsonify({"error": error_msg, "status": "error"}), 400

        # Type validation
        try:
            # Create validated data with proper types
            validated_data = {
                'brand': str(data['brand']),
                'model': str(data['model']),
                'year': int(data['year']),
                'fuel': str(data['fuel']),
                'transmission': str(data['transmission']),
                'kms_driven': int(data['kms_driven'])
            }
        except (ValueError, TypeError) as type_error:
            logger.error(f"Type validation error: {str(type_error)}")
            return jsonify({"error": f"Invalid data types: {str(type_error)}", "status": "error"}), 400

        # Test mode for environments where model might not be available
        if ml_model is None:
            logger.warning("Model not available, returning mock prediction")
            # Return mock prediction for testing
            return jsonify({
                "price": 500000.00,  # Mock price
                "currency": "INR",
                "status": "success",
                "note": "Test mode - actual model not loaded"
            })

        # Create Spark DataFrame
        features = spark.createDataFrame([Row(**validated_data)], schema=PREDICTION_SCHEMA)

        # Make prediction with timeout handling
        prediction = ml_model.transform(features).first().prediction

        return jsonify({
            "price": round(float(prediction), 2),
            "currency": "INR",
            "status": "success"
        })

    except ValueError as ve:
        logger.error("Validation error: %s", ve)
        return jsonify({"error": str(ve), "status": "error"}), 400
    except Exception as e:
        logger.exception("Prediction failed")  # This logs the full stack trace
        return jsonify({"error": f"Server error: {str(e)}", "status": "error"}), 500

# Simple test endpoint that doesn't require Spark or the model
@app.route('/test', methods=['GET'])
def test_endpoint():
    """Test endpoint that always works"""
    return jsonify({
        "status": "ok",
        "message": "API is running",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    port = int(os.getenv("PORT", "5001"))
    logger.info(f"🔥 Starting application on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)