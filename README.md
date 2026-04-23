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

# System Architecture Workflow

The CHAITRA platform follows a multi-stage workflow where user requests are processed through modular services for analytics, prediction, retrieval, and intelligent response generation.

User Access
   ↓
Frontend Interface (React Dashboard)
   ↓
Authentication Check
   ↓
Request Routing (FastAPI Backend)
   ↓
Choose Operation
   ├── CSV Upload
   │      ↓
   │   Data Validation
   │      ↓
   │   PostgreSQL Storage
   │      ↓
   │   Preprocessing Pipeline
   │      ↓
   │   Feature Engineering
   │      ↓
   │   XGBoost Prediction
   │      ↓
   │   KPI + Charts Output
   │
   ├── Natural Language Query
   │      ↓
   │   Intent Detection
   │      ↓
   │   Query Router
   │      ├── SQL Retrieval Path
   │      ├── Prediction Path
   │      ├── RAG Retrieval Path
   │      └── LLM Reasoning Path
   │      ↓
   │   Natural Language Response
   │
   ├── PDF Upload
   │      ↓
   │   Text Extraction
   │      ↓
   │   Embedding Creation
   │      ↓
   │   FAISS Vector Storage
   │
   └── Voice Interaction
          ↓
       Speech-to-Text
          ↓
       Query Processing
          ↓
       Text-to-Speech Response
Core Modules

1. Authentication Module
Supports secure account access:
Signup
Login
Password hashing
JWT token sessions

2. Dashboard Module
Displays:
KPI cards
Forecast outputs
Trend charts
Business metrics

3. Prediction Module
Used for structured forecasting tasks.
Current implementation uses:
XGBoost Regressor

4. Query Intelligence Module
Supports user questions such as:
Explain current trend
What is predicted next?
Why did sales change?
Show important factors

5. RAG Module
Used for contextual retrieval from uploaded content:
PDF ingestion
Embedding generation
FAISS search
Context-aware responses

6. Voice Module
Supports:
Speech-to-Text input
Text-to-Speech output

Machine Learning Pipeline
Raw Dataset
   ↓
Validation
   ↓
Cleaning
   ↓
Outlier Handling
   ↓
Encoding
   ↓
Normalization
   ↓
Feature Engineering
   ↓
Feature Selection
   ↓
ML Ready Dataset
   ↓
XGBoost Training
   ↓
Prediction Output

Model Used
XGBoost Regressor
Evaluation Metrics
MAE
RMSE
R² Score

Natural Language Query System
CHAITRA supports business query interaction.

Flow
User Query
   ↓
Intent Detection
   ↓
Route Decision
   ├── Database Query Path
   ├── Prediction Path
   ├── RAG Retrieval Path
   └── LLM Explanation Path
   ↓
Natural Language Response

Voice Features
Speech-to-Text
User can speak instead of typing.
Text-to-Speech
System can read responses aloud.

Useful for:
Accessibility
Hands-free usage
Faster interaction

Repository Structure
chaitanyaai_chaitra/
│
├── frontend/
│   ├── src/
│   ├── components/
│   ├── pages/
│   └── services/
│
├── backend/
│   ├── main.py
│   ├── routes/
│   ├── scripts/
│   │   ├── ml/
│   │   ├── rag/
│   │   ├── auth/
│   │   └── orchestrator/
│   └── requirements.txt
│
├── docker-compose.yml
├── nginx/
├── docs/
└── README.md

API Endpoints

Authentication
POST /auth/signup
POST /auth/login

Upload
POST /upload
POST /upload/pdf

Prediction
POST /predict
GET /predictions/latest

Query
POST /query

Health
GET /docs
GET /health

Database Design
Examples of tables used in the project:
User Tables
users
user_settings
Interaction Tables
chat_history
query_logs
Dataset Tables
training_data
walmart_sales
walmart_sales_cleaned
walmart_sales_ml_ready
Output Tables
predictions
analytics_results

Local Setup
1. Clone Repository
git clone https://github.com/KushangShukla/chaitanyaai_chaitra.git
cd chaitanyaai_chaitra

2. Configure Environment
Create .env
DATABASE_URL=postgresql://user:password@db:5432/chaitra
JWT_SECRET=your_secret

3. Run with Docker
docker-compose up --build

4. Access

Frontend:
http://localhost:3000

Backend:
http://localhost:8000/docs

Docker Deployment
Services supported:
frontend
backend
postgres

Production-ready improvements:
Reverse proxy via Nginx
HTTPS with SSL
Environment isolation
Container scaling

Configuration Notes
For lightweight deployment environments:
Disable local LLM runtime
Keep prediction APIs enabled
Keep dashboard enabled
Keep PostgreSQL active
Useful for low-memory cloud instances.

Screenshots / Outputs:
Login page
Signup page
Dashboard
KPI cards
Prediction outputs
Chat interface
Voice features
PostgreSQL tables
Docker running containers
AWS deployment page
Testing
Covered Areas
Authentication
CSV upload
Prediction APIs
Query responses
Dashboard rendering
Database writes
Docker services
Voice features
Example Checks
Valid login
Invalid login rejection
Successful prediction response
Correct chart rendering
Query output generation
Security

Implemented controls:
JWT authentication
Password hashing
Protected routes
Session handling
Input validation

Recommended next steps:
Role-based access control
Audit logging
Rate limiting
HTTPS enforcement

Performance Notes
Modular architecture improves maintainability
XGBoost offers strong structured-data performance
RAG improves contextual answers
LLM can be disabled for lightweight deployment

Future Improvements
Multi-tenant SaaS architecture
Real-time streaming analytics
AutoML training workflows
Role-based enterprise access
Full cloud LLM deployment
Scheduled reporting engine
Advanced anomaly detection

Contributors
Kushang Shukla
AI / ML Engineer Intern

License
This repository is intended for academic, research, and demonstration purposes unless otherwise specified.

Project Summary
CHAITRA demonstrates how modern analytics systems can move beyond static dashboards into intelligent decision platforms by combining machine learning, retrieval systems, and natural language interaction in one scalable architecture.

