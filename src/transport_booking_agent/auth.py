import os
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from google.oauth2 import id_token
from google.auth.transport import requests

# It's crucial to load your Google Client ID from an environment variable
# for security. The default value is a placeholder.
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")

# This scheme will look for an "Authorization: Bearer <token>" header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Validates the Google ID token and returns the user's claims.

    This function acts as a FastAPI dependency. It automatically extracts the
    Bearer token from the Authorization header, verifies it with Google, and
    returns the token's payload (claims) if it's valid.

    Raises:
        HTTPException: 401 Unauthorized if the token is invalid, expired,
                       or for the wrong audience.
    """
    if not GOOGLE_CLIENT_ID:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Google Client ID is not configured on the server."
        )
    try:
        # Verify the token against Google's public keys
        id_info = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
        return id_info
    except ValueError as e:
        # This can happen if the token is invalid, expired, or for the wrong audience.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )