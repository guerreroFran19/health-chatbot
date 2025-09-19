# En repository/user_repository.py
from services.db_service import get_connection


def create_user(name: str, email: str, password: str):
    query = """
    INSERT INTO users (name, email, password)
    VALUES (%s, %s, %s)
    RETURNING id, name, email;
    """
    try:
        conn = get_connection()
        if conn is None:
            raise Exception("No hay conexión a la base de datos")

        cur = conn.cursor()
        cur.execute(query, (name, email, password))
        new_user = cur.fetchone()
        conn.commit()

        if new_user:
            # Convertir tupla a diccionario
            user_dict = {
                "id": new_user[0],
                "name": new_user[1],
                "email": new_user[2]
            }
            print(f"✅ Usuario creado: {user_dict}")
            return user_dict
        else:
            raise Exception("No se retornó ningún usuario después del INSERT")

    except Exception as ex:
        print("❌ Error en create_user:", repr(ex))
        raise  # Re-lanza la excepción para que el servicio la capture
    finally:
        try:
            cur.close()
        except:
            pass
        try:
            conn.close()
        except:
            pass