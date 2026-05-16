# Cyris AI Assistant — Setup Guide

---

## About

This guide explains how to locally set up and run the Cyris AI Assistant MVP environment.

The project currently includes:

- backend orchestration systems
- adaptive behavioral coordination
- conversational interaction architecture
- AI orchestration infrastructure
- adaptive frontend interaction systems

---

## Requirements

Install:

- Python 3.11+
- Node.js 20+
- Git

---

## Backend Setup

### 1. Navigate to backend

```bash
cd backend
```

---

### 2. Create virtual environment

```bash
python -m venv venv
```

---

### 3. Activate virtual environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

---

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 5. Configure environment variables

Create:

```bash
.env
```

inside:

```bash
backend/
```

Add:

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

---

### 6. Run backend server

```bash
python run.py
```

Backend runs on:

```bash
http://127.0.0.1:8000
```

---

## Frontend Setup

### 1. Navigate to frontend

```bash
cd frontend
```

---

### 2. Install dependencies

```bash
npm install
```

---

### 3. Run frontend

```bash
npm run dev
```

Frontend runs on:

```bash
http://localhost:5173
```

---