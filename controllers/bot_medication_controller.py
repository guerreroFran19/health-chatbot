import requests
from datetime import datetime, timedelta

from core.speech.speechToText import listen
from core.speech.textToSpeech import speak
from core.utils.parse_natural_time import parse_natural_datetime
from repository.medication_repository import get_medication_by_name
from repository.sessions_repository import get_active_session, get_latest_active_session, deactivate_session, get_active_sessions_count
from services.medication_service import delete_medication_service, create_medication_service

# Configuración de la API
API_BASE_URL = "http://localhost:8000"

def get_latest_active_user_session():
    """
    Obtiene la sesión activa más reciente de cualquier usuario desde la BD.
    Verifica si la sesión está expirada y la desactiva si corresponde.
    """
    try:
        session = get_latest_active_session()
        if not session:
            return None, "No hay usuarios con sesión activa. Por favor inicia sesión primero."

        if datetime.now() > session['expires_at']:
            deactivate_session(session['token'])
            return None, "La sesión ha expirado. Por favor inicia sesión nuevamente."

        return session, None
    except Exception as e:
        print(f"❌ Error obteniendo sesión activa: {e}")
        return None, "Error al obtener la sesión activa."



def create_medication_bot():
    """
    Flujo del bot para crear un medicamento preguntando al usuario.
    """

    # 1️⃣ Obtener sesión activa
    session = get_latest_active_session()
    if not session:
        speak("No hay usuarios con sesión activa. Por favor inicia sesión primero.")
        return "No hay sesión activa."

    if datetime.now() > session['expires_at']:
        deactivate_session(session['token'])
        speak("La sesión ha expirado. Por favor inicia sesión nuevamente.")
        return "Sesión expirada."

    user_id = session['user_id']

    # 2️⃣ Pedir datos al usuario

    while True:
        # Pedir datos al usuario
        speak("¿Cuál es el nombre del medicamento?")
        name = listen().strip().lower()

        speak("¿Cuál es la dosis?")
        dosage = listen().strip().lower()
        speak("¿Cada cuántas horas se debe tomar?")
        frequency_hours = listen().strip()

        if not name or not dosage or not frequency_hours:
            speak("Por favor completa todos los campos obligatorios.")
            continue

        # Convertir frecuencia a número
        try:
            # Extraer solo los números del texto
            frequency_number = int(''.join(filter(str.isdigit, frequency_hours)))

            # Validar que sea un número positivo
            if frequency_number <= 0:
                speak("Por favor ingresa un número válido de horas mayor a cero.")
                continue

        except (ValueError, TypeError):
            speak(
                "No entendí el número de horas. Por favor di solo el número, por ejemplo: 'cada 8 horas' o simplemente '8'.")
            continue
        print("frecuencia",frequency_number)

        # Fecha de finalización (opcional)
        speak(
            "¿Hasta cuándo tomarás el medicamento? Puedes decir 'sin fecha' si no quieres establecer una fecha final.")
        fecha_texto = listen().strip().lower()
        if fecha_texto in ["sin fecha", "ninguna", "no"]:
            end_date = None
        else:
            _, end_iso, _ = parse_natural_datetime(fecha_texto)
            end_date = end_iso

        # Instrucciones adicionales (opcional)
        speak("¿Instrucciones adicionales? (Enter si no hay)")
        instructions = listen().strip().lower()


        break

    # 3️⃣ Crear medicamento
    try:
        medication_data = {
            "user_id": user_id,
            "name": name,
            "dosage": dosage,
            "frequency_hours": frequency_number,
            "end_date": end_date,
            "instructions": instructions,
            "is_active": True
        }

        new_med = create_medication_service(medication_data)
        speak(f"✅ Medicamento '{new_med['name']}' creado correctamente.")
        return new_med

    except ValueError as ve:
        speak(f"⚠️ No se pudo crear el medicamento: {ve}")
        print(f"⚠️ No se pudo crear el medicamento: {ve}")
        return None
    except Exception as e:
        speak(f"❌ Ocurrió un error al crear el medicamento: {e}")
        return None





