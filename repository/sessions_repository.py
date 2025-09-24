from services.db_service import get_connection
from psycopg2.extras import RealDictCursor

def save_session(user_id: int, token: str, expires_at):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    # Marcar sesiones previas como inactivas
    cursor.execute("UPDATE user_sessions SET is_active = FALSE WHERE user_id = %s", (user_id,))

    cursor.execute("""
        INSERT INTO user_sessions (user_id, token, expires_at, is_active)
        VALUES (%s, %s, %s, TRUE)
        RETURNING id, user_id, token, expires_at, is_active
    """, (user_id, token, expires_at))

    session = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    return session

def get_active_session(user_id: int):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT * FROM user_sessions
        WHERE user_id = %s AND is_active = TRUE AND expires_at > NOW()
        ORDER BY created_at DESC LIMIT 1
    """, (user_id,))

    session = cursor.fetchone()
    cursor.close()
    conn.close()
    return session

def deactivate_session(token: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE user_sessions SET is_active = FALSE WHERE token = %s", (token,))
    conn.commit()
    cursor.close()
    conn.close()
def get_latest_active_session():
    """
    Obtiene la sesión activa más reciente de cualquier usuario
    """
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT us.*, u.email as user_email, u.name as user_name
        FROM user_sessions us
        JOIN users u ON us.user_id = u.id
        WHERE us.is_active = TRUE AND us.expires_at > NOW()
        ORDER BY us.created_at DESC 
        LIMIT 1
    """)

    session = cursor.fetchone()
    cursor.close()
    conn.close()
    return session

def get_active_sessions_count():
    """
    Obtiene el número de sesiones activas
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*) as active_count 
        FROM user_sessions 
        WHERE is_active = TRUE AND expires_at > NOW()
    """)

    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else 0