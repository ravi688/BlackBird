from fastapi import APIRouter

import os
import secrets
import hashlib

from datetime import datetime, timedelta, timezone
from threading import Lock

from fastapi import (
    FastAPI,
    Request,
    Response,
    HTTPException,
    Depends,
)
from pydantic import BaseModel
from pwdlib import PasswordHash
from dotenv import load_dotenv


router = APIRouter(
	prefix="/admin",
	tags=["Admin"]
	)



load_dotenv()

# --------------------------------------------------
# Configuration
# --------------------------------------------------

ADMIN_USERNAME = os.environ["ADMIN_USERNAME"]
ADMIN_PASSWORD_HASH = os.environ["ADMIN_PASSWORD_HASH"]

SESSION_COOKIE = "admin_session"

SESSION_IDLE_TIMEOUT = timedelta(days=30)
SESSION_MAX_LIFETIME = timedelta(days=90)

COOKIE_SECURE = True

password_hash = PasswordHash.recommended()


# --------------------------------------------------
# In-memory session storage
# --------------------------------------------------

# token_hash -> {
#     created_at: datetime,
#     expires_at: datetime,
#     absolute_expires_at: datetime
# }

sessions = {}

sessions_lock = Lock()


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


# --------------------------------------------------
# Session management
# --------------------------------------------------

def create_session():
    now = datetime.now(timezone.utc)

    token = secrets.token_urlsafe(32)

    session = {
        "created_at": now,
        "expires_at": now + SESSION_IDLE_TIMEOUT,
        "absolute_expires_at": now + SESSION_MAX_LIFETIME,
    }

    with sessions_lock:
        sessions[hash_token(token)] = session

    return token, session


def renew_session(session):
    now = datetime.now(timezone.utc)

    session["expires_at"] = min(
        now + SESSION_IDLE_TIMEOUT,
        session["absolute_expires_at"],
    )


def set_session_cookie(response, token, session):
    now = datetime.now(timezone.utc)

    expiry = min(
        session["expires_at"],
        session["absolute_expires_at"],
    )

    max_age = max(0, int((expiry - now).total_seconds()))

    response.set_cookie(
        key=SESSION_COOKIE,
        value=token,
        max_age=max_age,
        httponly=True,
        secure=COOKIE_SECURE,
        samesite="lax",
        path="/",
    )


# --------------------------------------------------
# Authentication dependency
# --------------------------------------------------

def authenticate_admin(
    request: Request,
    response: Response,
):
    token = request.cookies.get(SESSION_COOKIE)

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
        )

    token_digest = hash_token(token)

    now = datetime.now(timezone.utc)

    with sessions_lock:

        session = sessions.get(token_digest)

        if session is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid session",
            )

        if (
            now >= session["expires_at"]
            or now >= session["absolute_expires_at"]
        ):
            del sessions[token_digest]

            response.delete_cookie(
                key=SESSION_COOKIE,
                path="/",
                httponly=True,
                secure=COOKIE_SECURE,
                samesite="lax",
            )

            raise HTTPException(
                status_code=401,
                detail="Session expired",
            )

        renew_session(session)

        set_session_cookie(response, token, session)

    return ADMIN_USERNAME


# --------------------------------------------------
# API endpoints
# --------------------------------------------------

class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login")
def login(data: LoginRequest, response: Response):

    valid_username = secrets.compare_digest(
        data.username,
        ADMIN_USERNAME,
    )

    valid_password = password_hash.verify(
        data.password,
        ADMIN_PASSWORD_HASH,
    )

    if not (valid_username and valid_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    token, session = create_session()

    set_session_cookie(response, token, session)

    return {
        "message": "Login successful"
    }


@router.post("/logout")
def logout(
    request: Request,
    response: Response,
):

    token = request.cookies.get(SESSION_COOKIE)

    if token:
        with sessions_lock:
            sessions.pop(hash_token(token), None)

    response.delete_cookie(
        key=SESSION_COOKIE,
        path="/",
        httponly=True,
        secure=COOKIE_SECURE,
        samesite="lax",
    )

    return {"message": "Logged out"}


@router.get("/me")
def get_current_admin(
    admin: str = Depends(authenticate_admin),
):
    return {
        "authenticated": True,
        "username": admin,
    }


@router.get("/admin/dashboard")
def dashboard(
    admin: str = Depends(authenticate_admin),
):
    return {
        "message": "Welcome to admin dashboard",
    }
