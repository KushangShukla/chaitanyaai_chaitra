# CHAITRA

Cognitive Hybrid AI for Tactical Reasoning & Analytics

CHAITRA is a full-stack AI-powered business analytics platform that combines machine learning, retrieval-based intelligence, and natural language interaction to improve decision-making from structured business data.

The platform extends traditional dashboards by adding:

- Predictive analytics
- Automated business insights
- Conversational querying
- Voice interaction
- Retrieval-Augmented Generation (RAG)
- Explainable AI support

It is designed as a modular production-style system with separate frontend, backend, and database layers.

---

# Table of Contents

1. Overview  
2. Key Features  
3. Technology Stack  
4. System Architecture  
5. Core Modules  
6. Machine Learning Pipeline  
7. Natural Language Query System  
8. Voice Features  
9. Repository Structure  
10. API Endpoints  
11. Database Design  
12. Local Setup  
13. Docker Deployment  
14. Configuration  
15. Screenshots / Outputs  
16. Testing  
17. Security  
18. Performance Notes  
19. Future Improvements  
20. Contributors  
21. License

---

# Overview

Many business dashboards only display historical metrics and charts. They often require manual interpretation and do not provide predictive or contextual assistance.

CHAITRA solves this by combining:

- Structured analytics
- Forecasting models
- AI-generated reasoning
- Searchable business knowledge
- Natural language interaction

Users can upload business datasets, generate predictions, view KPI dashboards, ask questions in natural language, and receive intelligent responses.

---

# Key Features

## Analytics & Prediction

- Predictive modeling using XGBoost
- KPI computation
- Trend analysis
- Structured forecasting outputs

## AI & Reasoning

- LLM-powered chat interface
- Retrieval-Augmented Generation (RAG)
- Natural language query to database response workflow
- Contextual business explanations

## Data Platform

- CSV dataset upload
- PDF upload for knowledge ingestion
- Multi-stage preprocessing pipeline
- PostgreSQL storage

## User Experience

- React dashboard
- Charts and visualizations
- Speech-to-Text input
- Text-to-Speech output
- Profile and settings management

## Engineering

- FastAPI backend
- Dockerized services
- PostgreSQL database
- Nginx-ready deployment
- AWS EC2 compatible

---

# Technology Stack

## Frontend

- React
- TypeScript
- Chart.js
- Recharts

## Backend

- Python
- FastAPI
- Uvicorn

## Machine Learning

- XGBoost
- Scikit-learn
- Pandas
- NumPy

## AI / NLP

- Transformers
- Sentence Transformers
- FAISS
- SHAP

## Database

- PostgreSQL

## Authentication

- JWT
- bcrypt / Passlib

## DevOps

- Docker
- Docker Compose
- Nginx
- AWS EC2

---

# System Architecture


User
 │
 ▼
React Frontend
 │
 ▼
FastAPI Backend
 ├── Authentication Layer
 ├── Upload Services
 ├── Prediction Engine
 ├── Query Router
 ├── Voice Services
 └── Dashboard APIs
      │
      ├── PostgreSQL
      ├── XGBoost Model
      ├── FAISS Vector Store
      └── LLM / Response Layer
