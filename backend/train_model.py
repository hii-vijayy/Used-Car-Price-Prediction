import os
import shutil
from pyspark.sql import SparkSession
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml import Pipeline
from pyspark.ml.regression import RandomForestRegressor
from pyspark.ml.evaluation import RegressionEvaluator

# Initialize Spark session
spark = SparkSession.builder.appName("CarPricePrediction").getOrCreate()

# Step 0: Load actual dataset here instead of hardcoded dummy data
# Example: df = spark.read.csv("your_data.csv", header=True, inferSchema=True)
data = [
    ("Toyota", "Corolla", 2018, "Petrol", "Manual", 50000, 20000),
    ("Honda", "Civic", 2019, "Diesel", "Automatic", 30000, 25000),
    ("Ford", "Focus", 2017, "Petrol", "Manual", 60000, 18000),
    ("BMW", "3 Series", 2020, "Petrol", "Automatic", 20000, 30000),
    ("Audi", "A4", 2021, "Diesel", "Automatic", 15000, 35000),
]

columns = ["brand", "model", "year", "fuel", "transmission", "kms_driven", "price"]
df = spark.createDataFrame(data, columns)

# Step 1: Drop nulls
df_cleaned = df.dropna(subset=["brand", "model", "year", "fuel", "transmission", "kms_driven", "price"])

# Step 2: Index categorical columns
brand_indexer = StringIndexer(inputCol="brand", outputCol="brand_indexed")
model_indexer = StringIndexer(inputCol="model", outputCol="model_indexed")
fuel_indexer = StringIndexer(inputCol="fuel", outputCol="fuel_indexed")
transmission_indexer = StringIndexer(inputCol="transmission", outputCol="transmission_indexed")

# Step 3: Assemble features
assembler = VectorAssembler(
    inputCols=["brand_indexed", "model_indexed", "year", "fuel_indexed", "transmission_indexed", "kms_driven"],
    outputCol="features"
)

# Step 4: Define regressor
rf = RandomForestRegressor(featuresCol="features", labelCol="price")

# Step 5: Build pipeline
pipeline = Pipeline(stages=[
    brand_indexer, model_indexer, fuel_indexer, transmission_indexer,
    assembler, rf
])

# Step 6: Train model
model = pipeline.fit(df_cleaned)

# Step 7: Predict and evaluate
predictions = model.transform(df_cleaned)
rmse = RegressionEvaluator(labelCol="price", predictionCol="prediction", metricName="rmse").evaluate(predictions)
print(f"Root Mean Squared Error (RMSE): {rmse}")

# Optional: Show predictions
predictions.select("brand", "model", "year", "kms_driven", "price", "prediction").show()

# Step 8: Save the model
model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saved_model")
if os.path.exists(model_path):
    shutil.rmtree(model_path)

model.write().overwrite().save(model_path)
print(f"Model has been saved to: {model_path}")

# Optional: Stop Spark session
spark.stop()
