from pyspark.sql import SparkSession
import os

# Initialize Spark
spark = SparkSession.builder.appName("DataDiagnosis").getOrCreate()

try:
    # Check if files exist
    files = ["data/used_car_dataset.csv", "data/used_car_dataset2.csv"]
    for file in files:
        if not os.path.exists(file):
            print(f"⚠️ File not found: {file}")
        else:
            print(f"✅ File exists: {file} (Size: {os.path.getsize(file)} bytes)")
    
    # Try loading each file individually
    for file in files:
        if os.path.exists(file):
            print(f"\n----- Analyzing {file} -----")
            try:
                # Load raw file with minimal processing
                df = spark.read.option("header", True).csv(file)
                
                # Print basic info
                print(f"Row count: {df.count()}")
                print(f"Column count: {len(df.columns)}")
                print(f"Columns: {', '.join(df.columns)}")
                
                # Show sample
                print("\nSample data:")
                df.show(5, truncate=False)
                
                # Check AskPrice values
                print("\nAskPrice sample values:")
                df.select("AskPrice").show(10, truncate=False)
                
                # Check for nulls in critical columns
                for col_name in ["Brand", "model", "Year", "kmDriven", "AskPrice"]:
                    if col_name in df.columns:
                        null_count = df.filter(df[col_name].isNull()).count()
                        print(f"Nulls in {col_name}: {null_count}")
                    else:
                        print(f"Column {col_name} not found")
            
            except Exception as e:
                print(f"❌ Error processing {file}: {str(e)}")

except Exception as e:
    print(f"❌ Error: {str(e)}")
finally:
    spark.stop()