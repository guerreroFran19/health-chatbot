# services/medication_service.py
from repository import medication_repository


def add_medication(user_id: int, medication_data: dict):
    if not medication_data['name'] or not medication_data['dosage']:
        raise ValueError("Nombre y dosis son obligatorios")

    if medication_data['frequency_hours'] <= 0:
        raise ValueError("La frecuencia debe ser mayor a 0 horas")

    return medication_repository.create_medication(user_id, medication_data)


def get_medications(user_id: int):
    return medication_repository.get_user_medications(user_id)