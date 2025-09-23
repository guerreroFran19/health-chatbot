# routes/medication_routes.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/medications", tags=["Medications"])


class MedicationCreate(BaseModel):
    name: str
    dosage: str
    frequency_hours: int
    instructions: str = ""


@router.post("/", response_model=dict)
async def create_medication(
        medication: MedicationCreate,
        current_user: dict = Depends(get_current_user)  # ✅ JWT required
):
    """Crear medicamento para el usuario autenticado"""
    try:
        from services.medication_service import add_medication

        new_med = add_medication(current_user["user_id"], medication.dict())
        return {
            "status": "success",
            "medication": new_med,
            "message": "Medicamento agregado correctamente"
        }
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/", response_model=dict)
async def list_medications(current_user: dict = Depends(get_current_user)):
    """Obtener medicamentos del usuario autenticado"""
    try:
        from services.medication_service import get_medications

        medications = get_medications(current_user["user_id"])
        return {
            "status": "success",
            "medications": medications
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")