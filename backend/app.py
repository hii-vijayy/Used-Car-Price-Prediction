import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from pyspark.ml import PipelineModel
from pyspark.sql import SparkSession

app = Flask(__name__)
CORS(app)

# Initialize Spark
spark = SparkSession.builder.appName("CarPriceAPI").getOrCreate()

# Load model
model_path = "/Users/vijaykumar/Programming/React_JS_Projects/Used-Car-Price-Prediction/backend/saved_model"  # Adjusted path
model = PipelineModel.load(model_path)

@app.route('/predict', methods=['POST'])
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
    app.run(host='0.0.0.0', port=5001, debug=True)
