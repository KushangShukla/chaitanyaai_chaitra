import os
import hashlib
from datetime import datetime, timedelta, timezone
from fastapi import FastAPI
from fastapi import Header
from backend.routes.query import router as query_router
from backend.routes.predict import router as predict_router

from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import jwt


app = FastAPI(title="CHAITRA AI API")
JWT_SECRET = os.getenv("JWT_SECRET", "chaitra_dev_secret_change_me")
JWT_ALGORITHM = "HS256"
JWT_EXPIRY_HOURS = int(os.getenv("JWT_EXPIRY_HOURS", "24"))


# =========================
#  DATABASE CONNECTION
# =========================
def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB", "chaitra_db"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "root64"),
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432")
    )


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def create_access_token(payload: dict) -> str:
    exp = datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRY_HOURS)
    token_payload = {**payload, "exp": exp}
    return jwt.encode(token_payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def get_current_user(authorization: str | None):
    if not authorization or not authorization.startswith("Bearer "):
        return None
    token = authorization.replace("Bearer ", "")
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return {"user_id": payload.get("user_id"), "email": payload.get("email")}
    except Exception:
        return None


def bootstrap_auth_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS app_users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            full_name VARCHAR(255) DEFAULT '',
            company VARCHAR(255) DEFAULT '',
            role VARCHAR(50) DEFAULT 'business',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS user_settings (
            id SERIAL PRIMARY KEY,
            user_id INTEGER UNIQUE REFERENCES app_users(id) ON DELETE CASCADE,
            theme VARCHAR(20) DEFAULT 'dark',
            voice_enabled BOOLEAN DEFAULT TRUE,
            chat_mode VARCHAR(20) DEFAULT 'auto',
            retention VARCHAR(20) DEFAULT '90_days',
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()


def bootstrap_chat_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("ALTER TABLE chat_history ADD COLUMN IF NOT EXISTS pinned BOOLEAN DEFAULT FALSE")
    conn.commit()
    conn.close()


# =========================
#  ROUTES
# =========================
app.include_router(query_router)
app.include_router(predict_router)
bootstrap_auth_tables()
bootstrap_chat_tables()


# =========================
#  CORS (FRONTEND)
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174"
    ],
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
#  HOME
# =========================
@app.get("/")
def home():
    return {"message": "CHAITRA API is running "}


@app.post("/auth/signup")
def auth_signup(body: dict):
    email = (body.get("email") or "").strip().lower()
    password = body.get("password") or ""
    full_name = body.get("full_name") or ""
    company = body.get("company") or ""

    if not email or not password:
        return {"status": "failed", "error": "Email and password are required."}

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM app_users WHERE email = %s", (email,))
        existing = cursor.fetchone()
        if existing:
            conn.close()
            return {"status": "failed", "error": "User already exists."}

        cursor.execute(
            """
            INSERT INTO app_users (email, password_hash, full_name, company)
            VALUES (%s, %s, %s, %s)
            RETURNING id, email, full_name, company, role
            """,
            (email, hash_password(password), full_name, company)
        )
        user = cursor.fetchone()
        cursor.execute(
            "INSERT INTO user_settings (user_id) VALUES (%s) ON CONFLICT (user_id) DO NOTHING",
            (user[0],)
        )
        conn.commit()
        token = create_access_token({"user_id": str(user[0]), "email": user[1]})
        return {
            "status": "success",
            "token": token,
            "user": {
                "id": str(user[0]),
                "email": user[1],
                "full_name": user[2] or "",
                "company": user[3] or "",
                "role": user[4] or "business"
            }
        }
    except Exception as e:
        return {"status": "failed", "error": str(e)}
    finally:
        conn.close()


@app.post("/auth/login")
def auth_login(body: dict):
    email = (body.get("email") or "").strip().lower()
    password = body.get("password") or ""
    if not email or not password:
        return {"status": "failed", "error": "Email and password are required."}

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, email, full_name, company, role
        FROM app_users
        WHERE email = %s AND password_hash = %s
        """,
        (email, hash_password(password))
    )
    user = cursor.fetchone()
    conn.close()

    if not user:
        return {"status": "failed", "error": "Invalid credentials."}

    token = create_access_token({"user_id": str(user[0]), "email": user[1]})
    return {
        "status": "success",
        "token": token,
        "user": {
            "id": str(user[0]),
            "email": user[1],
            "full_name": user[2] or "",
            "company": user[3] or "",
            "role": user[4] or "business"
        }
    }


@app.get("/auth/me")
def auth_me(authorization: str | None = Header(default=None)):
    current_user = get_current_user(authorization)
    if not current_user:
        return {"status": "failed", "error": "Unauthorized"}

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, email, full_name, company, role, created_at FROM app_users WHERE id = %s",
        (current_user["user_id"],)
    )
    user = cursor.fetchone()
    conn.close()

    if not user:
        return {"status": "failed", "error": "User not found"}

    return {
        "status": "success",
        "user": {
            "id": str(user[0]),
            "email": user[1],
            "full_name": user[2] or "",
            "company": user[3] or "",
            "role": user[4] or "business",
            "created_at": str(user[5])
        }
    }


@app.put("/auth/profile")
def update_profile(body: dict, authorization: str | None = Header(default=None)):
    current_user = get_current_user(authorization)
    if not current_user:
        return {"status": "failed", "error": "Unauthorized"}

    full_name = body.get("full_name", "")
    company = body.get("company", "")
    role = body.get("role", "business")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE app_users
        SET full_name = %s, company = %s, role = %s
        WHERE id = %s
        """,
        (full_name, company, role, current_user["user_id"])
    )
    conn.commit()
    conn.close()
    return {"status": "success"}


