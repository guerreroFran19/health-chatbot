from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from controllers.auth_controller import AuthController

# Crear router
router = APIRouter(prefix="/auth", tags=["Authentication"])


class UserLogin(BaseModel):
    email: str
    password: str


@router.post("/login")
def login(user: UserLogin):
    try:
        print(f"[DEBUG] Login attempt for: {user.email}")

        result = AuthController.login_user(user.email, user.password)

        if result["status"] == "error":
            raise HTTPException(status_code=401, detail=result["message"])

        return result

    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Login error: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.post("/logout")
def logout():
    return {"status": "success", "message": "Logout exitoso"}