from services.db_service import get_connection
import bcrypt


def create_user(name: str, email: str, password: str):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    query = """
            INSERT INTO users (name, email, password)
            VALUES (%s, %s, %s) RETURNING id, name, email; \
            """
    try:
        conn = get_connection()
        if conn is None:
            raise Exception("No hay conexión a la base de datos")

        cur = conn.cursor()
        cur.execute(query, (name, email, hashed_password.decode('utf-8')))
        new_user = cur.fetchone()
        conn.commit()

        if new_user:
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
def get_user_by_id(user_id: int):
    query = "SELECT id, name, email, password FROM users WHERE id = %s;"
    try:
        conn = get_connection()
        if conn is None:
            raise Exception("No hay conexión a la base de datos")

        cur = conn.cursor()
        cur.execute(query, (user_id,))
        user = cur.fetchone()

        if user:
            user_dict = {
                "id": user[0],
                "name": user[1],
                "email": user[2],
                "password": user[3]
            }
            return user_dict
        else:
            return None

    except Exception as ex:
        print("❌ Error en get_user_by_id:", repr(ex))
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

def get_user_by_email(email: str):
    query = "SELECT id, name, email, password FROM users WHERE email = %s;"
    try:
        conn = get_connection()
        if conn is None:
            raise Exception("No hay conexión a la base de datos")

        cur = conn.cursor()
        cur.execute(query, (email,))
        user = cur.fetchone()

        if user:
            user_dict = {
                "id": user[0],
                "name": user[1],
                "email": user[2],
                "password": user[3]
            }
            return user_dict
        else:
            return None

    except Exception as ex:
        print("❌ Error en get_user_by_email:", repr(ex))
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