@app.get("/auth/settings")
def get_settings(authorization: str | None = Header(default=None)):
    current_user = get_current_user(authorization)
    if not current_user:
        return {"status": "failed", "error": "Unauthorized"}

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT theme, voice_enabled, chat_mode, retention
        FROM user_settings
        WHERE user_id = %s
        """,
        (current_user["user_id"],)
    )
    settings = cursor.fetchone()
    if not settings:
        cursor.execute("INSERT INTO user_settings (user_id) VALUES (%s)", (current_user["user_id"],))
        conn.commit()
        settings = ("dark", True, "auto", "90_days")
    conn.close()

    return {
        "status": "success",
        "settings": {
            "theme": settings[0],
            "voice_enabled": bool(settings[1]),
            "chat_mode": settings[2],
            "retention": settings[3]
        }
    }


@app.put("/auth/settings")
def update_settings(body: dict, authorization: str | None = Header(default=None)):
    current_user = get_current_user(authorization)
    if not current_user:
        return {"status": "failed", "error": "Unauthorized"}

    theme = body.get("theme", "dark")
    voice_enabled = bool(body.get("voice_enabled", True))
    chat_mode = body.get("chat_mode", "auto")
    retention = body.get("retention", "90_days")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO user_settings (user_id, theme, voice_enabled, chat_mode, retention)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (user_id) DO UPDATE
        SET theme = EXCLUDED.theme,
            voice_enabled = EXCLUDED.voice_enabled,
            chat_mode = EXCLUDED.chat_mode,
            retention = EXCLUDED.retention,
            updated_at = CURRENT_TIMESTAMP
        """,
        (current_user["user_id"], theme, voice_enabled, chat_mode, retention)
    )
    conn.commit()
    conn.close()
    return {"status": "success"}


# =========================
#  DASHBOARD API
# =========================
@app.get("/dashboard/")
def get_dashboard():

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Total queries
        cursor.execute("SELECT COUNT(*) FROM query_logs")
        total_queries = cursor.fetchone()[0]

        # Avg prediction
        cursor.execute("SELECT AVG(prediction) FROM query_logs WHERE prediction IS NOT NULL")
        avg_prediction = cursor.fetchone()[0]

        # Recent predictions (for chart)
        cursor.execute("""
            SELECT prediction 
            FROM query_logs 
            WHERE prediction IS NOT NULL 
            ORDER BY id DESC 
            LIMIT 10
        """)
        predictions = cursor.fetchall()

        conn.close()

        return {
            "total_queries": total_queries or 0,
            "avg_prediction": round(avg_prediction, 2) if avg_prediction else 0,
            "recent_predictions": [float(p[0]) for p in predictions[::-1]]
        }

    except Exception as e:
        return {"error": str(e)}


@app.get("/predictions/")
def get_predictions():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, prediction, query
            FROM query_logs
            WHERE prediction IS NOT NULL
            ORDER BY id DESC
            LIMIT 20
            """
        )
        rows = cursor.fetchall()
        conn.close()

        return {
            "predictions": [
                {
                    "id": row[0],
                    "prediction": float(row[1]),
                    "query": row[2] or ""
                }
                for row in rows
            ]
        }
    except Exception as e:
        return {"error": str(e)}


@app.get("/insights/")
def get_insights():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                COUNT(*) FILTER (WHERE prediction IS NOT NULL),
                AVG(prediction),
                MAX(prediction),
                MIN(prediction)
            FROM query_logs
            """
        )
        total_pred, avg_pred, max_pred, min_pred = cursor.fetchone()

        cursor.execute(
            """
            SELECT query, response
            FROM chat_history
            ORDER BY id DESC
            LIMIT 5
            """
        )
        recent_chats = cursor.fetchall()
        conn.close()

        insights = [
            f"Total prediction records: {int(total_pred or 0)}",
            f"Average predicted sales: {round(float(avg_pred), 2) if avg_pred is not None else 0}",
            f"Highest predicted sales: {round(float(max_pred), 2) if max_pred is not None else 0}",
            f"Lowest predicted sales: {round(float(min_pred), 2) if min_pred is not None else 0}",
        ]

        return {
            "insights": insights,
            "recent_chats": [
                {"query": q or "", "response": r or ""}
                for q, r in recent_chats
            ]
        }
    except Exception as e:
        return {"error": str(e)}


# =========================
#  CHAT HISTORY API
# =========================
@app.get("/chats/{user_id}")
def get_user_chats(user_id: str):

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, query, response, pinned
            FROM chat_history
            WHERE user_id = %s
            ORDER BY pinned DESC, id DESC
            LIMIT 100
        """, (user_id,))

        chats = cursor.fetchall()

        conn.close()

        return {
            "chats": [
                {"id": c[0], "query": c[1] or "", "response": c[2] or "", "pinned": bool(c[3])}
                for c in chats
            ]
        }

    except Exception as e:
        return {"error": str(e)}


@app.put("/chats/{chat_id}/pin")
def toggle_pin_chat(chat_id: int, body: dict):
    try:
        pinned = bool(body.get("pinned", False))
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE chat_history SET pinned = %s WHERE id = %s", (pinned, chat_id))
        conn.commit()
        conn.close()
        return {"status": "success", "chat_id": chat_id, "pinned": pinned}
    except Exception as e:
        return {"status": "failed", "error": str(e)}


@app.delete("/chats/{chat_id}")
def delete_chat(chat_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM chat_history WHERE id = %s", (chat_id,))
        conn.commit()
        conn.close()
        return {"status": "success", "chat_id": chat_id}
    except Exception as e:
        return {"status": "failed", "error": str(e)}