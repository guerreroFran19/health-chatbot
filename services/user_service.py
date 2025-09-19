from repository import user_repository

def register_user(name: str, email: str, password: str):
    if not name or not email or not password:
        raise ValueError("Todos los campos son obligatorios")

    try:
        return user_repository.create_user(name, email, password)
    except Exception as e:
        print(f"❌ Error en register_user: {e}")
        # Convierte la excepción de base de datos en ValueError para el controller
        raise ValueError(f"No se pudo crear el usuario: {e}")