def list_medications():
    """
    Lista medicamentos usando la sesión más reciente de la BD (multiusuario).
    """
    session, error_msg = get_latest_active_user_session()
    if error_msg:
        return error_msg

    token = session["token"]
    user_email = session.get("user_email", "Usuario")
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(f"{API_BASE_URL}/medications", headers=headers)
        if response.status_code == 200:
            medications = response.json().get("medications", [])
            return format_medication_speech(medications, user_email)
        elif response.status_code == 401:
            deactivate_session(token)
            return "La sesión ha expirado. Por favor inicia sesión nuevamente."
        else:
            return f"Error al obtener medicamentos: {response.status_code} - {response.text}"
    except requests.exceptions.ConnectionError:
        return "Error de conexión con el servidor. Verifica que la API esté ejecutándose."
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return "Ocurrió un error inesperado al obtener los medicamentos."


def delete_medication_by_name_bot(medication_name: str):
    """
    Elimina un medicamento por nombre usando la sesión activa del usuario.
    """
    try:
        # Obtener sesión activa más reciente
        session = get_latest_active_session()
        if not session:
            return "No hay usuarios con sesión activa. Por favor inicia sesión primero."

        # Verificar expiración
        if datetime.now() > session['expires_at']:
            deactivate_session(session['token'])
            return "La sesión ha expirado. Por favor inicia sesión nuevamente."

        user_id = session['user_id']

        # Buscar el medicamento por nombre y user_id
        medication = get_medication_by_name(medication_name, user_id)
        if not medication:
            return f"No se encontró ningún medicamento llamado '{medication_name}' para tu usuario."

        # Eliminar medicamento
        deleted = delete_medication_service(medication['id'], user_id)
        if deleted:
            return f"✅ Medicamento '{medication_name}' eliminado correctamente."
        else:
            return f"⚠️ No se pudo eliminar el medicamento '{medication_name}'."

    except Exception as e:
        print(f"❌ Error en delete_medication_by_name_bot: {e}")
        return f"Ocurrió un error al intentar eliminar el medicamento: {e}"



def format_medication_speech(medications, user_identifier="Tienes"):
    """
    Formatea la lista de medicamentos para speech.
    """
    if not medications:
        return f"{user_identifier}, no tienes medicamentos registrados."

    speech_parts = []
    for i, med in enumerate(medications, 1):
        name = med.get('name', 'Medicamento sin nombre')
        dosage = med.get('dosage', 'Dosis no especificada')
        frequency = med.get('frequency_hours', 'Frecuencia no especificada')
        instructions = med.get('instructions', 'Sin instrucciones específicas')
        next_dose_time = calculate_next_dose_time(frequency)
        medication_info = (
            f"{i}. {name}. Dosis: {dosage}. Próxima toma a las {next_dose_time}. "
            f"Instrucciones: {instructions}"
        )
        speech_parts.append(medication_info)

    intro = f"{user_identifier}, tienes {len(medications)} medicamento{'s' if len(medications) > 1 else ''}: "
    return intro + ". ".join(speech_parts)


def calculate_next_dose_time(frequency_hours):
    """
    Calcula la próxima hora de toma basada en la frecuencia.
    """
    try:
        if isinstance(frequency_hours, int) and frequency_hours > 0:
            return (datetime.now() + timedelta(hours=frequency_hours)).strftime("%H:%M")
        return "hora no programada"
    except:
        return "hora no programada"


def get_session_stats():
    """
    Obtiene estadísticas de sesiones activas (útil para debugging).
    """
    try:
        active_sessions = get_active_sessions_count()
        return f"Hay {active_sessions} sesiones activas en el sistema."
    except:
        return "No se pudieron obtener estadísticas de sesiones."
