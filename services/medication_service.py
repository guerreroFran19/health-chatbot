from repository.medication_repository import (
    create_medication_repository,
    get_medications_repository,
    get_medication_repository,
    update_medication_repository,
    delete_medication_repository
)


def create_medication_service(medication_data: dict):
    try:
        # Validaciones básicas
        required_fields = ['name', 'dosage', 'frequency_hours', 'user_id']
        for field in required_fields:
            if field not in medication_data or not medication_data[field]:
                raise ValueError(f"El campo '{field}' es obligatorio")

        # Validar que frequency_hours sea un número positivo
        if not isinstance(medication_data['frequency_hours'], int) or medication_data['frequency_hours'] <= 0:
            raise ValueError("La frecuencia en horas debe ser un número positivo")

        return create_medication_repository(medication_data)
    except ValueError as ve:
        raise ve
    except Exception as e:
        print(f"❌ Error en create_medication_service: {e}")
        raise ValueError(f"No se pudo crear el medicamento: {e}")


def get_medications_service(user_id: int):
    try:
        return get_medications_repository(user_id)
    except Exception as e:
        print(f"❌ Error en get_medications_service: {e}")
        raise ValueError(f"No se pudieron obtener los medicamentos: {e}")


def get_medication_service(medication_id: int, user_id: int):
    try:
        return get_medication_repository(medication_id, user_id)
    except Exception as e:
        print(f"❌ Error en get_medication_service: {e}")
        raise ValueError(f"No se pudo obtener el medicamento: {e}")


def update_medication_service(medication_id: int, medication_data: dict):
    try:
        if 'name' in medication_data and not medication_data['name']:
            raise ValueError("El nombre del medicamento es obligatorio")

        if 'frequency_hours' in medication_data:
            if not isinstance(medication_data['frequency_hours'], int) or medication_data['frequency_hours'] <= 0:
                raise ValueError("La frecuencia en horas debe ser un número positivo")

        return update_medication_repository(medication_id, medication_data)
    except ValueError as ve:
        raise ve
    except Exception as e:
        print(f"❌ Error en update_medication_service: {e}")
        raise ValueError(f"No se pudo actualizar el medicamento: {e}")


def delete_medication_service(medication_id: int, user_id: int):
    try:
        return delete_medication_repository(medication_id, user_id)
    except Exception as e:
        print(f"❌ Error en delete_medication_service: {e}")
        raise ValueError(f"No se pudo eliminar el medicamento: {e}")