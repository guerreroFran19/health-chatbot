import datetime as dt
import re


def parse_natural_datetime(text_datetime):
    """
    Parser manual para fechas en español - VERSIÓN COMPLETA
    """
    try:
        text = text_datetime.lower().strip()
        print(f" Parseando: '{text}'")

        # 🔹 PRIMERO: Verificar si es una fecha relativa
        relative_result = parse_relative_date(text)
        if relative_result:
            print(f" Fecha relativa encontrada: {relative_result}")
            return format_for_calendar(relative_result)

        # 🔹 SEGUNDO: Verificar si es una fecha absoluta
        absolute_result = parse_absolute_date(text)
        if absolute_result:
            print(f" Fecha absoluta encontrada: {absolute_result}")
            return format_for_calendar(absolute_result)

        # 🔹 TERCERO: Fecha por defecto
        default_date = dt.datetime.now() + dt.timedelta(hours=1)
        print("  Usando fecha por defecto")
        return format_for_calendar(default_date)

    except Exception as e:
        print(f"Error en parse_natural_datetime: {e}")
        default_date = dt.datetime.now() + dt.timedelta(hours=1)
        return format_for_calendar(default_date)


def parse_relative_date(text):
    """Parsear fechas relativas como 'mañana', 'pasado mañana'"""
    now = dt.datetime.now()

    # Patrones para fechas relativas
    if re.search(r'mañana|manana', text):
        date = now + dt.timedelta(days=1)
        hour = extract_hour_from_text(text) or 10  # Hora por defecto: 10 AM
        return date.replace(hour=hour, minute=0, second=0, microsecond=0)

    elif re.search(r'pasado mañana|pasado manana', text):
        date = now + dt.timedelta(days=2)
        hour = extract_hour_from_text(text) or 10
        return date.replace(hour=hour, minute=0, second=0, microsecond=0)

    elif re.search(r'hoy', text):
        date = now
        hour = extract_hour_from_text(text) or 10
        return date.replace(hour=hour, minute=0, second=0, microsecond=0)

    # Patrón para "en X días"
    match = re.search(r'en (\d+) días|en (\d+) dias', text)
    if match:
        days = int(match.group(1) or match.group(2))
        date = now + dt.timedelta(days=days)
        hour = extract_hour_from_text(text) or 10
        return date.replace(hour=hour, minute=0, second=0, microsecond=0)

    return None


def parse_absolute_date(text):
    """Parsear fechas absolutas - VERSIÓN MEJORADA"""
    try:
        # 🔹 PATRÓN MEJORADO para detectar AM/PM correctamente
        pattern = r'(\d{1,2})\s*(?:de)?\s*(\w+)\s*(?:a las)?\s*(\d{1,2})?\s*(am|pm|mañana|tarde|noche)?'
        match = re.search(pattern, text)

        if not match:
            print("No match encontrado")
            return None

        print(f"Match groups: {match.groups()}")

        dia = int(match.group(1))
        mes_str = match.group(2).lower()

        # Hora y AM/PM - manejar casos donde no hay hora especificada
        if match.group(3):
            hora = int(match.group(3))
        else:
            hora = 10  # Hora por defecto: 10 AM

        am_pm = match.group(4).lower() if match.group(4) else ''

        print(f"Datos crudos: dia={dia}, mes={mes_str}, hora={hora}, am_pm='{am_pm}'")

        # Diccionario de meses
        meses = {
            'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5, 'junio': 6,
            'julio': 7, 'agosto': 8, 'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12,
            'sep': 9, 'sept': 9, 'oct': 10, 'nov': 11, 'dic': 12
        }

        mes = meses.get(mes_str)
        if not mes:
            print(f"❌ Mes no reconocido: {mes_str}")
            return None

        # Obtener año actual
        now = dt.datetime.now()
        year = now.year

        # Si el mes ya pasó este año, usar próximo año
        if mes < now.month:
            year += 1

        # 🔹 AJUSTAR HORA CORRECTAMENTE
        hora_ajustada = adjust_hour(hora, am_pm)

        # Validar que la fecha sea válida
        try:
            fecha = dt.datetime(year, mes, dia, hora_ajustada, 0)
            print(f" Fecha creada: {fecha}")
            return fecha
        except ValueError as e:
            print(f" Fecha inválida: {e}")
            return None

    except Exception as e:
        print(f"Error en parse_absolute_date: {e}")
        return None


def extract_hour_from_text(text):
    """Extraer hora de texto como 'a las 10'"""
    hour_patterns = [
        r'a las (\d{1,2})',
        r'las (\d{1,2})',
        r'(\d{1,2})\s*(?:horas|hrs|h)'
    ]

    for pattern in hour_patterns:
        match = re.search(pattern, text)
        if match:
            return int(match.group(1))

    return None


def adjust_hour(hora, am_pm):
    """Ajustar hora según AM/PM """
    if not am_pm:
        print(f" Sin AM/PM, hora original: {hora}")
        return hora

    am_pm = am_pm.lower().strip()
    print(f"Ajustando hora: {hora}, am_pm: '{am_pm}'")

    # Detectar PM
    if any(pm_word in am_pm for pm_word in ['pm', 'tarde', 'noche']):
        if hora < 12:
            hora_ajustada = hora + 12
            print(f"PM detectado: {hora} -> {hora_ajustada}")
        else:
            hora_ajustada = hora
            print(f"PM detectado, pero hora ya es >= 12: {hora}")
        return hora_ajustada

    # Detectar AM
    elif any(am_word in am_pm for am_word in ['am', 'mañana', 'manana']):
        if hora == 12:
            hora_ajustada = 0
            print(f"AM detectado: 12 -> 0")
        elif hora > 12:
            # Si hora es > 12 pero dice AM, probable error del usuario
            hora_ajustada = hora - 12
            print(f" AM detectado con hora > 12: {hora} -> {hora_ajustada}")
        else:
            hora_ajustada = hora
            print(f"AM detectado, hora mantiene: {hora}")
        return hora_ajustada

    print(f"⚡ AM/PM no reconocido, hora original: {hora}")
    return hora


def format_for_calendar(date_obj):
    """Formatear datetime para Google Calendar"""
    start_time = date_obj.isoformat()
    end_time = (date_obj + dt.timedelta(minutes=30)).isoformat()
    timezone = "America/Argentina/Buenos_Aires"
    return start_time, end_time, timezone


# 🧪 PRUEBAS
def test_parser():
    """Probar el parser completo"""
    test_cases = [
        "14 de septiembre 10 am",
        "15 de octubre 3 pm",
        "3 pm",
        "10 am",
        "mañana a las 9",
        "hoy a las 2 de la tarde"
    ]

    print("🧪 TESTEO COMPLETO DEL PARSER:")
    for test in test_cases:
        print(f"\n--- Probando: '{test}' ---")
        start, end, tz = parse_natural_datetime(test)
        print(f"RESULTADO: {start}")


# Ejecutar pruebas
test_parser()