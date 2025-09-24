from fastapi import APIRouter
from controllers.auth_controller import login_controller, register_controller

router = APIRouter()

@router.post("/login")
def login(credentials: dict):
    return login_controller(credentials)

@router.post("/register")
def register(user_data: dict):
    return register_controller(user_data)
@router.post("/logout")
def logout():
    return logout()