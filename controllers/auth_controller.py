# controllers/auth_controller.py
from repository import user_repository
from config.jwt_config import create_access_token, verify_password
from datetime import timedelta

class AuthController:
    @staticmethod
    def login_user(email: str, password: str):
        try:
            if not email or not password:
                return {"status": "error", "message": "Email y contraseña requeridos"}

            # 1. Buscar usuario
            user = user_repository.get_user_by_email(email)
            if not user:
                return {"status": "error", "message": "Usuario no encontrado"}

            # 2. Verificar contraseña con passlib (compatible con bcrypt)
            if not verify_password(password, user['password']):
                return {"status": "error", "message": "Contraseña incorrecta"}

            # 3. Crear token JWT
            access_token = create_access_token(
                data={"sub": user['email'], "user_id": user['id']},
                expires_delta=timedelta(minutes=30)
            )

            # 4. Preparar respuesta
            user_data = {
                'id': user['id'],
                'name': user['name'],
                'email': user['email'],
                'has_google_calendar': user.get('google_calendar_enabled', False)
            }

            return {
                "status": "success",
                "message": "Login exitoso",
                "user": user_data,
                "access_token": access_token,
                "token_type": "bearer"
            }

        except Exception as e:
            return {"status": "error", "message": f"Error en el login: {str(e)}"}