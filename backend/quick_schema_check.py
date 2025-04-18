# quick_schema_check.py
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("CheckSchema").getOrCreate()
df = spark.read.csv("used_car_dataset.csv", header=True, inferSchema=True)
df.printSchema()
