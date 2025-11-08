"""
Auth0 Authentication and Authorization
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from typing import Optional
import httpx

from app.config import settings


# Security scheme
security = HTTPBearer()


class Auth0User:
    """Authenticated user from Auth0"""
    def __init__(self, sub: str, email: str, name: str, role: str = "user", permissions: list = None):
        self.sub = sub  # Auth0 ID
        self.email = email
        self.name = name
        self.role = role
        self.permissions = permissions or []


async def get_auth0_public_key():
    """
    Fetch Auth0 public key for JWT verification
    In production, cache this result
    """
    jwks_url = f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(jwks_url)
        return response.json()


async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    Verify Auth0 JWT token
    Returns decoded token payload
    """
    token = credentials.credentials
    
    try:
        # For development, we can skip full verification
        # In production, verify signature with Auth0 public key
        
        # Decode without verification (development only)
        unverified_claims = jwt.get_unverified_claims(token)
        
        # Verify issuer
        if unverified_claims.get("iss") != settings.AUTH0_ISSUER.rstrip("/") + "/":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token issuer"
            )
        
        # For production, use proper verification:
        # jwks = await get_auth0_public_key()
        # header = jwt.get_unverified_header(token)
        # rsa_key = find_rsa_key(jwks, header)
        # payload = jwt.decode(token, rsa_key, algorithms=settings.AUTH0_ALGORITHMS, 
        #                      audience=settings.AUTH0_API_AUDIENCE, issuer=settings.AUTH0_ISSUER)
        
        return unverified_claims
        
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(token_payload: dict = Depends(verify_token)) -> Auth0User:
    """
    Get current authenticated user from token
    """
    try:
        # Debug: Log the entire token payload
        import json
        print("=" * 80)
        print("TOKEN PAYLOAD:")
        print(json.dumps(token_payload, indent=2))
        print("=" * 80)
        
        sub = token_payload.get("sub")
        
        # Try multiple ways to get email and name
        email = (
            token_payload.get("email") or 
            token_payload.get("https://eventhub.com/email") or
            token_payload.get("https://eventhub-api/email")
        )
        
        name = (
            token_payload.get("name") or 
            token_payload.get("https://eventhub.com/name") or
            token_payload.get("https://eventhub-api/name") or
            token_payload.get("nickname") or
            email  # Fallback to email if no name
        )
        
        # If still no email/name, fetch from Auth0 userinfo endpoint
        if not email or not name:
            print(f"Email or name missing, will use sub as identifier")
            # Use sub as fallback
            email = email or f"{sub.replace('|', '_')}@auth0.user"
            name = name or sub.split('|')[1] if '|' in sub else sub
        
        permissions = token_payload.get("permissions", [])
        
        print(f"Extracted - sub: {sub}, email: {email}, name: {name}")
        print(f"Initial permissions: {permissions}")
        
        # Get role from custom claim
        role = token_payload.get("https://eventhub-api/role") or "user"
        print(f"Role from custom claim 'https://eventhub-api/role': {role}")
        
        if role and role not in permissions:
            permissions.append(role)
            print(f"Added role to permissions: {permissions}")
        
        if not sub:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing subject"
            )
        
        print(f"Final user role: {role}, permissions: {permissions}")
        print("=" * 80)
        
        return Auth0User(sub=sub, email=email, name=name, role=role, permissions=permissions)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {str(e)}"
        )


def require_admin(current_user: Auth0User = Depends(get_current_user)) -> Auth0User:
    """
    Dependency to require admin role
    Checks if user has admin permissions
    """
    # Check if user has admin permission
    if "admin" not in current_user.permissions and "write:admin" not in current_user.permissions:
        # For demo purposes, you can also check email domain
        # if not current_user.email.endswith("@eventhub.com"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    return current_user


def require_user(current_user: Auth0User = Depends(get_current_user)) -> Auth0User:
    """
    Dependency to require authenticated user (any role)
    """
    return current_user


# Optional: For development/testing without Auth0
class MockAuth0User(Auth0User):
    """Mock user for testing"""
    def __init__(self):
        super().__init__(
            sub="auth0|test123",
            email="test@example.com",
            name="Test User",
            permissions=["read:events", "write:registrations"]
        )


def get_mock_user() -> Auth0User:
    """Get mock user for testing without Auth0"""
    return MockAuth0User()
