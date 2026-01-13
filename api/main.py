from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import os

app = FastAPI(title="Churn Prediction API", version="1.0")

model = None
feature_columns = None

@app.on_event("startup")
async def load_model():
    global model, feature_columns
    
    # Try multiple paths for different environments
    model_paths = [
        "churn_model.pkl",           # Docker container
        "api/churn_model.pkl",        # Local development and CI
        "/app/churn_model.pkl"        # Alternative Docker path
    ]
    
    model_path = None
    for path in model_paths:
        if os.path.exists(path):
            model_path = path
            break
    
    if model_path is None:
        # List current directory for debugging
        print(f"Current directory: {os.getcwd()}")
        print(f"Files in current directory: {os.listdir('.')}")
        if os.path.exists('api'):
            print(f"Files in api/: {os.listdir('api')}")
        raise FileNotFoundError("Model file not found in any expected location")
    
    model = joblib.load(model_path)
    feature_columns = model.feature_names_in_
    print(f"Model loaded from {model_path}")
    print(f"Expected features: {len(feature_columns)}")

class CustomerData(BaseModel):
    gender: int
    SeniorCitizen: int
    Partner: int
    Dependents: int
    tenure: int
    PhoneService: int
    PaperlessBilling: int
    MonthlyCharges: float
    TotalCharges: float
    MultipleLines: str = "No"
    InternetService: str = "DSL"
    OnlineSecurity: str = "No"
    OnlineBackup: str = "No"
    DeviceProtection: str = "No"
    TechSupport: str = "No"
    StreamingTV: str = "No"
    StreamingMovies: str = "No"
    Contract: str = "Month-to-month"
    PaymentMethod: str = "Electronic check"

@app.get("/")
def root():
    return {"message": "Churn Prediction API", "status": "running", "version": "1.0"}

@app.get("/health")
def health():
    return {"status": "healthy", "model_loaded": model is not None}

@app.post("/predict")
def predict(data: CustomerData):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    input_dict = data.model_dump()
    
    categorical_cols = ['MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup', 
                       'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies', 
                       'Contract', 'PaymentMethod']
    
    input_df = pd.DataFrame([input_dict])
    input_df = pd.get_dummies(input_df, columns=categorical_cols, drop_first=True)
    
    for col in feature_columns:
        if col not in input_df.columns:
            input_df[col] = 0
    
    input_df = input_df[feature_columns]
    
    prediction = model.predict(input_df)
    probability = model.predict_proba(input_df)[0][1]
    
    return {
        "churn_prediction": int(prediction[0]),
        "churn_probability": float(probability),
        "risk_level": "High" if probability > 0.7 else "Medium" if probability > 0.4 else "Low"
    }
