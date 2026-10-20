"""
db.py
Database layer for the ALT backend (SQLAlchemy Core).

Set DATABASE_URL to use PostgreSQL (e.g. Render's managed Postgres):
    DATABASE_URL=postgresql://user:pass@host:5432/dbname
If it isn't set, falls back to a local SQLite file (alt.db) so the project
still runs with zero setup on a laptop. Both go through the same code.

On first start the tables are created and seeded from the original
student_data.csv and users.json (bcrypt hashes only), so a fresh deploy
comes up with the same 600 students and 4 demo accounts. After that, the
database is the source of truth -- check-ins are real UPDATEs, not CSV
rewrites.
"""
import json
import os

import pandas as pd
from sqlalchemy import (Column, Float, Integer, MetaData, String, Table,
                        create_engine, func, select, update)

_url = os.environ.get("DATABASE_URL", "sqlite:///alt.db")
# Render/Heroku hand out "postgres://..." which SQLAlchemy 1.4+ rejects.
# Also pin the psycopg2 driver (what requirements.txt installs); SQLAlchemy 2
# would otherwise look for the newer psycopg v3 package.
if _url.startswith("postgres://"):
    _url = _url.replace("postgres://", "postgresql://", 1)
if _url.startswith("postgresql://"):
    _url = _url.replace("postgresql://", "postgresql+psycopg2://", 1)

engine = create_engine(_url, pool_pre_ping=True, future=True)
metadata = MetaData()

students = Table(
    "students", metadata,
    Column("student_id", String(16), primary_key=True),
    Column("attendance_pct", Float, nullable=False),
    Column("avg_marks", Float, nullable=False),
    Column("study_hours_per_day", Float, nullable=False),
    Column("assignment_completion_pct", Float, nullable=False),
    Column("daily_checkin_mood", Float, nullable=False),
    Column("sleep_hours", Float, nullable=False),
    Column("gpa", Float, nullable=False),
    Column("academic_risk", Integer, nullable=False),
)

users = Table(
    "users", metadata,
    Column("username", String(64), primary_key=True),
    Column("password_hash", String(128), nullable=False),
    Column("role", String(16), nullable=False),
    Column("student_id", String(16), nullable=True),
    Column("display_name", String(128), nullable=False),
)

STUDENT_COLUMNS = [c.name for c in students.columns]


def init_db() -> None:
    """Create tables and seed them from the CSV / users.json if empty."""
    metadata.create_all(engine)
    with engine.begin() as conn:
        if conn.execute(select(func.count()).select_from(students)).scalar() == 0:
            df = pd.read_csv("student_data.csv")[STUDENT_COLUMNS]
            conn.execute(students.insert(), df.to_dict(orient="records"))
        if conn.execute(select(func.count()).select_from(users)).scalar() == 0:
            with open("users.json") as f:
                conn.execute(users.insert(), json.load(f))


def get_students_df() -> pd.DataFrame:
    """All students as a DataFrame (600 rows -- cheap enough per request)."""
    with engine.connect() as conn:
        rows = conn.execute(select(students).order_by(students.c.student_id)).mappings().all()
    return pd.DataFrame(rows, columns=STUDENT_COLUMNS)


def get_student(student_id: str) -> dict | None:
    with engine.connect() as conn:
        row = conn.execute(
            select(students).where(students.c.student_id == student_id)
        ).mappings().first()
    return dict(row) if row else None


def update_checkin(student_id: str, mood: float, sleep_hours: float) -> bool:
    with engine.begin() as conn:
        result = conn.execute(
            update(students)
            .where(students.c.student_id == student_id)
            .values(daily_checkin_mood=mood, sleep_hours=sleep_hours)
        )
    return result.rowcount > 0


def get_user(username: str) -> dict | None:
    with engine.connect() as conn:
        row = conn.execute(
            select(users).where(users.c.username == username)
        ).mappings().first()
    return dict(row) if row else None
