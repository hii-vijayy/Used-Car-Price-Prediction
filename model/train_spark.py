from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.regression import LinearRegression
import os
from pyspark.sql.functions import col, regexp_replace, when
from pyspark.sql.types import DoubleType, IntegerType

# Initialize Spark
spark = SparkSession.builder.appName("CarPricePrediction").getOrCreate()

try:
    # Load datasets
    print("Loading datasets...")
    df1 = spark.read.csv("data/used_car_dataset.csv", header=True, inferSchema=True)
    df2 = spark.read.csv("data/used_car_dataset2.csv", header=True, inferSchema=True)
    
    # Combine datasets
    df = df1.unionByName(df2)
    print(f"Combined dataset row count: {df.count()}")
    
    # Fix column names
    df = df.withColumnRenamed("AdditionInfo", "AdditionalInfo")
    
    # Clean AskPrice - remove ₹, commas, and spaces
    df = df.withColumn("AskPrice", 
                      regexp_replace(
                          regexp_replace(col("AskPrice"), "[₹,\\s]", ""),  # Remove rupee symbol, commas, spaces
                          "^$", "0"  # Replace empty strings with 0
                      ).cast(DoubleType()))
    
    # Clean kmDriven - extract just the numbers
    df = df.withColumn("kmDriven", 
                      regexp_replace(
                          regexp_replace(col("kmDriven"), "[^0-9.]", ""),  # Keep only digits and decimal point
                          "^$", "0"  # Replace empty strings with 0
                      ).cast(DoubleType()))
    
    # Check if we have valid data after cleaning
    valid_rows = df.filter(
        (col("AskPrice") > 0) & 
        (col("kmDriven") > 0) &
        (col("Year").isNotNull())
    )
    
    print(f"Valid rows after cleaning: {valid_rows.count()}")
    
    if valid_rows.count() == 0:
        raise ValueError("No valid rows found after data cleaning")
    
    # Fill missing values for categorical columns
    categorical_cols = ["Brand", "model", "Transmission", "Owner", "FuelType"]
    for cat_col in categorical_cols:
        valid_rows = valid_rows.fillna("Unknown", subset=[cat_col])
    
    # Calculate Age
    valid_rows = valid_rows.withColumn("Age", 2025 - col("Year"))
    
    # Show sample of processed data
    print("\nSample of processed data:")
    valid_rows.select("Brand", "model", "Year", "Age", "kmDriven", "AskPrice").show(5)
    
    # Define categorical and numerical features
    numerical_cols = ["Year", "Age", "kmDriven"]
    
    # Apply StringIndexer
    indexers = [StringIndexer(inputCol=col, outputCol=col + "_indexed", handleInvalid="keep") 
                for col in categorical_cols]
    
    # Final feature columns
    feature_cols = [col + "_indexed" for col in categorical_cols] + numerical_cols
    
    # Create vector assembler
    assembler = VectorAssembler(
        inputCols=feature_cols,
        outputCol="features",
        handleInvalid="keep"
    )
    
    # Define regression model with regularization
    lr = LinearRegression(
        featuresCol="features", 
        labelCol="AskPrice",
        regParam=0.01,  # Add regularization to avoid overfitting
        maxIter=10,     # Limit iterations in case of convergence issues
        standardization=True  # Standardize features
    )
    
    # Create pipeline
    pipeline = Pipeline(stages=indexers + [assembler, lr])
    
    # Train model
    print("Training model...")
    model = pipeline.fit(valid_rows)
    
    # Print model summary
    summary = model.stages[-1].summary
    print(f"Root Mean Squared Error: {summary.rootMeanSquaredError}")
    print(f"R² (coefficient of determination): {summary.r2}")
    
    # Save the model
    output_path = "model/saved_model"
    if os.path.exists(output_path):
        import shutil
        shutil.rmtree(output_path)
    
    model.save(output_path)
    print("\n✅ Model trained and saved successfully!")
    
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
finally:
    spark.stop()