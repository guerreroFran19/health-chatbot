# middleware/auth_middleware.py
from fastapi import HTTPException, Header
from config.jwt_config import verify_token


async def get_current_user(authorization: str = Header(...)):
    """Middleware para obtener el usuario actual del token JWT"""

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Formato de autorización inválido. Use: Bearer <token>"
        )

    token = authorization.split(" ")[1]
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

    return {
        "user_id": payload.get("user_id"),
        "email": payload.get("sub")
    }