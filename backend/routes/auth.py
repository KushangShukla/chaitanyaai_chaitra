from fastapi import APIRouter, Depends, HTTPException
from backend.auth.auth_2fa import generate_2fa_secret, verify_otp
import psycopg2
import jwt
from datetime import datetime, timedelta
from pydantic import BaseModel
from passlib.context import CryptContext
from fastapi.security import HTTPBearer
import os
from backend.db.connection import get_connection

# =========================
# CONFIG
# =========================
SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# =========================
# PASSWORD HASHING
# =========================
def hash_password(password):
    return pwd_context.hash(password)

def verify_password(password, hashed):
    return pwd_context.verify(password, hashed)

# =========================
# DB CONNECTION
# =========================
conn=get_connection()

# =========================
# MODELS
# =========================
class UserRequest(BaseModel):
    user_id: str

class VerifyRequest(BaseModel):
    user_id: str
    otp: str

class SignupRequest(BaseModel):
    email: str
    password: str

# =========================
# SIGNUP
# =========================
@router.post("/signup")
def signup(data: SignupRequest):

    conn = get_connection()
    cursor = conn.cursor()

    hashed = hash_password(data.password)

    cursor.execute(
        "INSERT INTO users (email, password) VALUES (%s, %s) RETURNING id",
        (data.email, hashed)
    )

    user_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()

    return {
        "message": "User created",
        "user_id": user_id
    }

# =========================
# LOGIN
# =========================
@router.post("/login")
def login_user(data: dict):

    email = data.get("email")
    password = data.get("password")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, password, is_2fa_enabled FROM users WHERE email=%s",
        (email,)
    )

    user = cursor.fetchone()
    conn.close()

    if not user:
        return {"status": "error", "error": "User not found"}

    user_id, stored_password, is_2fa_enabled = user

    #  HASH VERIFY
    if not verify_password(password, stored_password):
        return {"status": "error", "error": "Invalid password"}

    #  2FA REQUIRED
    if is_2fa_enabled:
        return {
            "status": "success",
            "2fa_required": True,
            "user_id": user_id
        }

    #  DIRECT JWT
    token = jwt.encode(
        {
            "user_id": user_id,
            "exp": datetime.utcnow() + timedelta(hours=2)
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {
        "status": "success",
        "token": token,
        "user": {
            "id": user_id,
            "email": email
        }
    }

# =========================
# ENABLE 2FA
# =========================
@router.post("/generate-2fa")
def enable_2fa(data: UserRequest):

    user_id = data.user_id
    secret, qr = generate_2fa_secret(user_id)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE users
        SET two_fa_secret=%s,
            is_2fa_enabled=TRUE
        WHERE id=%s
        """,
        (secret, user_id)
    )

    conn.commit()
    conn.close()

    print("Incoming Data:",data)

    return {
        "message": "Scan QR Code in Google Authenticator",
        "qr_code": qr
    }

# =========================
# RATE LIMIT
# =========================
attempts = {}

# =========================
# VERIFY 2FA
# =========================
@router.post("/verify-2fa")
def verify_2fa_route(data: VerifyRequest):

    user_id = data.user_id
    otp = data.otp

    if user_id not in attempts:
        attempts[user_id] = 0

    if attempts[user_id] >= 3:
        return {"error": "Too many attempts"}

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT two_fa_secret FROM users WHERE id=%s",
        (user_id,)
    )

    row = cursor.fetchone()
    conn.close()

    if not row:
        return {"error": "User not found"}

    secret = row[0]

    if not secret:
        return {"error": "2FA not enabled"}

    if verify_otp(secret, otp):
        attempts[user_id] = 0

        token = jwt.encode(
            {
                "user_id": user_id,
                "exp": datetime.utcnow() + timedelta(hours=2)
            },
            SECRET_KEY,
            algorithm=ALGORITHM
        )

        return {
            "message": "2FA verification successful",
            "token": token
        }

    attempts[user_id] += 1
    return {"error": "Invalid OTP"}

# =========================
# PROTECTED ROUTE
# =========================
def get_current_user(token=Depends(security)):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["user_id"]
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/me")
def get_me(user_id=Depends(get_current_user)):
    return {"user_id": user_id}