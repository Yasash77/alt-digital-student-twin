# ALT — AI-Powered Digital Student Twin

[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-RandomForest-F7931E?style=flat-square&logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)
[![Gemini](https://img.shields.io/badge/Google-Gemini%20Thinking%20AI-4285F4?style=flat-square&logo=google&logoColor=white)](https://ai.google.dev/)
[![Design](https://img.shields.io/badge/UI%20Design-Studio%20Mirage%20Obsidian-ff6200?style=flat-square)](https://studiomirage.io/)
[![Audio](https://img.shields.io/badge/Audio-432Hz%20Generative%20Ambient-10b981?style=flat-square)](https://en.wikipedia.org/wiki/432_Hz)

**CSI1006 Mini Project**: A genuine, data-driven Digital Student Twin platform synthesizing academic and behavioral telemetry (attendance, internal marks, study hours, assignment completion, daily mood, and sleep duration) into real-time GPA forecasts and academic risk predictions using dual trained **Random Forest** models. Features a luxury creative-technology dashboard modeled after **[Studio Mirage](https://studiomirage.io/)**, an integrated **432Hz calm generative ambient soundscape**, and deep cognitive reasoning powered by **Google Gemini Thinking AI**.

---

## ⚡ Quick Start Guide (Run in 2 Minutes)

### Option 1: Standard Python (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Yasash77/alt-digital-student-twin.git
   cd alt-digital-student-twin
   ```

2. **Create and activate a virtual environment:**
   - **Windows:**
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\activate
     ```
   - **macOS / Linux:**
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **(Optional) Configure Gemini Thinking AI Key:**
   Create a `.env` file or export your key:
   ```env
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   ```
   *(Note: The platform features a built-in Random Forest digital twin simulation engine that works 100% offline even without an external API key!)*

5. **Start the application:**
   ```bash
   uvicorn app:app --port 8000 --reload
   ```

6. **Open in browser:**
   👉 Go to **[http://localhost:8000](http://localhost:8000)**

---

### Option 2: Docker / Docker Compose

Run the entire stack with zero manual dependency setup:
```bash
docker compose up --build
```
Open **http://localhost:8000**.

---

## 🔑 Demo Account Credentials

Every endpoint enforces server-side JWT authentication and strict role-based access control (RBAC):

| Account | Password | Role | Access Scope |
| :--- | :--- | :--- | :--- |
| **`admin`** | `admin123` | **Faculty / Admin** | Complete cohort view (all 600 students), scatter correlations, feature importances, individual student twins, assistant, and model metrics. |
| **`s1000`** | `student123` | **Student (On Track)** | Restricted server-side to Student S1000 twin data (Predicted GPA ~8.10), daily check-in, and personalized AI mentor. |
| **`s1182`** | `student123` | **Student (Mid-Range)** | Restricted to Student S1182 twin data (Predicted GPA ~6.80). |
| **`s1093`** | `student123` | **Student (At Risk)** | Restricted to Student S1093 twin data (Predicted GPA ~2.90, academic risk intervention flag). |

*Quick login buttons are available right on the login screen.*

---

## 🎨 Key Features & Architecture

### 1. Studio Mirage Luxury Creative-Tech UI
- **Fixed Floating Blur Header**: Multi-layer progressive blur glass (`backdrop-filter: blur(24px) saturate(180%)`) with horizontal pill navigation and live status dot.
- **Fluid Magnetic Cursor**: Interactive trailing circular ring with physical inertia that dynamically expands on hover over cards, chips, and buttons.
- **Deep Obsidian Atmosphere**: Signature `#050505` background with hairline luminous borders (`rgba(255, 255, 255, 0.08)`), electric amber/orange highlights (`#ff6200`), and conic-gradient button reflections (`--border-shine`).

### 2. Generative 432Hz Calm Soothing Ambient Music
- Built-in Web Audio API generative synthesizer tuned to the calming **432 Hz** harmonic standard.
- Cycles through overlapping 9th and minor 7th pad chords (`Fmaj9`, `Cmaj7`, `Am9`, `Dm9`) with slow analog filter sweeps, gentle reverberant glass chime drops, and filtered ocean wave noise.
- Toggle anytime in the header via **`CALM MUSIC`** with an inline volume slider.

### 3. Gemini Thinking AI Cognitive Mentor
- Prioritizes Google's **Gemini Thinking AI** models (`gemini-2.0-flash-thinking-exp-01-21`, `gemini-2.5-pro`) with configured cognitive thinking budgets for deep reasoning over student telemetry.
- Automatically falls back to the internal Random Forest Digital Twin simulation engine if network connectivity is unavailable.

### 4. Machine Learning Core
- **GPA Regression**: Trained Random Forest Regressor ($R^2 = 0.94$, $MAE = 0.17$).
- **Risk Classification**: Trained Random Forest Classifier ($ROC\text{-}AUC = 0.98$, $F_1 = 0.92$).
- **Live What-If Simulator**: Real-time slider experiments allowing students to simulate how adjusting sleep or study hours immediately recalculates their predicted trajectory.

---

## ☁️ Cloud Deployment

The repository includes production-ready deployment configurations:

- **Render**: Blueprint defined in `render.yaml` (auto-deploys Web Service + Managed PostgreSQL).
- **Railway**: Configured via `railway.json`.
- **Docker**: Configured via `Dockerfile` and `docker-compose.yml`.

---

## 🛠️ API Reference

- `POST /api/auth/login` — Authenticate and receive a signed JWT token.
- `GET /api/cohort_summary` — Overall cohort statistics and at-risk watchlist (Admin).
- `GET /api/students` — List all tracked student twins (Admin).
- `GET /api/student/{id}/prediction` — Live GPA prediction, risk status, and recommendation.
- `POST /api/chat` — Context-aware AI chat with live parameter simulation.
- `POST /api/student/{id}/checkin` — Student daily check-in (updates mood & sleep in real time).
