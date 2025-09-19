# repository/user_repository.py
from services.db_service import get_connection

def create_user(name: str, email: str, password: str):
    query = """
    INSERT INTO users (name, email, password)
    VALUES (%s, %s, %s)
    RETURNING id, name, email;
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query, (name, email, password))
        new_user = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return new_user
    except Exception as ex:
        print("❌ Error en create_user:", repr(ex))  # repr evita el decode raro
        raise  # importante para que FastAPI capture el error real

