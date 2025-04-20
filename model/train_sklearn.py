import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import os
import re
import joblib

try:
    # Load datasets
    print("Loading datasets...")
    df1 = pd.read_csv("data/used_car_dataset.csv")
    df2 = pd.read_csv("data/used_car_dataset2.csv")
    
    # Combine datasets
    df = pd.concat([df1, df2], ignore_index=True)
    print(f"Combined dataset row count: {len(df)}")
    
    # Fix column names
    if 'AdditionInfo' in df.columns:
        df.rename(columns={"AdditionInfo": "AdditionalInfo"}, inplace=True)
    
    # Clean AskPrice - remove ₹, commas, and spaces
    df['AskPrice'] = df['AskPrice'].astype(str).str.replace('[₹,\s]', '', regex=True)
    df['AskPrice'] = pd.to_numeric(df['AskPrice'].str.replace('^$', '0', regex=True), errors='coerce')
    
    # Clean kmDriven - extract just the numbers
    df['kmDriven'] = df['kmDriven'].astype(str).str.replace('[^0-9.]', '', regex=True)
    df['kmDriven'] = pd.to_numeric(df['kmDriven'].str.replace('^$', '0', regex=True), errors='coerce')
    
    # Check if we have valid data after cleaning
    valid_rows = df[(df['AskPrice'] > 0) & (df['kmDriven'] > 0) & (~df['Year'].isna())]
    print(f"Valid rows after cleaning: {len(valid_rows)}")
    
    if len(valid_rows) == 0:
        raise ValueError("No valid rows found after data cleaning")
    
    # Fill missing values for categorical columns
    categorical_cols = ["Brand", "model", "Transmission", "Owner", "FuelType"]
    for cat_col in categorical_cols:
        if cat_col in valid_rows.columns:
            valid_rows[cat_col] = valid_rows[cat_col].fillna("Unknown")
    
    # Calculate Age
    valid_rows['Age'] = 2025 - valid_rows['Year']
    
    # Show sample of processed data
    print("\nSample of processed data:")
    print(valid_rows[['Brand', 'model', 'Year', 'Age', 'kmDriven', 'AskPrice']].head(5))
    
    # Define categorical and numerical features
    categorical_cols = [col for col in categorical_cols if col in valid_rows.columns]
    numerical_cols = ["Year", "Age", "kmDriven"]
    
    # Prepare data for model
    X = valid_rows.drop('AskPrice', axis=1)
    y = valid_rows['AskPrice']
    
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Create preprocessing pipeline for categorical and numerical data
    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])
    
    numerical_transformer = Pipeline(steps=[
        ('scaler', StandardScaler())
    ])
    
    # Create column transformer
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', categorical_transformer, categorical_cols),
            ('num', numerical_transformer, numerical_cols)
        ],
        remainder='drop'  # Drop columns not specified
    )
    
    # Create model pipeline
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', LinearRegression())
    ])
    
    # Train model
    print("Training model...")
    model.fit(X_train, y_train)
    
    # Evaluate model
    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    
    print(f"Root Mean Squared Error: {rmse}")
    print(f"R² (coefficient of determination): {r2}")
    
    # Save the model
    output_path = "model/saved_model/sklearn_model.joblib"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    joblib.dump(model, output_path)
    print("\n✅ Model trained and saved successfully!")
    
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()