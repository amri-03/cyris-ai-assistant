# ⚙️ Cyris Setup & Installation Guide

Follow these steps to set up and run Cyris on your local development machine.

---

## Prerequisites

Before starting, ensure you have the following installed on your system:
* **Python 3.10+** (Ensure Python is added to your system PATH)
* **Node.js (v16+) and npm**

---

## 1. Clone the Repository

Open your terminal and clone the repository, then navigate to the root directory:

```bash
git clone https://github.com/amri-03/cyris-ai-assistant.git
cd cyris-ai-assistant
```

---

## 2. Backend Setup (FastAPI)

Navigate to the `backend` directory:

```bash
cd backend
```

### Create a Python Virtual Environment

* **Windows (PowerShell/CMD)**:
  ```bash
  python -m venv venv
  ```
* **macOS / Linux**:
  ```bash
  python3 -m venv venv
  ```

### Activate the Virtual Environment

* **Windows (PowerShell)**:
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
* **Windows (CMD)**:
  ```cmd
  .\venv\Scripts\activate.bat
  ```
* **macOS / Linux**:
  ```bash
  source venv/bin/activate
  ```

### Install Python Dependencies

Make sure your virtual environment is active (you should see `(venv)` in your terminal prompt), then run:

```bash
pip install -r requirements.txt
```

---

## 3. Configure Environment Variables

Create a file named `.env` in the `backend/` folder:

```bash
# On Windows (CMD/PowerShell) or macOS/Linux:
# Copy the example file to get started
cp .env.example .env
```

Open the `.env` file and configure your API keys and provider selection:

```env
# Choose your main chat provider: "gemini" or "groq"
AI_PROVIDER=gemini

# If using Gemini (highly recommended for both Chat and Memory extraction)
GEMINI_API_KEY=your_gemini_api_key_here

# If using Groq (Llama models)
GROQ_API_KEY=your_groq_api_key_here
```

---

## 4. Run the Backend Server

Start the FastAPI application by executing `run.py`:

```bash
python run.py
```

The backend API server will start up with auto-reload enabled at:
👉 **`http://127.0.0.1:8000`**

---

## 5. Frontend Setup (React + Vite)

Open a **new terminal window**, navigate to the `frontend` folder, install the Node packages, and run the development server:

```bash
cd frontend
npm install
npm run dev
```

The frontend client will start running at:
👉 **`http://localhost:5173`**

---

## 6. Access Cyris AI Assistant

Open your web browser and navigate to **`http://localhost:5173`** to begin chatting with Cyris!
* Click the **🧠 Memory** button in the top right header to toggle open the memory dashboard panel.
* Chat naturally, and Cyris will extract goals/struggles and automatically update your profile.
