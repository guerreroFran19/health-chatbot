# services/user_service.py
from repository import user_repository

def register_user(name: str, email: str, password: str):
    if not name or not email or not password:
        raise ValueError("Todos los campos son obligatorios")

    return user_repository.create_user(name, email, password)
