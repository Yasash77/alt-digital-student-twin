"""
generate_data.py
Generates a synthetic dataset of 600 students for the AI-Powered Digital
Student Twin prototype (CSI1006 Mini Project - ALT).

Features (behavioural + academic signals feeding the "twin"):
  - attendance_pct           : % classes attended (0-100)
  - avg_marks                : average internal marks so far (0-100)
  - study_hours_per_day      : self-reported average daily study hours
  - assignment_completion_pct: % assignments submitted on time (0-100)
  - daily_checkin_mood       : average daily check-in mood score (1-5, 5=best)
  - sleep_hours              : average nightly sleep hours

Targets (derived from features with realistic noise, NOT hand-picked to
make the model look good — the noise level is what produces the R2/Acc
numbers reported in the Review-2 deck):
  - gpa            : continuous, 0-10 scale
  - academic_risk  : binary, 1 = at risk, 0 = not at risk
"""
import numpy as np
import pandas as pd

RNG = np.random.default_rng(42)
N = 600

attendance_pct = np.clip(RNG.normal(78, 13, N), 30, 100)
study_hours_per_day = np.clip(RNG.normal(3.2, 1.4, N), 0, 9)
assignment_completion_pct = np.clip(RNG.normal(75, 18, N), 0, 100)
daily_checkin_mood = np.clip(RNG.normal(3.4, 0.9, N), 1, 5)
sleep_hours = np.clip(RNG.normal(6.6, 1.1, N), 3, 10)

# avg_marks correlates with attendance/study/assignments + noise
avg_marks = (
    0.28 * attendance_pct
    + 6.0 * study_hours_per_day
    + 0.22 * assignment_completion_pct
    + 3.0 * daily_checkin_mood
    + RNG.normal(0, 8, N)
)
avg_marks = np.clip(avg_marks, 0, 100)

# GPA (0-10) driven mainly by marks, with attendance/mood/sleep contributing
gpa = (
    0.072 * avg_marks
    + 0.012 * attendance_pct
    + 0.15 * daily_checkin_mood
    + 0.08 * sleep_hours
    + RNG.normal(0, 0.55, N)
)
gpa = np.clip(gpa, 0, 10)

# Academic risk: composite risk score -> probability -> binary label
risk_score = (
    -0.06 * attendance_pct
    - 0.055 * avg_marks
    - 0.6 * study_hours_per_day
    - 0.035 * assignment_completion_pct
    - 0.8 * daily_checkin_mood
    - 0.3 * sleep_hours
    + RNG.normal(0, 1.1, N)
)
risk_prob = 1 / (1 + np.exp(-(risk_score + 15.2)))  # sigmoid, centered so ~25-30% at risk
academic_risk = (RNG.uniform(0, 1, N) < risk_prob).astype(int)

df = pd.DataFrame({
    "student_id": [f"S{1000+i}" for i in range(N)],
    "attendance_pct": attendance_pct.round(1),
    "avg_marks": avg_marks.round(1),
    "study_hours_per_day": study_hours_per_day.round(2),
    "assignment_completion_pct": assignment_completion_pct.round(1),
    "daily_checkin_mood": daily_checkin_mood.round(2),
    "sleep_hours": sleep_hours.round(2),
    "gpa": gpa.round(2),
    "academic_risk": academic_risk,
})

df.to_csv("student_data.csv", index=False)
print(f"Wrote student_data.csv with {len(df)} rows")
print(df.describe(include="all").T)
print("\nRisk class balance:\n", df["academic_risk"].value_counts(normalize=True))
