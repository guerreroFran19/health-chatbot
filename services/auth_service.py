from repository.auth_repository import get_user_by_email, create_user
from repository.sessions_repository import save_session
import bcrypt
import jwt
import os
from datetime import datetime, timedelta
import json

JWT_EXP_HOURS = 24

def register_user(name: str, email: str, password: str):
    """
    Registra un usuario y retorna datos sin contraseña.
    """
    if not name or not email or not password:
        raise ValueError("Nombre, email y contraseña son obligatorios")

    try:
        # Verificar si el usuario ya existe
        existing_user = get_user_by_email(email)
        if existing_user:
            raise ValueError("El email ya está registrado")

        # Crear usuario en la DB (create_user hace el hash internamente)
        new_user = create_user(name, email, password)

        # Retornar usuario sin password
        user_without_password = {
            "id": new_user["id"],
            "name": new_user["name"],
            "email": new_user["email"]
        }

        print(f"✅ Usuario creado: {user_without_password}")
        return user_without_password

    except ValueError as ve:
        raise ve
    except Exception as e:
        print(f"❌ Error en register_user: {e}")
        raise ValueError(f"No se pudo crear el usuario: {e}")

def login_user(email: str, password: str):
    """
    Verifica credenciales, genera JWT y crea sesión en DB.
    """

    if not email or not password:
        raise ValueError("Email y contraseña son obligatorios")

    try:

        # Buscar usuario por email
        user = get_user_by_email(email)
        print("Password ingresado:", password)
        print("Hash DB (string):", user['password'])
        print("Check result:", bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')))
        user = get_user_by_email(email)
        print("Usuario completo de DB:", user)
        if not user:
            raise ValueError("Credenciales inválidas")

        # Debug: imprimir hash de la DB y password ingresado
        print(f"Password ingresado: {password}")
        print(f"Hash en DB: {user['password']}")

        # Verificar contraseña
        if not bcrypt.checkpw(password.encode("utf-8"), user["password"].strip().encode("utf-8")):
            raise ValueError("Credenciales inválidas")

        # Generar token JWT
        token = generate_jwt_token(user)

        # Calcular expiración
        expires_at = datetime.now() + timedelta(hours=JWT_EXP_HOURS)

        # Guardar sesión en la DB
        session_info = save_session(user["id"], token, expires_at)

        # Retornar usuario sin password y token
        user_without_password = {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"]
        }
        print("Password ingresado:", password)
        print("Hash DB (string):", user['password'])
        print("Check result:", bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')))
        user = get_user_by_email(email)
        print("Usuario completo de DB:", user)
        return {
            "user": user_without_password,
            "token": token,
            "session_id": session_info["id"]
        }

    except ValueError as ve:
        raise ve
    except Exception as e:
        print(f"❌ Error en login_user: {e}")
        raise ValueError(f"Error durante el login: {e}")


def generate_jwt_token(user: dict):
    """
    Genera un JWT con expiración de 24h.
    """
    secret_key = os.getenv("JWT_SECRET_KEY", "fallback_secret_key")
    expires_delta = timedelta(hours=JWT_EXP_HOURS)

    payload = {
        "user_id": user["id"],
        "email": user["email"],
        "exp": datetime.utcnow() + expires_delta,
        "iat": datetime.utcnow()
    }

    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token


def verify_jwt_token(token: str):
    """
    Verifica JWT y retorna payload.
    """
    try:
        secret_key = os.getenv("JWT_SECRET_KEY", "fallback_secret_key")
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expirado")
    except jwt.InvalidTokenError:
        raise ValueError("Token inválido")



