from fastapi import APIRouter, Depends
from middleware.auth_middleware import get_current_user
from controllers.medication_controller import (
    create_medication_controller,
    get_medications_controller,
    get_medication_controller,
    update_medication_controller,
    delete_medication_controller
)

router = APIRouter()

@router.post("")
def create_medication(medication_data: dict, current_user: dict = Depends(get_current_user)):
    return create_medication_controller(medication_data, current_user)

@router.get("")
def get_medications(current_user: dict = Depends(get_current_user)):
    return get_medications_controller(current_user)

@router.get("/{medication_id}")
def get_medication(medication_id: int, current_user: dict = Depends(get_current_user)):
    return get_medication_controller(medication_id, current_user)

@router.put("/{medication_id}")
def update_medication(medication_id: int, medication_data: dict, current_user: dict = Depends(get_current_user)):
    return update_medication_controller(medication_id, medication_data, current_user)

@router.delete("/{medication_id}")
def delete_medication(medication_id: int, current_user: dict = Depends(get_current_user)):
    return delete_medication_controller(medication_id, current_user)