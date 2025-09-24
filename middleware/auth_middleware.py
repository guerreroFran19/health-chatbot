from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from services.auth_service import verify_jwt_token
from repository.auth_repository import get_user_by_id

security = HTTPBearer()


async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Middleware para verificar el token JWT
    """
    try:
        token = credentials.credentials
        payload = verify_jwt_token(token)
        return payload
    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Obtiene el usuario actual basado en el token JWT
    """
    try:
        token = credentials.credentials
        payload = verify_jwt_token(token)

        # Obtener el usuario completo de la base de datos
        user_id = payload.get('user_id')
        user = get_user_by_id(user_id)

        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # Remover la contraseña por seguridad
        user.pop('password', None)
        return user

    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )