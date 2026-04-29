# backend/db/auth.py

from typing import Optional

from fastapi import Header, HTTPException, status
from .supabase import supabase


# ==================================================
# HELPERS
# ==================================================

def extract_bearer_token(authorization: Optional[str]) -> str:
    """
    Extract Bearer token from Authorization header.
    """

    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing"
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization format"
        )

    token = authorization.replace("Bearer ", "").strip()

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token missing"
        )

    return token


# ==================================================
# CURRENT USER DEPENDENCY
# ==================================================

async def get_current_user(
    authorization: Optional[str] = Header(None)
):
    """
    FastAPI dependency.
    Validates Supabase JWT and returns user object.
    """

    token = extract_bearer_token(authorization)

    try:
        response = supabase.auth.get_user(token)

        if not response or not response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )

        return response.user

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed"
        )


# ==================================================
# OPTIONAL ADMIN / SERVICE CHECK
# ==================================================

async def get_current_user_id(
    authorization: Optional[str] = Header(None)
) -> str:
    """
    Returns only user id.
    Useful for lightweight routes.
    """

    user = await get_current_user(authorization)

    return user.id