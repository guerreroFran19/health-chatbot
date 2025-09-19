import psycopg2

def get_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="healthdb",
        user="admin",
        password="admin",
        port="5432"
    )
    conn.set_client_encoding('UTF8')


