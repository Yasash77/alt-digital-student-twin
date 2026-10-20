"""
app.py
FastAPI backend + dashboard host for the AI-Powered Digital Student Twin
(ALT) prototype.

ONE command runs the whole thing:  uvicorn app:app --reload --port 8000
Then open:  http://localhost:8000

(Earlier versions of this prototype served dashboard.html separately, e.g.
via VS Code Live Server on a different port -- that meant two processes on
two ports, and an easy-to-hit failure mode where the dashboard loads but
can't reach the API because it's simply not running yet. This version
serves the dashboard AND the API from the same FastAPI app on the same
port, so there is exactly one thing to start and one URL to open.)

Auth: every /api/... route below (except /api/auth/login and /api/status)
requires a Bearer token issued by POST /api/auth/login (see auth.py).
Demo accounts are in users.json / documented in README.md. A "student"
token can only ever read/write ITS OWN student_id -- that's enforced here
server-side via auth.require_own_student_or_admin, not just hidden in the
UI, so it's a real authorization boundary, not a cosmetic one.

Endpoints:
  GET  /                        -> the dashboard (dashboard.html)
  POST /api/auth/login          -> {username, password} -> {access_token, role, student_id, display_name}
  GET  /api/auth/me             -> the current token's identity
  GET  /api/students            -> list all students (admin only)
  GET  /api/students/{id}       -> one student's raw record (admin, or that student)
  GET  /api/predict/{id}        -> GPA prediction + risk flag (admin, or that student)
  POST /api/predict             -> GPA prediction + risk flag for ad-hoc input (any logged-in user -- the what-if simulator)
  GET  /api/recommend/{id}      -> AI-generated recommendation (admin, or that student)
  POST /api/chat                -> free-form Q&A about one student (admin, or that student)
  GET  /api/metrics             -> model performance metrics (any logged-in user)
  GET  /api/cohort_summary      -> cohort-wide stats for the Overview page (admin only, includes per-student watchlist)
  GET  /api/cohort_aggregate    -> cohort AVERAGES only, no per-student data (any logged-in user -- "how you compare")
  POST /api/students/{id}/checkin -> log today's mood/sleep, re-predict live, persist to the database (admin, or that student)
"""
import json
import logging
import re

import joblib
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

import auth
import db
import gemini_chat

load_dotenv()  # reads GEMINI_API_KEY from a local .env file, if present

logger = logging.getLogger("alt")

app = FastAPI(title="ALT — AI-Powered Digital Student Twin", version="1.0.0")

# CORS stays open in case someone still wants to serve the dashboard from a
# separate dev server (e.g. Live Server) while pointing it at this API --
# but the default, recommended path below no longer needs it, since the
# dashboard is served from this same app on the same origin.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

FEATURES = joblib.load("models/features.pkl")
gpa_model = joblib.load("models/gpa_model.pkl")
risk_model = joblib.load("models/risk_model.pkl")
RISK_THRESHOLD = joblib.load("models/risk_threshold.pkl")
db.init_db()  # create tables + seed from CSV/users.json on first run
with open("models/metrics.json") as f:
    METRICS = json.load(f)


class StudentFeatures(BaseModel):
    attendance_pct: float
    avg_marks: float
    study_hours_per_day: float
    assignment_completion_pct: float
    daily_checkin_mood: float
    sleep_hours: float


class ChatTurn(BaseModel):
    role: str  # "user" | "model"
    text: str


class ChatRequest(BaseModel):
    student_id: str
    message: str
    history: list[ChatTurn] = []


class LoginRequest(BaseModel):
    username: str
    password: str


class CheckinRequest(BaseModel):
    daily_checkin_mood: float
    sleep_hours: float


def _predict(features_row: dict) -> dict:
    X = pd.DataFrame([features_row])[FEATURES]
    gpa_pred = float(gpa_model.predict(X)[0])
    risk_proba = float(risk_model.predict_proba(X)[0][1])
    risk_flag = bool(risk_proba >= RISK_THRESHOLD)
    return {
        "predicted_gpa": round(gpa_pred, 2),
        "risk_probability": round(risk_proba, 3),
        "at_risk": risk_flag,
    }


def _rule_based_recommend(features_row: dict, prediction: dict) -> dict:
    """Rule-based recommendation engine -- the ORIGINAL milestone-1 engine,
    now kept on as an automatic fallback for when Gemini is unavailable
    (no API key configured, network down, quota hit, etc.) so the dashboard
    never breaks. See _recommend() below for the Gemini-first logic and
    gemini_chat.py for the actual API integration.
    """
    tips = []
    if features_row["attendance_pct"] < 75:
        tips.append("Attendance is below 75% — prioritise attending upcoming classes to stay eligible.")
    if features_row["study_hours_per_day"] < 2:
        tips.append("Study hours are low — try blocking at least 2 focused hours daily, even in short sessions.")
    if features_row["assignment_completion_pct"] < 70:
        tips.append("Several assignments look incomplete — clearing the backlog will lift both marks and mood.")
    if features_row["daily_checkin_mood"] < 3:
        tips.append("Recent mood check-ins are low — consider a short break or talking to a mentor/counsellor.")
    if features_row["sleep_hours"] < 6:
        tips.append("Sleep is under 6 hours on average — this is strongly linked to both burnout and lower marks.")

    if prediction["at_risk"]:
        headline = "This student is flagged as academically at-risk. Immediate, focused support is recommended."
    elif prediction["predicted_gpa"] >= 8.5:
        headline = "Strong trajectory — consider stretch goals (research, competitive exams, placement prep)."
    else:
        headline = "On track. The tips below are targeted areas to push the GPA trend further up."

    if not tips:
        tips.append("All core signals look healthy — maintain current habits and recheck weekly.")

    return {"headline": headline, "tips": tips, "source": "rule_based"}


def _recommend(features_row: dict, prediction: dict) -> dict:
    """Gemini-first recommendation, with an automatic, silent fallback to
    the rule-based engine on any failure. The response always carries
    "source" so the UI (and the demo) can honestly show which one ran.
    """
    if gemini_chat.is_configured():
        try:
            return gemini_chat.generate_recommendation(features_row, prediction)
        except Exception:
            logger.exception("Gemini recommendation failed, falling back to rule-based")
    return _rule_based_recommend(features_row, prediction)


def _get_student_row(student_id: str):
    row = db.get_student(student_id)
    if row is None:
        raise HTTPException(status_code=404, detail="student not found")
    return pd.Series(row)


@app.get("/")
def root():
    return FileResponse("dashboard.html", headers={
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
        "Expires": "0"
    })


@app.get("/chart.umd.js")
def chart_js():
    # Served explicitly (rather than mounting the whole directory) so only
    # the dashboard's own assets are exposed -- not the dataset or model files.
    return FileResponse("chart.umd.js", media_type="application/javascript")


@app.get("/api/status")
def status():
    return {
        "service": "ALT Digital Student Twin API",
        "endpoints": [
            "/api/auth/login (POST)", "/api/auth/me", "/api/students", "/api/students/{id}",
            "/api/predict/{id}", "/api/predict (POST)", "/api/recommend/{id}", "/api/metrics",
        ],
    }


# ---------------- Auth ----------------

@app.post("/api/auth/login")
def login(payload: LoginRequest):
    user = auth.authenticate(payload.username, payload.password)
    token = auth.issue_token(user)
    return {
        "access_token": token,
        "role": user["role"],
        "student_id": user["student_id"],
        "display_name": user["display_name"],
    }


@app.get("/api/auth/me")
def me(user: dict = Depends(auth.get_current_user)):
    return {
        "username": user["sub"],
        "role": user["role"],
        "student_id": user["student_id"],
        "display_name": user["display_name"],
    }


# ---------------- Students / predictions / recommendations ----------------

@app.get("/api/students")
def list_students(user: dict = Depends(auth.get_current_user)):
    auth.require_admin(user)
    return db.get_students_df().to_dict(orient="records")


@app.get("/api/students/{student_id}")
def get_student(student_id: str, user: dict = Depends(auth.get_current_user)):
    auth.require_own_student_or_admin(user, student_id)
    return _get_student_row(student_id).to_dict()


@app.get("/api/predict/{student_id}")
def predict_for_student(student_id: str, user: dict = Depends(auth.get_current_user)):
    auth.require_own_student_or_admin(user, student_id)
    row = _get_student_row(student_id)
    features_row = row[FEATURES].to_dict()
    return {"student_id": student_id, **_predict(features_row)}


@app.post("/api/predict")
def predict_adhoc(payload: StudentFeatures, user: dict = Depends(auth.get_current_user)):
    """Ad-hoc prediction for a hypothetical feature vector -- not tied to any
    real student_id, so any logged-in user (student or admin) may call it.
    This is what powers the "what-if" simulator on the Student Twin page."""
    return _predict(payload.dict())


@app.get("/api/recommend/{student_id}")
def recommend_for_student(student_id: str, user: dict = Depends(auth.get_current_user)):
    auth.require_own_student_or_admin(user, student_id)
    row = _get_student_row(student_id)
    features_row = row[FEATURES].to_dict()
    prediction = _predict(features_row)
    recommendation = _recommend(features_row, prediction)
    return {"student_id": student_id, "prediction": prediction, "recommendation": recommendation}


@app.get("/api/metrics")
def get_metrics(user: dict = Depends(auth.get_current_user)):
    return METRICS


@app.get("/api/cohort_summary")
def cohort_summary(user: dict = Depends(auth.get_current_user)):
    """Cohort-wide stats for the Overview page -- admin only; a single
    student's token has no business seeing the whole cohort's numbers.
    Uses the dataset's real logged gpa/academic_risk columns (not model
    predictions -- computing predictions for all 600 students on every
    page load would be wasteful and these ground-truth numbers are
    equally honest for a cohort-level picture)."""
    auth.require_admin(user)
    students_df = db.get_students_df()
    gpa_counts, gpa_edges = np.histogram(students_df["gpa"], bins=10, range=(0, 10))
    at_risk_ids = (
        students_df[students_df["academic_risk"] == 1]
        .nsmallest(8, "gpa")[["student_id", "gpa", "attendance_pct"]]
        .to_dict(orient="records")
    )
    return {
        "n_students": int(len(students_df)),
        "avg_gpa": round(float(students_df["gpa"].mean()), 2),
        "avg_attendance": round(float(students_df["attendance_pct"].mean()), 1),
        "avg_study_hours": round(float(students_df["study_hours_per_day"].mean()), 2),
        "pct_at_risk": round(float(students_df["academic_risk"].mean()) * 100, 1),
        "gpa_histogram": {
            "bin_edges": [round(float(e), 1) for e in gpa_edges],
            "counts": [int(c) for c in gpa_counts],
        },
        "at_risk_watchlist": at_risk_ids,
    }


@app.get("/api/cohort_aggregate")
def cohort_aggregate(user: dict = Depends(auth.get_current_user)):
    """Aggregate-only cohort stats -- safe for ANY logged-in user (student
    or admin), unlike /api/cohort_summary (admin only), because it contains
    no per-student data at all, just cohort averages. Powers the "how you
    compare" panel on the Student Twin page without leaking anyone's
    individual record to a student account."""
    students_df = db.get_students_df()
    return {
        "n_students": int(len(students_df)),
        "avg_gpa": round(float(students_df["gpa"].mean()), 2),
        "avg_attendance": round(float(students_df["attendance_pct"].mean()), 1),
        "avg_marks": round(float(students_df["avg_marks"].mean()), 1),
        "avg_study_hours": round(float(students_df["study_hours_per_day"].mean()), 2),
        "avg_assignment_completion": round(float(students_df["assignment_completion_pct"].mean()), 1),
        "avg_mood": round(float(students_df["daily_checkin_mood"].mean()), 2),
        "avg_sleep_hours": round(float(students_df["sleep_hours"].mean()), 2),
        "pct_at_risk": round(float(students_df["academic_risk"].mean()) * 100, 1),
    }


