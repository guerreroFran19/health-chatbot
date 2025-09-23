from services.db_service import get_connection


def create_medication(user_id: int, medication_data: dict):
    query = """
            INSERT INTO medications (user_id, name, dosage, frequency_hours, end_date, instructions)
            VALUES (%s, %s, %s, %s, %s, \
                    %s) RETURNING id, name, dosage, frequency_hours, start_date, end_date, instructions, is_active; \
            """
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(query, (
            user_id,
            medication_data['name'],
            medication_data['dosage'],
            medication_data['frequency_hours'],
            medication_data.get('end_date'),
            medication_data.get('instructions')
        ))

        medication = cur.fetchone()
        conn.commit()

        if medication:
            return {
                "id": medication[0],
                "name": medication[1],
                "dosage": medication[2],
                "frequency_hours": medication[3],
                "start_date": medication[4],
                "end_date": medication[5],
                "instructions": medication[6],
                "is_active": medication[7]
            }
        return None

    except Exception as ex:
        print("❌ Error en create_medication:", repr(ex))
        raise
    finally:
        try:
            cur.close()
        except:
            pass
        try:
            conn.close()
        except:
            pass


def get_user_medications(user_id: int):
    query = """
            SELECT id, \
                   name, \
                   dosage, \
                   frequency_hours, \
                   start_date, \
                   end_date, \
                   instructions, \
                   is_active
            FROM medications
            WHERE user_id = %s \
              AND is_active = TRUE
            ORDER BY start_date DESC; \
            """
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(query, (user_id,))
        medications = cur.fetchall()

        result = []
        for med in medications:
            result.append({
                "id": med[0],
                "name": med[1],
                "dosage": med[2],
                "frequency_hours": med[3],
                "start_date": med[4],
                "end_date": med[5],
                "instructions": med[6],
                "is_active": med[7]
            })
        return result

    except Exception as ex:
        print("❌ Error en get_user_medications:", repr(ex))
        raise
    finally:
        try:
            cur.close()
        except:
            pass
        try:
            conn.close()
        except:
            pass

