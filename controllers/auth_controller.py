import os

from repository.sessions_repository import deactivate_session
from services.auth_service import login_user, register_user
from fastapi import HTTPException, Request

def login_controller(credentials: dict):
    try:
        result = login_user(
            email=credentials.get('email'),
            password=credentials.get('password')
        )
        return {"message": "Login exitoso", "data": result}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")

def register_controller(user_data: dict):
    try:
        result = register_user(
            name=user_data.get('name'),
            email=user_data.get('email'),
            password=user_data.get('password')
        )
        return {"message": "Usuario registrado exitosamente", "user": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


def logout(request: Request):
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        return {"detail": "Token requerido"}

    token = token.split(" ")[1]
    deactivate_session(token)
    return {"detail": "Sesión cerrada exitosamente"}