@app.post("/api/students/{student_id}/checkin")
def submit_checkin(student_id: str, payload: CheckinRequest, user: dict = Depends(auth.get_current_user)):
    """A real write: a student logs today's mood and sleep hours -- the two
    signals it's realistic to self-report day to day -- and the twin's
    prediction is re-run immediately from the updated row. This is what
    makes it a genuine "digital twin" rather than a static lookup: the
    model's output changes because the underlying data changed, not because
    a different student_id was picked. Persists to the database so the
    change survives a server restart too. Admins may also call this (e.g.
    entering a check-in on a student's behalf).
    """
    auth.require_own_student_or_admin(user, student_id)
    if not (1 <= payload.daily_checkin_mood <= 5):
        raise HTTPException(status_code=422, detail="mood must be between 1 and 5")
    if not (0 <= payload.sleep_hours <= 14):
        raise HTTPException(status_code=422, detail="sleep hours must be between 0 and 14 hours")

    if not db.update_checkin(student_id, payload.daily_checkin_mood, payload.sleep_hours):
        raise HTTPException(status_code=404, detail="student not found")

    row = _get_student_row(student_id)
    features_row = row[FEATURES].to_dict()
    prediction = _predict(features_row)
    # Deliberately NOT calling _recommend() here: it's a potentially slow
    # Gemini round-trip, and the frontend re-fetches the recommendation
    # separately (via GET /api/recommend/{id}) right after a check-in anyway
    # -- so generating one here would just be wasted latency on the "save"
    # button for a value nothing uses.
    return {
        "student_id": student_id,
        "student": row.to_dict(),
        "prediction": prediction,
    }


@app.get("/api/gemini_status")
def gemini_status(user: dict = Depends(auth.get_current_user)):
    return {
        "configured": True,
        "gemini_live": gemini_chat.is_configured(),
    }


def _detect_simulation(msg: str) -> tuple[str, float, str, str] | None:
    feature_matchers = [
        ("study_hours_per_day", ["study", "study hour", "study hours", "study time", "hours of study"], (0.1, 12.0), "h/day", "Study Hours"),
        ("attendance_pct", ["attendance", "attend", "classes"], (10.0, 100.0), "%", "Attendance"),
        ("sleep_hours", ["sleep", "sleeping", "hours of sleep"], (1.0, 14.0), "h/night", "Sleep Duration"),
        ("assignment_completion_pct", ["assignment", "assignments", "homework"], (5.0, 100.0), "%", "Assignment Completion"),
        ("daily_checkin_mood", ["mood", "check-in mood", "checkin mood", "feeling"], (1.0, 5.0), "/5", "Daily Check-in Mood"),
        ("avg_marks", ["marks", "avg marks", "score", "grades", "exam"], (5.0, 100.0), "/100", "Average Marks"),
    ]
    sim_triggers = ["what if", "simulate", "if ", "suppose", "increase", "decrease", "change", "boost", "raise", "drop", "lower", "target"]
    if not any(t in msg for t in sim_triggers):
        return None

    for feat_key, keywords, (min_v, max_v), unit, label in feature_matchers:
        if any(kw in msg for kw in keywords):
            numbers = re.findall(r"\b\d+(?:\.\d+)?\b", msg)
            for n_str in reversed(numbers):
                try:
                    val = float(n_str)
                    if min_v <= val <= max_v:
                        return feat_key, val, unit, label
                except ValueError:
                    continue
    return None


def _calculate_feature_impacts(features_row: dict) -> list[dict]:
    base_pred = _predict(features_row)
    impacts = []
    tests = [
        ("study_hours_per_day", min(8.0, features_row["study_hours_per_day"] + 1.0), "+1h Study Time", "study_hours_per_day", "h/day"),
        ("attendance_pct", min(100.0, features_row["attendance_pct"] + 10.0), "+10% Attendance", "attendance_pct", "%"),
        ("assignment_completion_pct", min(100.0, features_row["assignment_completion_pct"] + 15.0), "+15% Assignments", "assignment_completion_pct", "%"),
        ("sleep_hours", min(9.0, max(7.5, features_row["sleep_hours"] + 1.5)), "7.5h Optimal Sleep", "sleep_hours", "h/night"),
    ]
    for key, val, label, feat, unit in tests:
        test_feat = features_row.copy()
        test_feat[key] = val
        p = _predict(test_feat)
        gpa_gain = round(p["predicted_gpa"] - base_pred["predicted_gpa"], 2)
        risk_drop = round((base_pred["risk_probability"] - p["risk_probability"]) * 100, 1)
        impacts.append({
            "label": label,
            "key": feat,
            "target_val": round(val, 1),
            "unit": unit,
            "gpa_gain": gpa_gain,
            "risk_drop": risk_drop
        })
    impacts.sort(key=lambda x: (x["gpa_gain"], x["risk_drop"]), reverse=True)
    return impacts


def _generate_follow_ups(features_row: dict, prediction: dict, msg: str) -> list[str]:
    at_risk = prediction["at_risk"]
    study = features_row.get("study_hours_per_day", 2.0)
    att = features_row.get("attendance_pct", 75.0)
    
    chips = []
    if at_risk:
        chips.append("🎯 What's the highest-impact change?")
        chips.append(f"⚡ Simulate Study: {min(6.0, round(study + 1.5, 1))}h")
        chips.append("📊 Compare with Cohort Average")
        chips.append("✉️ Draft Check-in Message")
    else:
        chips.append(f"⚡ Simulate Attendance: {min(100.0, round(att + 8.0, 1))}%")
        chips.append("📈 How to push toward higher GPA?")
        chips.append("📊 Compare with Cohort Average")
        chips.append("🔍 Any early warning signs to watch?")
    return chips


