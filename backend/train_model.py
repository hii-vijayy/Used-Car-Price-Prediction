import os
import shutil
from pyspark.sql import SparkSession
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml import Pipeline
from pyspark.ml.regression import RandomForestRegressor
from pyspark.ml.evaluation import RegressionEvaluator

# Initialize Spark session
spark = SparkSession.builder.appName("CarPricePrediction").getOrCreate()

# Sample DataFrame creation (Replace this with loading your actual dataset)
data = [
    ("Toyota", "Corolla", 2018, "Petrol", "Manual", 50000, 20000),
    ("Honda", "Civic", 2019, "Diesel", "Automatic", 30000, 25000),
    ("Ford", "Focus", 2017, "Petrol", "Manual", 60000, 18000),
    ("BMW", "3 Series", 2020, "Petrol", "Automatic", 20000, 30000),
    ("Audi", "A4", 2021, "Diesel", "Automatic", 15000, 35000),
    # Add more rows as needed
]

columns = ["Brand", "Model", "Year", "Fuel", "Transmission", "kmDriven", "Price"]

df = spark.createDataFrame(data, columns)

# Step 1: Handle null values (remove rows with nulls in selected columns)
df_cleaned = df.dropna(subset=['Brand', 'Model', 'Year', 'Fuel', 'Transmission', 'kmDriven'])

# Step 2: StringIndexer for categorical columns (Brand, Model, Fuel, Transmission)
brand_indexer = StringIndexer(inputCol="Brand", outputCol="Brand_indexed")
model_indexer = StringIndexer(inputCol="Model", outputCol="model_indexed")
fuel_indexer = StringIndexer(inputCol="Fuel", outputCol="Fuel_indexed")
transmission_indexer = StringIndexer(inputCol="Transmission", outputCol="Transmission_indexed")

# Step 3: Assemble features into a single vector using VectorAssembler
assembler = VectorAssembler(
    inputCols=['Brand_indexed', 'model_indexed', 'Year', 'Fuel_indexed', 'Transmission_indexed', 'kmDriven'],
    outputCol='features'
)

# Step 4: Define the regression model (Random Forest in this case)
rf = RandomForestRegressor(featuresCol='features', labelCol='Price')

# Step 5: Set up the pipeline
pipeline = Pipeline(stages=[brand_indexer, model_indexer, fuel_indexer, transmission_indexer, assembler, rf])

# Step 6: Fit the pipeline model
model = pipeline.fit(df_cleaned)

# Step 7: Make predictions on the data
predictions = model.transform(df_cleaned)

# Step 8: Evaluate the model (using RegressionEvaluator)
evaluator = RegressionEvaluator(labelCol="Price", predictionCol="prediction", metricName="rmse")
rmse = evaluator.evaluate(predictions)

# Step 9: Show some predictions and the RMSE result
predictions.select("Brand", "Model", "Year", "kmDriven", "Price", "prediction").show()

print(f"Root Mean Squared Error (RMSE): {rmse}")

# Save the trained model
script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, "saved_model")

# Remove the existing model directory if it exists
if os.path.exists(model_path):
    shutil.rmtree(model_path)

# Save the model with overwrite
model.write().overwrite().save(model_path)
print(f"Model has been saved to: {model_path}")
