"""
gemini_chat.py
Thin wrapper around the Google Gemini API for the ALT prototype's
"AI chatbot" milestone -- replaces the rule-based recommendation engine
with real generated guidance, and adds a free-form chat endpoint.

Design goals (this runs live, in front of an examiner, on conference wifi):
  - NEVER let a Gemini failure break the dashboard. Every public function
    here either returns a good result or raises; app.py always wraps calls
    in try/except and falls back to the rule-based engine (see app.py's
    _rule_based_recommend). The UI marks which one actually produced the
    text it's showing ("source": "gemini" | "rule_based"), so nothing is
    silently faked.
  - Try more than one model id. Gemini model names change fairly often
    (flash-lite / flash / pro tiers get renamed across versions); trying a
    short list in order means one renamed/retired id doesn't take the
    whole feature down.
  - Keep prompts small and ask for structured JSON output (a Pydantic
    schema via response_schema) rather than parsing freeform text --
    much less likely to break the UI on an odd response shape.
"""
import os
import time

from google import genai
from google.genai import types
from pydantic import BaseModel

# Tried in order; prioritized Gemini Thinking AI models for deep reasoning.
MODEL_CANDIDATES = [
    "gemini-2.0-flash-thinking-exp-01-21",
    "gemini-2.0-flash-thinking-exp",
    "gemini-2.5-pro",
    "gemini-2.0-pro-exp-02-05",
    "gemini-2.0-flash",
    "gemini-1.5-pro",
]

_client = None
_working_model = None  # remembered once one candidate succeeds, to skip retrying the rest

# --- Circuit breaker -------------------------------------------------------
# If the configured key/network is broken (e.g. an invalid key, or a Google
# account/region issue), every single call would otherwise retry all of
# MODEL_CANDIDATES over the network before giving up -- adding real,
# user-visible latency to every recommendation/chat request, forever. Once
# we've seen a few failures in a row, stop attempting the network entirely
# for a cooldown window and fail straight to the rule-based fallback. A
# single success (e.g. the key gets fixed) immediately clears this.
_FAILURE_THRESHOLD = 2       # consecutive failed calls before the breaker trips
_COOLDOWN_SECONDS = 60       # how long to skip network attempts once tripped
_consecutive_failures = 0
_cooldown_until = 0.0        # time.monotonic() timestamp; 0 = not tripped


def is_configured() -> bool:
    return bool(os.environ.get("GEMINI_API_KEY"))



# Every Gemini call gets a hard timeout. Without this, a network that just
# hangs (rather than failing fast with a clean error -- which is what this
# sandbox's network happens to do, but a real campus/home network is under
# no obligation to) blocks the request indefinitely. Since the dashboard
# awaits the recommendation before rendering anything else on the page, an
# indefinite hang here looks exactly like "the page is stuck loading" to
# the person using it -- this is what actually causes that, not a frontend
# bug. 8s per model attempt, up to 3 candidates tried in _call_with_fallback,
# so worst case ~24s before falling back to the rule-based engine on a
# fully dead connection -- and the circuit breaker (below) means only the
# very first request(s) ever pay that cost.
_GEMINI_TIMEOUT_MS = 8000


def _get_client() -> genai.Client:
    global _client
    if _client is None:
        _client = genai.Client(
            api_key=os.environ["GEMINI_API_KEY"],
            http_options=types.HttpOptions(timeout=_GEMINI_TIMEOUT_MS),
        )
    return _client


class RecommendationOut(BaseModel):
    headline: str
    tips: list[str]


def _student_context(features_row: dict, prediction: dict) -> str:
    return (
        f"Attendance: {features_row['attendance_pct']:.1f}%\n"
        f"Average marks: {features_row['avg_marks']:.1f}/100\n"
        f"Study hours/day: {features_row['study_hours_per_day']:.2f}\n"
        f"Assignment completion: {features_row['assignment_completion_pct']:.1f}%\n"
        f"Daily check-in mood (1-5): {features_row['daily_checkin_mood']:.2f}\n"
        f"Sleep hours/night: {features_row['sleep_hours']:.2f}\n"
        f"Model-predicted GPA (0-10): {prediction['predicted_gpa']}\n"
        f"Model-predicted academic-risk probability: {prediction['risk_probability']:.0%}"
        f" ({'FLAGGED at-risk' if prediction['at_risk'] else 'not flagged at-risk'})"
    )


