# Cyris AI Assistant — Setup Guide

## Project Root

cyris-ai-assistant

## Backend Environment Setup

### Create Python Virtual Environment

```powershell
python -m venv backend/venv
```

### Activate Virtual Environment

```powershell
backend\venv\Scripts\Activate.ps1
```

### Install Dependencies

```powershell
pip install fastapi uvicorn
```

### Generate requirements.txt

```powershell
pip freeze > backend/requirements.txt
```

## Run Backend Server

```powershell
uvicorn backend.app.main:app --reload
```

## Backend Entry Point

backend/app/main.py

## Current Backend Test Endpoint

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Cyris AI Assistant backend is running"}
```
