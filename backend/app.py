import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from pyspark.ml import PipelineModel
from pyspark.sql import SparkSession
import tempfile

app = Flask(__name__)
CORS(app)

# Configure Spark for container environment
os.environ['PYSPARK_SUBMIT_ARGS'] = '--driver-memory 1g pyspark-shell'

# Set a specific temp directory with permissions
temp_dir = tempfile.mkdtemp()
os.environ['SPARK_LOCAL_DIRS'] = temp_dir

# Initialize Spark with proper config
spark = SparkSession.builder \
    .appName("CarPriceAPI") \
    .config("spark.driver.host", "localhost") \
    .config("spark.driver.bindAddress", "0.0.0.0") \
    .config("spark.executor.memory", "1g") \
    .config("spark.driver.memory", "1g") \
    .config("spark.python.worker.memory", "512m") \
    .config("spark.local.dir", temp_dir) \
    .config("spark.sql.warehouse.dir", os.path.join(temp_dir, "spark-warehouse")) \
    .getOrCreate()

# Load model - adjust the path to where it's mounted in the container
model_path = os.environ.get("MODEL_PATH", "/app/saved_model")
model = PipelineModel.load(model_path)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    print("Received data:", data)
    try:
        features = spark.createDataFrame(
            [[
                data.get('brand'),
                data.get('model'),
                data.get('year'),
                data.get('fuel'),
                data.get('transmission'),
                data.get('kms_driven')
            ]],
            schema=(
                'Brand string, Model string, Year int, '
                'Fuel string, Transmission string, kmDriven int'
            )
        )
        features.show()  # debug: prints input to verify
        prediction = model.transform(features).first().prediction
        return jsonify({
            'price': round(prediction, 2),
            'input': data
        })
    except Exception as e:
        print("Prediction error:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))  # default to 5001 if not set
    app.run(host='0.0.0.0', port=port)