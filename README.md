# Customer Churn Prediction - Production MLOps Pipeline

## Overview
End-to-end MLOps pipeline for real-time customer churn prediction on Azure.

## Architecture
Data -> Databricks (Training) -> MLflow (Registry) -> Docker (API) -> ACR -> AKS (Production)

## Tech Stack
- Training: Azure Databricks, MLflow
- API: FastAPI, Docker
- Deployment: Azure Kubernetes Service (AKS)
- CI/CD: GitHub Actions
- Monitoring: Kubernetes health checks

## Business Problem
Predicts customer churn risk in real-time for proactive retention campaigns.

## Author
Pushker - Senior AI Sales Engineer
