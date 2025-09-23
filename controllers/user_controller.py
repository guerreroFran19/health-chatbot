from services import user_service

def create_user_controller(name: str, email: str, password: str):
    try:
        user = user_service.register_user(name, email, password)
        return {"status": "success", "user": user}
    except Exception as e:
        return {"status": "error", "message": str(e)}
