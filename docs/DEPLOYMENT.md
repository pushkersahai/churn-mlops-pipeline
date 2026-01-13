# Deployment Guide

## Architecture Overview
```
Developer -> GitHub -> CI Tests -> Docker Build -> Manual Deploy to ACR -> AKS
```

## Prerequisites
- Azure CLI installed and logged in
- Docker Desktop running
- kubectl configured for AKS cluster

## Manual Deployment Steps

### 1. Build and Test Locally
```bash
# Run tests
pytest test_api.py -v

# Build Docker image
docker build -t churn-api:v1 -f api/Dockerfile .

# Test locally
docker run -d -p 8000:8000 --name churn-api-test churn-api:v1
curl http://localhost:8000/health
docker rm -f churn-api-test
```

### 2. Push to Azure Container Registry
```bash
# Set variables
ACR_NAME="churnmlopsacr1768341457"

# Login and push
az acr login --name $ACR_NAME
docker tag churn-api:v1 $ACR_NAME.azurecr.io/churn-api:v1
docker push $ACR_NAME.azurecr.io/churn-api:v1
```

### 3. Deploy to AKS
```bash
# Update deployment with new image
kubectl set image deployment/churn-api churn-api=$ACR_NAME.azurecr.io/churn-api:v1

# Check rollout status
kubectl rollout status deployment/churn-api

# Verify deployment
kubectl get pods
kubectl get services
```

### 4. Test Production Endpoint
```bash
# Get external IP
EXTERNAL_IP=$(kubectl get service churn-api-service -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

# Test health
curl http://$EXTERNAL_IP/health

# Test prediction
curl -X POST http://$EXTERNAL_IP/predict \
  -H "Content-Type: application/json" \
  -d '{"gender": 1, "SeniorCitizen": 0, "Partner": 1, "Dependents": 0, "tenure": 12, "PhoneService": 1, "PaperlessBilling": 1, "MonthlyCharges": 70.5, "TotalCharges": 850.0}'
```

## Automated CI/CD (Future Enhancement)
The current setup uses GitHub Actions for CI (testing) but requires manual deployment.

To add automated CD:
1. Create Azure Service Principal with proper permissions
2. Add AZURE_CREDENTIALS to GitHub Secrets
3. Update workflow to include deployment step

## Monitoring
```bash
# View logs
kubectl logs -l app=churn-api --tail=100

# Check pod status
kubectl get pods -l app=churn-api

# Describe deployment
kubectl describe deployment churn-api
```

## Cleanup
```bash
# Delete AKS resources
kubectl delete -f kubernetes/deployment.yaml
kubectl delete -f kubernetes/service.yaml

# Or delete entire resource group
az group delete --name rg-churn-mlops --yes --no-wait
```
