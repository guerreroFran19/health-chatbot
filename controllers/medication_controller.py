from services.medication_service import (
    create_medication_service,
    get_medications_service,
    get_medication_service,
    update_medication_service,
    delete_medication_service
)
from fastapi import HTTPException


def create_medication_controller(medication_data: dict, current_user: dict):
    try:
        # Asegurarse de que el usuario está autenticado
        if not current_user or 'id' not in current_user:
            raise HTTPException(status_code=401, detail="Usuario no autenticado")

        # Agregar el user_id a los datos del medicamento
        medication_data['user_id'] = current_user['id']

        result = create_medication_service(medication_data)
        return {"message": "Medicamento creado exitosamente", "medication": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


def get_medications_controller(current_user: dict):
    try:
        if not current_user or 'id' not in current_user:
            raise HTTPException(status_code=401, detail="Usuario no autenticado")

        medications = get_medications_service(current_user['id'])
        return {"medications": medications}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


def get_medication_controller(medication_id: int, current_user: dict):
    try:
        if not current_user or 'id' not in current_user:
            raise HTTPException(status_code=401, detail="Usuario no autenticado")

        medication = get_medication_service(medication_id, current_user['id'])
        if not medication:
            raise HTTPException(status_code=404, detail="Medicamento no encontrado")

        return {"medication": medication}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


def update_medication_controller(medication_id: int, medication_data: dict, current_user: dict):
    try:
        if not current_user or 'id' not in current_user:
            raise HTTPException(status_code=401, detail="Usuario no autenticado")

        medication_data['user_id'] = current_user['id']
        medication = update_medication_service(medication_id, medication_data)

        if not medication:
            raise HTTPException(status_code=404, detail="Medicamento no encontrado")

        return {"message": "Medicamento actualizado exitosamente", "medication": medication}
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


def delete_medication_controller(medication_id: int, current_user: dict):
    try:
        if not current_user or 'id' not in current_user:
            raise HTTPException(status_code=401, detail="Usuario no autenticado")

        success = delete_medication_service(medication_id, current_user['id'])

        if not success:
            raise HTTPException(status_code=404, detail="Medicamento no encontrado")

        return {"message": "Medicamento eliminado exitosamente"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")