def _call_with_fallback(contents: str, config: "types.GenerateContentConfig | None" = None):
    """Try each candidate model in turn; remember the first that works.

    Wrapped in a small circuit breaker (see module-level state above): if
    Gemini has failed several times in a row, skip the network attempts
    entirely for a cooldown window and fail immediately so the caller (and
    the UI) doesn't pay the retry latency on every single request.
    """
    global _working_model, _consecutive_failures, _cooldown_until

    now = time.monotonic()
    if _cooldown_until and now < _cooldown_until:
        remaining = round(_cooldown_until - now, 1)
        raise RuntimeError(
            f"Gemini circuit breaker open ({_consecutive_failures} recent failures); "
            f"skipping network attempt for {remaining}s"
        )

    client = _get_client()
    order = [_working_model] + [m for m in MODEL_CANDIDATES if m != _working_model] \
        if _working_model else MODEL_CANDIDATES
    last_err = None
    for model in order:
        try:
            response = client.models.generate_content(model=model, contents=contents, config=config)
            _working_model = model
            _consecutive_failures = 0
            _cooldown_until = 0.0
            return response
        except Exception as e:  # noqa: BLE001 -- deliberately broad, see module docstring
            last_err = e
            continue

    _consecutive_failures += 1
    if _consecutive_failures >= _FAILURE_THRESHOLD:
        _cooldown_until = time.monotonic() + _COOLDOWN_SECONDS
    raise RuntimeError(f"all Gemini model candidates failed: {last_err}")


def generate_recommendation(features_row: dict, prediction: dict) -> dict:
    """Returns {"headline": str, "tips": [str, ...], "source": "gemini"}.
    Raises on any failure -- caller (app.py) catches and falls back.
    """
    prompt = (
        "You are an academic mentor AI inside a university 'digital student twin' "
        "dashboard. Given one student's behavioural and academic signals plus a "
        "machine-learning model's GPA/risk prediction, write a short, encouraging, "
        "specific recommendation. Do not repeat the raw numbers back verbatim; "
        "interpret them. Give 2-4 concrete, actionable tips, ordered by impact.\n\n"
        f"Student data:\n{_student_context(features_row, prediction)}"
    )
    response = _call_with_fallback(
        prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=RecommendationOut,
        ),
    )
    parsed = getattr(response, "parsed", None)
    if parsed is None:
        import json
        parsed = RecommendationOut(**json.loads(response.text))
    return {"headline": parsed.headline, "tips": parsed.tips, "source": "gemini"}


def chat_reply(features_row: dict, prediction: dict, history: list[dict], message: str) -> str:
    """Free-form Q&A powered by Gemini Thinking AI with deep cognitive reasoning. `history` is a list of
    {"role": "user"|"model", "text": str} from earlier turns in this
    session (kept client-side by the dashboard, not persisted server-side).
    """
    system_context = (
        "You are an academic mentor AI powered by Google's Gemini Thinking AI inside a university 'digital student twin' "
        "dashboard. Think through the student's behavioural signals (sleep, mood, attendance, study hours) and their "
        "impact on the machine learning GPA trajectory before formulating your response. "
        "Be analytical yet encouraging, concise (2-5 sentences unless asked for deeper breakdowns), and grounded strictly in their data. "
        "Never invent data not provided below.\n\n"
        f"Student data:\n{_student_context(features_row, prediction)}"
    )
    contents = [types.Content(role="user", parts=[types.Part(text=system_context)])]
    contents.append(types.Content(
        role="model",
        parts=[types.Part(text="Understood — I'll analyze this student's digital twin signals deeply using Gemini Thinking AI reasoning.")],
    ))
    for turn in history[-10:]:  # cap context sent, keep it cheap
        role = "user" if turn.get("role") == "user" else "model"
        contents.append(types.Content(role=role, parts=[types.Part(text=turn.get("text", ""))]))
    contents.append(types.Content(role="user", parts=[types.Part(text=message)]))

    # Enable cognitive thinking budget for deeper reasoning
    thinking_cfg = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=1024)
    )
    try:
        response = _call_with_fallback(contents, config=thinking_cfg)
    except Exception:
        # Fallback to standard generation if the selected tier doesn't accept thinking_budget
        response = _call_with_fallback(contents)
    return response.text