def _rule_based_chat(student_id: str, features_row: dict, prediction: dict, message: str, history: list[dict] = None) -> dict:
    msg = message.lower().strip()
    att = float(features_row.get("attendance_pct", 0))
    marks = float(features_row.get("avg_marks", 0))
    study = float(features_row.get("study_hours_per_day", 0))
    assign = float(features_row.get("assignment_completion_pct", 0))
    mood = float(features_row.get("daily_checkin_mood", 0))
    sleep = float(features_row.get("sleep_hours", 0))
    gpa = float(prediction.get("predicted_gpa", 0.0))
    at_risk = bool(prediction.get("at_risk", False))
    risk_prob = float(prediction.get("risk_probability", 0.0))

    words = msg.split()

    # 0. Emotional Wellbeing & Mental Health Support (Reactive Empathy)
    sad_keywords = ["sad", "saf", "unhappy", "depressed", "down", "crying", "miserable", "lonely", "hopeless", "hurt", "grief", "bad day", "awful", "terrible", "sucks", "feel bad", "feeling bad"]
    tired_keywords = ["tired", "exhausted", "sleepy", "fatigue", "fatigued", "burnt out", "burnout", "drained", "can't focus", "no energy", "cant focus", "cant sleep", "can't sleep", "sleep deprived"]
    stress_keywords = ["stressed", "stress", "anxious", "anxiety", "overwhelmed", "panic", "freaking out", "worried", "nervous", "pressure", "too much work"]
    demotivated_keywords = ["lazy", "procrastinating", "no motivation", "don't want to study", "give up", "giving up", "cant do this", "can't do this", "hate this", "why bother"]
    positive_keywords = ["happy", "great", "awesome", "good", "excited", "proud", "feeling good", "doing well", "love this", "feeling better"]

    if any(k in msg for k in sad_keywords) or any(k in words for k in ["sad", "saf"]):
        sleep_comment = f"Looking at your digital twin data, your sleep is recorded at only **{sleep:.1f} hours/night** (with mood check-in at **{mood:.1f}/5**). Severe sleep debt is directly linked to intense feelings of sadness, emotional vulnerability, and brain fog." if sleep < 6.0 else f"Your check-in mood is currently logged at **{mood:.1f}/5**."
        reply = (
            f"I hear you, and I am really sorry you are feeling down right now. ❤️\n\n"
            f"{sleep_comment}\n\n"
            f"When you are carrying a heavy emotional load, trying to force intense academic focus usually leads to frustration. Here is what I strongly suggest for right now:\n\n"
            f"1. **Pause and step back:** Take a genuine break for the next couple of hours. Step away from your computer screen, hydrate, and do something gentle.\n"
            f"2. **Prioritize sleep tonight:** Rest is neurological medicine. Getting 7–8 hours of uninterrupted sleep will reset your emotional regulation center.\n"
            f"3. **Lighten today's goal:** Pick just ONE tiny 15-minute task if you must study today, or give yourself permission to rest completely.\n"
            f"4. **Campus Support:** You don't have to carry this alone. Your university advisors and counseling services are available to help you navigate stressful periods.\n\n"
            f"> *Remember:* Your wellbeing and mental health will always matter infinitely more than any GPA score or coursework deadline."
        )
        return {
            "reply": reply,
            "simulation": None,
            "follow_ups": [
                "💤 How does sleep deprivation affect mood?",
                "✉️ Draft email to professor asking for extension",
                "☕ What is a gentle 15-minute study plan?",
                "📊 Check my current signal health",
            ],
        }

    if any(k in msg for k in tired_keywords):
        reply = (
            f"I hear you loud and clear. Your Digital Twin shows your sleep is at **{sleep:.1f} hours/night**—that is well below the 7–8 hours university students need for healthy cognitive function.\n\n"
            f"When you are operating on a severe sleep deficit:\n"
            f"- Memory consolidation drops by over 30%.\n"
            f"- Problem-solving speed and focus decline sharply.\n"
            f"- Cortisol (stress hormone) spikes, making small tasks feel overwhelming.\n\n"
            f"> **Immediate recommendation:** Do not attempt late-night study sessions today. Power down screens, get 8 hours of sleep tonight, and let your brain recharge. Studying while exhausted yields diminishing returns."
        )
        return {
            "reply": reply,
            "simulation": None,
            "follow_ups": [
                "⚡ Simulate getting 8 hours of sleep",
                "🎯 What's the highest-impact change?",
                "☕ Quick 20-minute power study routine",
                "📊 Compare with Class Average",
            ],
        }

    if any(k in msg for k in stress_keywords):
        reply = (
            f"Take a deep breath. University workload can pile up fast, but you do not need to solve the entire semester today.\n\n"
            f"Here is where you stand right now:\n"
            f"- **Predicted GPA:** {gpa:.2f}/10.0\n"
            f"- **Risk Status:** {'Flagged at-risk (' + str(round(risk_prob*100)) + '%)' if at_risk else 'Safe / On track (' + str(round(risk_prob*100)) + '%)'}\n\n"
            f"**To de-stress right now:**\n"
            f"1. **Brain Dump:** Write down all your deadlines on paper to get them out of your head.\n"
            f"2. **The 5-Minute Rule:** Work on just one pending assignment for exactly 5 minutes. If you want to stop after 5 minutes, you can.\n"
            f"3. **Ask for an extension:** Faculty are very receptive to students who communicate early rather than waiting until after a deadline passes."
        )
        return {
            "reply": reply,
            "simulation": None,
            "follow_ups": [
                "✉️ Draft extension request to professor",
                "🎯 Single highest-impact thing to fix",
                "⚡ Simulate +1h Study Time",
                "📊 Compare with Class Average",
            ],
        }

    if any(k in msg for k in demotivated_keywords):
        reply = (
            f"It is completely normal to have days where you have zero motivation. The secret is that you don't actually need motivation to make progress—you just need tiny momentum:\n\n"
            f"- **The Pomodoro Reset:** Set a timer for 15 minutes. Put your phone in another room and focus on just one problem.\n"
            f"- **Lower the bar:** Opening your textbook or notebook counts as a win. Action creates motivation, not the other way around.\n"
            f"- **Small win:** Clearing even one pending assignment boosts your assignment completion (currently {assign:.1f}%) and lifts your predicted GPA."
        )
        return {
            "reply": reply,
            "simulation": None,
            "follow_ups": [
                "⚡ Simulate completing all assignments",
                "🎯 Highest-impact change",
                "📊 View Signal Health",
                "✉️ Draft Check-in Message",
            ],
        }

    if any(k in msg for k in positive_keywords):
        reply = (
            f"That's wonderful to hear! 🎉 Experiencing high energy and good spirits is the best time to accelerate your learning.\n\n"
            f"Your current trajectory is solid with a predicted GPA of **{gpa:.2f}/10.0**. When your mood and wellness are high, cognitive retention is at its peak.\n\n"
            f"Would you like to explore stretch academic goals, research opportunities, or run simulations to see how high your GPA could go?"
        )
        return {
            "reply": reply,
            "simulation": None,
            "follow_ups": [
                "📈 How could they push toward a higher GPA?",
                "⚡ Simulate 4 hours study",
                "📊 Compare with Class Average",
                "🔍 Any early warning signs to watch for?",
            ],
        }

    # Conversational chit-chat
    if any(k in msg for k in ["how are you", "how are u", "how r u", "hows it going"]):
        reply = (
            f"I'm doing great, thank you for asking! 😊 I'm here monitoring student {student_id}'s Digital Twin data and ready to run live simulations, breakdown risk factors, or help plan your study schedule. How are you feeling today?"
        )
        return {
            "reply": reply,
            "simulation": None,
            "follow_ups": [
                "🎯 What's the highest-impact change?",
                "📊 Compare with Class Average",
                "⚡ Simulate +1.5h Study Time",
                "✉️ Draft Check-in Message",
            ],
        }

    if any(k in msg for k in ["thank you", "thanks", "thx", "appreciate"]):
        reply = (
            f"You're very welcome! I'm always here to support your academic journey. Don't hesitate to check in whenever you need advice, simulations, or study planning."
        )
        return {
            "reply": reply,
            "simulation": None,
            "follow_ups": [
                "🎯 What's the highest-impact change?",
                "📊 Compare with Class Average",
                "⚡ Simulate 85% Attendance",
                "✉️ Draft Check-in Message",
            ],
        }

    # 1. Interactive What-If Simulation
    sim_spec = _detect_simulation(msg)
    if sim_spec:
        feat_key, target_val, unit, feat_label = sim_spec
        old_val = float(features_row.get(feat_key, 0.0))
        hypo_features = features_row.copy()
        hypo_features[feat_key] = target_val
        hypo_pred = _predict(hypo_features)

        old_gpa = gpa
        new_gpa = hypo_pred["predicted_gpa"]
        delta_gpa = round(new_gpa - old_gpa, 2)

        old_risk_pct = round(risk_prob * 100, 1)
        new_risk_pct = round(hypo_pred["risk_probability"] * 100, 1)
        delta_risk_pct = round(new_risk_pct - old_risk_pct, 1)

        gpa_sign = "+" if delta_gpa >= 0 else ""
        risk_sign = "+" if delta_risk_pct >= 0 else ""

        reply = (
            f"⚡ **Live Digital Twin Simulation**\n\n"
            f"Simulating adjustment in **{feat_label}** from **{old_val:.1f}{unit}** ➔ **{target_val:.1f}{unit}**:\n\n"
            f"- **Predicted GPA:** {old_gpa:.2f} ➔ **{new_gpa:.2f}** ({gpa_sign}{delta_gpa})\n"
            f"- **Academic Risk:** {old_risk_pct}% ➔ **{new_risk_pct}%** ({risk_sign}{delta_risk_pct}%)\n"
            f"- **Risk Status:** {'🚨 FLAGGED AT-RISK' if hypo_pred['at_risk'] else '✅ SAFE / ON TRACK'}\n\n"
            f"> *Analysis:* Adjusting {feat_label} to {target_val:.1f}{unit} produces a "
            f"{'positive' if delta_gpa > 0 else 'negative' if delta_gpa < 0 else 'neutral'} impact on the Random Forest models. "
            f"Use the action button below to load this scenario into the Student Twin What-If Panel."
        )
        return {
            "reply": reply,
            "simulation": {
                "feature": feat_key,
                "feature_name": feat_label,
                "old_val": round(old_val, 1),
                "new_val": round(target_val, 1),
                "unit": unit,
                "old_gpa": old_gpa,
                "new_gpa": new_gpa,
                "delta_gpa": delta_gpa,
                "old_risk_pct": old_risk_pct,
                "new_risk_pct": new_risk_pct,
                "delta_risk_pct": delta_risk_pct,
                "old_at_risk": at_risk,
                "new_at_risk": hypo_pred["at_risk"],
            },
            "follow_ups": [
                f"⚡ Simulate Study: {min(6.0, round(study + 1.0, 1))}h",
                "📊 Compare with Class Average",
                "🎯 Highest-Impact Change",
                "✉️ Draft Check-in Message",
            ],
        }

    # 2. Cohort Comparison
    if any(k in msg for k in ["compare", "cohort", "class", "average", "peer", "standing", "rank", "percentile"]):
        students_df = db.get_students_df()
        c_gpa = float(students_df["gpa"].mean())
        c_att = float(students_df["attendance_pct"].mean())
        c_marks = float(students_df["avg_marks"].mean())
        c_study = float(students_df["study_hours_per_day"].mean())
        c_assign = float(students_df["assignment_completion_pct"].mean())
        c_sleep = float(students_df["sleep_hours"].mean())

        diff_gpa = gpa - c_gpa
        diff_att = att - c_att
        diff_marks = marks - c_marks
        diff_study = study - c_study
        diff_assign = assign - c_assign

        reply = (
            f"📊 **Cohort Standing & Benchmark Analysis for {student_id}**\n\n"
            f"Comparing this student's signals against the cohort of 600 peers:\n\n"
            f"| Metric | Student | Class Avg | Difference | Standing |\n"
            f"|---|---|---|---|---|\n"
            f"| **Predicted GPA** | {gpa:.2f} | {c_gpa:.2f} | {'+' if diff_gpa >= 0 else ''}{diff_gpa:.2f} | {'🟢 Above Average' if diff_gpa >= 0 else '🔴 Below Average'} |\n"
            f"| **Attendance** | {att:.1f}% | {c_att:.1f}% | {'+' if diff_att >= 0 else ''}{diff_att:.1f}% | {'🟢 Above Average' if diff_att >= 0 else '🔴 Below Average'} |\n"
            f"| **Average Marks** | {marks:.1f} | {c_marks:.1f} | {'+' if diff_marks >= 0 else ''}{diff_marks:.1f} | {'🟢 Above Average' if diff_marks >= 0 else '🔴 Below Average'} |\n"
            f"| **Study Hours** | {study:.1f}h | {c_study:.1f}h | {'+' if diff_study >= 0 else ''}{diff_study:.1f}h | {'🟢 Above Average' if diff_study >= 0 else '🔴 Below Average'} |\n"
            f"| **Assignments** | {assign:.1f}% | {c_assign:.1f}% | {'+' if diff_assign >= 0 else ''}{diff_assign:.1f}% | {'🟢 Above Average' if diff_assign >= 0 else '🔴 Below Average'} |\n"
            f"| **Sleep** | {sleep:.1f}h | {c_sleep:.1f}h | {'+' if sleep >= c_sleep else ''}{sleep - c_sleep:.1f}h | {'🟢 Healthy' if sleep >= 7.0 else '🟡 Under Target'} |\n\n"
            f"> **Summary:** Student {student_id} is {'outperforming' if diff_gpa >= 0 else 'trailing'} the cohort average by {abs(diff_gpa):.2f} GPA points. "
            f"Their strongest relative signal is {'attendance' if diff_att >= max(diff_study*10, diff_marks) else 'internal marks' if diff_marks >= 0 else 'study time'}."
        )
        return {
            "reply": reply,
            "simulation": None,
            "follow_ups": [
                "🎯 What's the highest-impact change?",
                f"⚡ Simulate Study: {round(c_study + 1.0, 1)}h",
                "🔍 Why is this student flagged?",
                "✉️ Draft Check-in Message",
            ],
        }

    # 3. Why flagged as at-risk / Risk inquiries
    if any(k in msg for k in ["why", "flagged", "at-risk", "at risk", "risk"]):
        if at_risk:
            drivers = []
            if att < 75:
                drivers.append(f"- Low Attendance: {att:.1f}% (below the required 75% threshold)")
            if marks < 60:
                drivers.append(f"- Lower Average Marks: {marks:.1f}/100")
            if study < 2.0:
                drivers.append(f"- Low Study Hours: {study:.1f} hrs/day (cohort average is higher)")
            if assign < 70:
                drivers.append(f"- Incomplete Assignments: {assign:.1f}% completion rate")
            if mood < 3.0:
                drivers.append(f"- Low Mood Check-in: {mood:.1f}/5 indicating possible stress or fatigue")
            if sleep < 6.0:
                drivers.append(f"- Insufficient Sleep: {sleep:.1f} hrs/night")
            if not drivers:
                drivers.append(f"- Combination of borderline metrics across study hours ({study:.1f}h) and assignments ({assign:.1f}%)")

            reasons_str = "\n".join(drivers)
            reply = (
                f"Student {student_id} is flagged as academically at-risk with a {risk_prob:.0%} risk probability and a predicted GPA of {gpa:.2f}.\n\n"
                f"Primary contributing factors identified by the Random Forest model:\n{reasons_str}\n\n"
                f"Recommended action: Address the lowest metrics first, particularly attendance and study hours, to bring the risk probability below the threshold."
            )
            return {
                "reply": reply,
                "simulation": None,
                "follow_ups": [
                    "🎯 What's the highest-impact change?",
                    f"⚡ Simulate Study: {min(6.0, round(study + 1.5, 1))}h",
                    "📊 Compare with Cohort Average",
                    "✉️ Draft Check-in Message",
                ],
            }
        else:
            positives = []
            if att >= 80: positives.append(f"strong attendance ({att:.1f}%)")
            if marks >= 70: positives.append(f"solid average marks ({marks:.1f}/100)")
            if study >= 2.5: positives.append(f"consistent study schedule ({study:.1f} hrs/day)")
            if assign >= 80: positives.append(f"high assignment completion ({assign:.1f}%)")
            pos_str = ", ".join(positives) if positives else "consistent behavioral indicators"
            reply = (
                f"Student {student_id} is currently NOT flagged at-risk. The model estimates only a {risk_prob:.0%} risk probability with a predicted GPA of {gpa:.2f}.\n\n"
                f"Key protective factors include {pos_str}. They are in good academic standing."
            )
            return {
                "reply": reply,
                "simulation": None,
                "follow_ups": [
                    "📈 How could they push toward a higher GPA?",
                    f"⚡ Simulate Study: {min(6.0, round(study + 1.0, 1))}h",
                    "📊 Compare with Cohort Average",
                    "🔍 Any early warning signs to watch for?",
                ],
            }

    # 4. Highest-impact change / Sensitivity test
    if any(k in msg for k in ["highest-impact", "highest impact", "single change", "most impact", "what should i change", "how to improve", "best change", "what can i do", "what to do", "leverage"]):
        impacts = _calculate_feature_impacts(features_row)
        top = impacts[0]
        rows_str = "\n".join([
            f"{i+1}. **{imp['label']}** (target: {imp['target_val']}{imp['unit']}): **+{imp['gpa_gain']} GPA** (Risk: -{imp['risk_drop']}%)"
            for i, imp in enumerate(impacts)
        ])
        reply = (
            f"🎯 **Ranked Impact Analysis for {student_id}**\n\n"
            f"Testing model sensitivity across all behavioral signals for this student's profile:\n\n"
            f"{rows_str}\n\n"
            f"**Single highest-impact recommendation:**\n"
            f"> **Focus on {top['label']} (targeting {top['target_val']}{top['unit']})**.\n\n"
            f"This intervention provides the steepest return in expected GPA (+{top['gpa_gain']}) and reduces academic risk by {top['risk_drop']}%. "
            f"You can apply this simulation directly using the button below."
        )
        return {
            "reply": reply,
            "simulation": {
                "feature": top["key"],
                "feature_name": top["label"],
                "old_val": round(float(features_row.get(top["key"], 0)), 1),
                "new_val": top["target_val"],
                "unit": top["unit"],
                "old_gpa": gpa,
                "new_gpa": round(gpa + top["gpa_gain"], 2),
                "delta_gpa": top["gpa_gain"],
                "old_risk_pct": round(risk_prob * 100, 1),
                "new_risk_pct": max(0.0, round((risk_prob * 100) - top["risk_drop"], 1)),
                "delta_risk_pct": -top["risk_drop"],
                "old_at_risk": at_risk,
                "new_at_risk": (risk_prob * 100 - top["risk_drop"]) >= (RISK_THRESHOLD * 100),
            },
            "follow_ups": [
                f"⚡ Simulate {top['label']}",
                "📊 Compare with Class Average",
                "📈 How to reach GPA 8.5?",
                "✉️ Draft Check-in Message",
            ],
        }

    # 5. Draft a check-in message
    if any(k in msg for k in ["draft", "message", "email", "reach out", "check-in message", "contact"]):
        tone = "supportive and encouraging" if at_risk else "motivating and praise-oriented"
        if at_risk:
            body = (
                f"Dear {student_id},\n\n"
                f"I hope you're doing well. I wanted to reach out because our course dashboard noticed you might be facing a demanding stretch recently "
                f"(attendance is around {att:.1f}% and sleep is ~{sleep:.1f} hrs/night). "
                f"Your predicted GPA is {gpa:.2f}, and I want to make sure you have all the support you need to succeed.\n\n"
                f"Please let me know if you would like to go over assignment backlog or need any study resources. "
                f"I'm here to help you get back on track whenever you have a few minutes to connect.\n\n"
                f"Best regards,\nYour Academic Advisor"
            )
        else:
            body = (
                f"Dear {student_id},\n\n"
                f"Great job on your consistent effort this term! Your attendance is at {att:.1f}%, assignment completion is {assign:.1f}%, "
                f"and your current predicted GPA is looking strong at {gpa:.2f}.\n\n"
                f"Keep up the excellent habits! Let me know if you'd like to explore any advanced coursework, research topics, or placement preparation.\n\n"
                f"Best regards,\nYour Academic Advisor"
            )
        reply = f"Here is a draft check-in message tailored for {student_id} ({tone}):\n\n```text\n{body}\n```"
        return {
            "reply": reply,
            "simulation": None,
            "follow_ups": [
                "🎯 What's the highest-impact change?",
                f"⚡ Simulate Study: {min(6.0, round(study + 1.0, 1))}h",
                "📊 Compare with Class Average",
                "🔍 Early Warning Signs",
            ],
        }

    # 6. What's helping stay on track / Strengths
    if any(k in msg for k in ["on track", "strength", "positive", "doing well", "helping"]):
        strengths = []
        if att >= 75: strengths.append(f"- Attendance: {att:.1f}% meets university eligibility standards.")
        if marks >= 60: strengths.append(f"- Internal Marks: {marks:.1f}/100 provides a reliable baseline.")
        if study >= 2.0: strengths.append(f"- Study Hours: {study:.1f} hrs/day shows dedicated effort.")
        if assign >= 75: strengths.append(f"- Assignments: {assign:.1f}% completion prevents credit penalties.")
        if sleep >= 6.5: strengths.append(f"- Sleep: {sleep:.1f} hrs/night supports cognitive endurance.")
        if mood >= 3.0: strengths.append(f"- Check-in Mood: {mood:.1f}/5 indicates positive mental readiness.")
        if not strengths:
            strengths.append(f"- Commitment to daily check-ins: logging mood ({mood:.1f}/5) and sleep ({sleep:.1f}h) regularly.")

        reply = (
            f"Here are the key strengths supporting {student_id} (Predicted GPA: {gpa:.2f}):\n\n"
            + "\n".join(strengths) +
            f"\n\nMaintaining these habits keeps their risk profile low ({risk_prob:.0%} risk probability)."
        )
        return {
            "reply": reply,
            "simulation": None,
            "follow_ups": [
                "📈 How could they push toward a higher GPA?",
                f"⚡ Simulate Study: {min(6.0, round(study + 1.5, 1))}h",
                "📊 Compare with Cohort Average",
                "🔍 Any early warning signs to watch for?",
            ],
        }

    # 7. Push toward higher GPA
    if any(k in msg for k in ["higher gpa", "push", "boost gpa", "increase gpa", "target gpa"]):
        next_target = min(10.0, round(gpa + 0.8, 1))
        tips = []
        if study < 3.5: tips.append(f"- Study Time: Increase from {study:.1f}h to {min(4.5, study + 1.0):.1f}h per day.")
        if marks < 85: tips.append(f"- Marks: Target 80+ in upcoming module assessments (currently {marks:.1f}).")
        if assign < 95: tips.append(f"- Assignment Submissions: Aim for 95%+ completion (currently {assign:.1f}%).")
        if sleep < 7.0: tips.append(f"- Consistent Rest: Prioritize 7-8 hours of sleep ({sleep:.1f}h now) for optimal retention.")
        reply = (
            f"To push {student_id}'s predicted GPA from {gpa:.2f} toward ~{next_target:.1f}:\n\n"
            + "\n".join(tips) +
            f"\n\nYou can also test these adjustments interactively in the 'What-If Simulator' on the Student Twin page to see immediate model re-evaluations."
        )
        return {
            "reply": reply,
            "simulation": None,
            "follow_ups": [
                f"⚡ Simulate Study: {min(6.0, round(study + 1.0, 1))}h",
                "🎯 What's the highest-impact change?",
                "📊 Compare with Class Average",
                "✉️ Draft Check-in Message",
            ],
        }

    # 8. Early warning signs
    if any(k in msg for k in ["warning", "early warning", "sign", "watch for", "red flag"]):
        flags = []
        if att < 80: flags.append(f"- Attendance is {att:.1f}% (risk increases sharply if it drops below 75%).")
        if assign < 80: flags.append(f"- Assignment completion is {assign:.1f}% (late submissions may hurt internals).")
        if sleep < 6.5: flags.append(f"- Sleep duration of {sleep:.1f}h/night puts the student at risk of cognitive fatigue.")
        if mood < 3.0: flags.append(f"- Average mood score of {mood:.1f}/5 signals potential burnout.")
        if not flags:
            flags.append("- No critical warnings detected at this time! Signals are well within safe thresholds.")
        reply = (
            f"Early warning indicators for {student_id}:\n\n"
            + "\n".join(flags) +
            f"\n\nRegular daily check-ins help the digital twin detect downward trends before they impact term results."
        )
        return {
            "reply": reply,
            "simulation": None,
            "follow_ups": [
                "🎯 What's the highest-impact change?",
                f"⚡ Simulate Study: {min(6.0, round(study + 1.0, 1))}h",
                "📊 Compare with Class Average",
                "✉️ Draft Check-in Message",
            ],
        }

    # 9. Specific metric inquiries
    if "attendance" in msg:
        status = "satisfactory" if att >= 75 else "below recommended 75% threshold"
        reply = f"{student_id}'s attendance is currently {att:.1f}%, which is {status}. Maintaining or raising this ensures course eligibility and supports higher test scores."
        return {
            "reply": reply,
            "simulation": None,
            "follow_ups": [
                "⚡ Simulate Attendance: 85%",
                "🎯 What's the highest-impact change?",
                "📊 Compare with Cohort Average",
            ],
        }

    if any(k in msg for k in ["marks", "grade", "score"]):
        reply = f"{student_id}'s average marks across assessments are {marks:.1f}/100. This is a primary driver in their predicted GPA of {gpa:.2f}."
        return {
            "reply": reply,
            "simulation": None,
            "follow_ups": [
                "⚡ Simulate Marks: 85",
                "📈 How to push toward higher GPA?",
                "📊 Compare with Class Average",
            ],
        }

    if any(k in msg for k in ["study", "hour"]):
        reply = f"{student_id} is currently logging an average of {study:.1f} study hours per day. For substantial GPA gains, students in this cohort benefit from 2.5 to 3.5 focused hours daily."
        return {
            "reply": reply,
            "simulation": None,
            "follow_ups": [
                f"⚡ Simulate Study: {round(study + 1.0, 1)}h",
                "🎯 What's the highest-impact change?",
                "📊 Compare with Cohort Average",
            ],
        }

    # 10. Greetings & identity
    if any(w in msg.split() for w in ["hi", "hello", "hey", "greetings", "help"]):
        reply = (
            f"Hello! I am the Digital Student Twin AI Assistant for student {student_id}.\n\n"
            f"- **Predicted GPA:** {gpa:.2f}/10.0\n"
            f"- **Academic Risk:** {'FLAGGED AT-RISK' if at_risk else 'Safe / Not at-risk'} ({risk_prob:.0%})\n"
            f"- **Signals:** Attendance {att:.1f}% | Study {study:.1f}h/day | Sleep {sleep:.1f}h\n\n"
            f"Try asking: *'What if I study 4 hours?'*, *'Compare me to the class'*, or *'What is the highest-impact change?'*"
        )
        return {
            "reply": reply,
            "simulation": None,
            "follow_ups": [
                "🎯 What's the highest-impact change?",
                f"⚡ Simulate Study: {min(6.0, round(study + 1.5, 1))}h",
                "📊 Compare with Cohort Average",
                "✉️ Draft Check-in Message",
            ],
        }

    # General fallback
    reply = (
        f"Based on student {student_id}'s Digital Twin data:\n\n"
        f"- Current Prediction: GPA {gpa:.2f}/10.0, Risk Probability: {risk_prob:.0%}\n"
        f"- Key Signals: Attendance {att:.1f}%, Avg Marks {marks:.1f}/100, Study {study:.1f}h/day, Assignments {assign:.1f}%, Sleep {sleep:.1f}h/night, Mood {mood:.1f}/5\n\n"
        f"To improve this student's trajectory, the highest leverage area is raising their {'attendance' if att < 75 else 'study hours' if study < 2.5 else 'assignment completion'}."
    )
    return {
        "reply": reply,
        "simulation": None,
        "follow_ups": [
            "🎯 What's the highest-impact change?",
            f"⚡ Simulate Study: {min(6.0, round(study + 1.0, 1))}h",
            "📊 Compare with Cohort Average",
            "✉️ Draft Check-in Message",
        ],
    }


