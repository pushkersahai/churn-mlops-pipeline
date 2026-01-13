# Customer Churn Prediction - Production MLOps Pipeline

## Overview
End-to-end MLOps pipeline demonstrating production-grade ML deployment on Azure with automated testing, containerization, and Kubernetes orchestration.

## Business Problem
Predicts customer churn risk in real-time, enabling proactive retention campaigns. Model achieves 78% accuracy with ROC-AUC of 0.83.

## Architecture
```
Training: Databricks + MLflow
    |
    v
API: FastAPI + Docker
    |
    v
Registry: Azure Container Registry
    |
    v
Production: Azure Kubernetes Service (AKS)
    |
    v
CI/CD: GitHub Actions
```

## Tech Stack
- **ML Training**: Azure Databricks, MLflow, scikit-learn
- **API**: FastAPI, Python 3.10
- **Containerization**: Docker
- **Orchestration**: Kubernetes (AKS)
- **CI/CD**: GitHub Actions
- **Cloud**: Microsoft Azure
- **Testing**: pytest

## Project Structure
```
churn-mlops-pipeline/
├── api/
│   ├── main.py              # FastAPI application
│   ├── churn_model.pkl      # Trained model
│   └── Dockerfile           # Container definition
├── kubernetes/
│   ├── deployment.yaml      # K8s deployment config
│   └── service.yaml         # K8s service config
├── .github/workflows/
│   └── ci.yaml              # CI/CD pipeline
├── docs/
│   └── DEPLOYMENT.md        # Deployment guide
├── train_local.py           # Model training script
├── test_api.py              # API tests
└── requirements.txt         # Python dependencies
```

## Key Features
- Automated testing with pytest (4 test cases)
- Containerized ML inference API
- Kubernetes deployment with auto-scaling
- Health checks and readiness probes
- CI pipeline with automated builds
- Model versioning via Docker tags

## API Endpoints

### Health Check
```bash
GET /health
Response: {"status": "healthy", "model_loaded": true}
```

### Prediction
```bash
POST /predict
Body: {
  "gender": 1,
  "SeniorCitizen": 0,
  "Partner": 1,
  "Dependents": 0,
  "tenure": 12,
  "PhoneService": 1,
  "PaperlessBilling": 1,
  "MonthlyCharges": 70.5,
  "TotalCharges": 850.0
}
Response: {
  "churn_prediction": 0,
  "churn_probability": 0.377,
  "risk_level": "Low"
}
```

## Local Development

### Setup
```bash
# Clone repository
git clone https://github.com/pushkersahai/churn-mlops-pipeline.git
cd churn-mlops-pipeline

# Create virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Train model
python train_local.py
```

### Run Tests
```bash
pytest test_api.py -v
```

### Run API Locally
```bash
uvicorn api.main:app --reload --port 8000
curl http://localhost:8000/health
```

### Build and Run Docker Container
```bash
docker build -t churn-api:v1 -f api/Dockerfile .
docker run -d -p 8000:8000 churn-api:v1
```

## Production Deployment
See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed deployment instructions.

## Model Details
- **Algorithm**: Logistic Regression
- **Training Data**: Telco Customer Churn (7,043 customers)
- **Features**: 30 (after one-hot encoding)
- **Metrics**:
  - Accuracy: 78.5%
  - Precision: 61.8%
  - Recall: 50.3%
  - F1 Score: 55.5%
  - ROC-AUC: 82.9%

## CI/CD Pipeline
GitHub Actions workflow runs on every push:
1. Install dependencies
2. Train model
3. Run automated tests
4. Build Docker image
5. (Manual deployment to AKS)


## Author
Pushker Sahai
LinkedIn: www.linkedin.com/in/pushkersahai

## License
MIT
EOF
