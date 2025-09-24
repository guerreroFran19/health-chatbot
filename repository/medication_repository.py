from services.db_service import get_connection


def create_medication_repository(medication_data: dict):
    query = """
            INSERT INTO medications (user_id, name, dosage, frequency_hours, end_date, instructions, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, \
                    %s) RETURNING id, user_id, name, dosage, frequency_hours, start_date, end_date, instructions, is_active; \
            """

    try:
        conn = get_connection()
        if conn is None:
            raise Exception("No hay conexión a la base de datos")

        cur = conn.cursor()
        cur.execute(query, (
            medication_data['user_id'],
            medication_data['name'],
            medication_data['dosage'],
            medication_data['frequency_hours'],
            medication_data.get('end_date'),
            medication_data.get('instructions', ''),
            medication_data.get('is_active', True)
        ))

        new_medication = cur.fetchone()
        conn.commit()

        if new_medication:
            medication_dict = {
                "id": new_medication[0],
                "user_id": new_medication[1],
                "name": new_medication[2],
                "dosage": new_medication[3],
                "frequency_hours": new_medication[4],
                "start_date": new_medication[5],
                "end_date": new_medication[6],
                "instructions": new_medication[7],
                "is_active": new_medication[8]
            }
            print(f"✅ Medicamento creado: {medication_dict}")
            return medication_dict
        else:
            raise Exception("No se retornó ningún medicamento después del INSERT")

    except Exception as ex:
        print("❌ Error en create_medication_repository:", repr(ex))
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


def get_medications_repository(user_id: int):
    query = """
            SELECT id, \
                   user_id, \
                   name, \
                   dosage, \
                   frequency_hours, \
                   start_date, \
                   end_date, \
                   instructions, \
                   is_active
            FROM medications
            WHERE user_id = %s
            ORDER BY start_date DESC; \
            """

    try:
        conn = get_connection()
        if conn is None:
            raise Exception("No hay conexión a la base de datos")

        cur = conn.cursor()
        cur.execute(query, (user_id,))
        medications = cur.fetchall()

        medications_list = []
        for med in medications:
            medication_dict = {
                "id": med[0],
                "user_id": med[1],
                "name": med[2],
                "dosage": med[3],
                "frequency_hours": med[4],
                "start_date": med[5],
                "end_date": med[6],
                "instructions": med[7],
                "is_active": med[8]
            }
            medications_list.append(medication_dict)

        return medications_list

    except Exception as ex:
        print("❌ Error en get_medications_repository:", repr(ex))
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


def get_medication_repository(medication_id: int, user_id: int):
    query = """
            SELECT id, \
                   user_id, \
                   name, \
                   dosage, \
                   frequency_hours, \
                   start_date, \
                   end_date, \
                   instructions, \
                   is_active
            FROM medications
            WHERE id = %s \
              AND user_id = %s; \
            """

    try:
        conn = get_connection()
        if conn is None:
            raise Exception("No hay conexión a la base de datos")

        cur = conn.cursor()
        cur.execute(query, (medication_id, user_id))
        medication = cur.fetchone()

        if medication:
            medication_dict = {
                "id": medication[0],
                "user_id": medication[1],
                "name": medication[2],
                "dosage": medication[3],
                "frequency_hours": medication[4],
                "start_date": medication[5],
                "end_date": medication[6],
                "instructions": medication[7],
                "is_active": medication[8]
            }
            return medication_dict
        else:
            return None

    except Exception as ex:
        print("❌ Error en get_medication_repository:", repr(ex))
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


def get_medication_by_name(name: str, user_id: int):
    query = "SELECT id, name FROM medications WHERE name = %s AND user_id = %s;"
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query, (name, user_id))
        row = cur.fetchone()
        if row:
            return {"id": row[0], "name": row[1]}
        return None
    finally:
        try: cur.close()
        except: pass
        try: conn.close()
        except: pass


def update_medication_repository(medication_id: int, medication_data: dict):
    query = """
            UPDATE medications
            SET name            = %s, \
                dosage          = %s, \
                frequency_hours = %s, \
                end_date        = %s,
                instructions    = %s, \
                is_active       = %s
            WHERE id = %s \
              AND user_id = %s RETURNING id, user_id, name, dosage, frequency_hours, start_date, end_date, instructions, is_active; \
            """

    try:
        conn = get_connection()
        if conn is None:
            raise Exception("No hay conexión a la base de datos")

        cur = conn.cursor()
        cur.execute(query, (
            medication_data.get('name'),
            medication_data.get('dosage'),
            medication_data.get('frequency_hours'),
            medication_data.get('end_date'),
            medication_data.get('instructions', ''),
            medication_data.get('is_active', True),
            medication_id,
            medication_data['user_id']
        ))

        updated_medication = cur.fetchone()
        conn.commit()

        if updated_medication:
            medication_dict = {
                "id": updated_medication[0],
                "user_id": updated_medication[1],
                "name": updated_medication[2],
                "dosage": updated_medication[3],
                "frequency_hours": updated_medication[4],
                "start_date": updated_medication[5],
                "end_date": updated_medication[6],
                "instructions": updated_medication[7],
                "is_active": updated_medication[8]
            }
            return medication_dict
        else:
            return None

    except Exception as ex:
        print("❌ Error en update_medication_repository:", repr(ex))
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


def delete_medication_repository(medication_id: int, user_id: int):
    query = "DELETE FROM medications WHERE id = %s AND user_id = %s;"

    try:
        conn = get_connection()
        if conn is None:
            raise Exception("No hay conexión a la base de datos")

        cur = conn.cursor()
        cur.execute(query, (medication_id, user_id))
        conn.commit()

        # Si se afectó alguna fila, fue exitoso
        return cur.rowcount > 0

    except Exception as ex:
        print("❌ Error en delete_medication_repository:", repr(ex))
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