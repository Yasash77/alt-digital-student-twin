"""
create_users.py
One-time (re-runnable) script that builds users.json: the demo user store
for the ALT prototype's login system.

Passwords are bcrypt-hashed here and only the hashes are written to disk --
app.py/auth.py never see or store a plaintext password. Re-run this script
any time you want to change the demo accounts or reset a password.

Demo accounts (documented in README.md too):
  admin    / admin123        -> role "admin", full access to every page
  s1000    / student123       -> role "student", student_id S1000 (GPA ~8.1, on track)
  s1182    / student123       -> role "student", student_id S1182 (GPA ~6.8, mid-range)
  s1093    / student123       -> role "student", student_id S1093 (GPA ~2.9, flagged at-risk)
"""
import json

import bcrypt


def _hash(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


USERS = [
    {"username": "admin", "password": "admin123", "role": "admin", "student_id": None, "display_name": "Faculty Admin"},
    {"username": "s1000", "password": "student123", "role": "student", "student_id": "S1000", "display_name": "Student S1000"},
    {"username": "s1182", "password": "student123", "role": "student", "student_id": "S1182", "display_name": "Student S1182"},
    {"username": "s1093", "password": "student123", "role": "student", "student_id": "S1093", "display_name": "Student S1093"},
]


def main():
    out = []
    for u in USERS:
        out.append({
            "username": u["username"],
            "password_hash": _hash(u["password"]),
            "role": u["role"],
            "student_id": u["student_id"],
            "display_name": u["display_name"],
        })
    with open("users.json", "w") as f:
        json.dump(out, f, indent=2)
    print(f"Wrote {len(out)} users to users.json")


if __name__ == "__main__":
    main()
