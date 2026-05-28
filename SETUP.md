# Cyris Setup Guide

## 1. Clone the Repository

```bash
git clone <repo-url>
cd cyris-ai-assistant
```

---

## 2. Backend Setup

```bash
cd backend
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3. Configure Environment Variables

Create a `.env` file inside the `backend/` directory.

Copy values from `.env.example`.

Required:

* `GROQ_API_KEY`

Optional:

* `GEMINI_API_KEY`

Set provider:

```env
AI_PROVIDER=groq
```

---

## 4. Start Backend

```bash
python run.py
```

Backend runs at:

```text
http://127.0.0.1:8000
```

---

## 5. Frontend Setup

Open a new terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at:

```text
http://localhost:5173
```

---

## 6. Start Using Cyris

Open the frontend in your browser and begin chatting with Cyris.
