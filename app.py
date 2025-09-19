from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from services import user_service

app = FastAPI()

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

@app.post("/users")
def create_user(user: UserCreate):
    try:
        print(f"[DEBUG] Recibido: {user.dict()}")
        new_user = user_service.register_user(user.name, user.email, user.password)
        if not new_user:
            raise HTTPException(status_code=400, detail="No se pudo crear el usuario")
        return {"status": "success", "user": new_user}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        print(f"[ERROR] {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

