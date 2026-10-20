"""
auth.py
Real backend authentication for the ALT prototype: bcrypt-hashed passwords
(users table in the database, seeded from users.json -- see
create_users.py for the demo accounts) + signed JWT access tokens (PyJWT), checked on every protected
API route via FastAPI dependencies.

This is a genuine login system, appropriately scoped for a course
prototype: and a fixed demo SECRET_KEY unless AUTH_SECRET_KEY is set (always set it in production). It is NOT what should protect
real student records in production -- see the "Security notes" section in
README.md. It IS real hashing, real signature verification, and real
per-request authorization (a student token literally cannot fetch another
student's data -- the API enforces it, not just the UI).
"""
import os
import time

import bcrypt
import jwt
from fastapi import Header, HTTPException

import db

SECRET_KEY = os.environ.get("AUTH_SECRET_KEY", "alt-prototype-demo-secret-change-me")
ALGORITHM = "HS256"
TOKEN_TTL_SECONDS = 12 * 60 * 60  # 12 hours -- long enough to survive a whole demo/review

def authenticate(username: str, password: str) -> dict:
    """Returns the user record on success, raises HTTPException(401) on failure."""
    user = db.get_user(username.strip().lower())
    if not user or not bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return user


def issue_token(user: dict) -> str:
    now = int(time.time())
    payload = {
        "sub": user["username"],
        "role": user["role"],
        "student_id": user["student_id"],
        "display_name": user["display_name"],
        "iat": now,
        "exp": now + TOKEN_TTL_SECONDS,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def _decode(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Session expired, please log in again")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid session token")


def get_current_user(authorization: str | None = Header(default=None)) -> dict:
    """FastAPI dependency: extracts + verifies the Bearer token, returns the
    decoded claims (sub/role/student_id/display_name). Raises 401 if
    missing/invalid/expired -- use as `user = Depends(get_current_user)`.
    """
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = authorization.split(" ", 1)[1].strip()
    return _decode(token)


def require_admin(user: dict) -> None:
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")


def require_own_student_or_admin(user: dict, student_id: str) -> None:
    """Admins may access any student; a student token may only access its
    own student_id. This is the actual authorization check -- it runs
    server-side on every relevant route, so a student can't just edit the
    URL/dropdown to see someone else's record."""
    if user["role"] == "admin":
        return
    if user["role"] == "student" and user.get("student_id") == student_id:
        return
    raise HTTPException(status_code=403, detail="Not authorized for this student's data")