@app.post("/api/chat")
def chat(payload: ChatRequest, user: dict = Depends(auth.get_current_user)):
    """Interactive free-form chat with live model simulation and dynamic follow-up chips."""
    auth.require_own_student_or_admin(user, payload.student_id)
    row = _get_student_row(payload.student_id)
    features_row = row[FEATURES].to_dict()
    prediction = _predict(features_row)

    if gemini_chat.is_configured():
        try:
            reply = gemini_chat.chat_reply(
                features_row, prediction, [t.dict() for t in payload.history], payload.message
            )
            follow_ups = _generate_follow_ups(features_row, prediction, payload.message)
            return {
                "student_id": payload.student_id,
                "reply": reply,
                "simulation": None,
                "follow_ups": follow_ups,
                "available": True,
                "source": "gemini",
            }
        except Exception:
            logger.exception("Gemini chat failed, falling back to twin engine")

    result = _rule_based_chat(payload.student_id, features_row, prediction, payload.message, [t.dict() for t in payload.history])
    return {
        "student_id": payload.student_id,
        "reply": result["reply"],
        "simulation": result.get("simulation"),
        "follow_ups": result.get("follow_ups", []),
        "available": True,
        "source": "twin_engine",
    }


class SetKeyRequest(BaseModel):
    api_key: str


@app.post("/api/set_gemini_key")
def set_gemini_key(payload: SetKeyRequest, user: dict = Depends(auth.get_current_user)):
    import os
    key = payload.api_key.strip()
    os.environ["GEMINI_API_KEY"] = key
    gemini_chat._client = None
    gemini_chat._working_model = None
    gemini_chat._consecutive_failures = 0
    gemini_chat._cooldown_until = 0.0

    env_path = os.path.join(os.path.dirname(__file__), ".env")
    lines = []
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            lines = [l for l in f.readlines() if not l.startswith("GEMINI_API_KEY=")]
    lines.append(f"GEMINI_API_KEY={key}\n")
    with open(env_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    return {"configured": bool(key), "message": "Gemini API Key configured successfully!"}
