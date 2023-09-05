import psycopg2
from decouple import AutoConfig
config = AutoConfig()

DATABASE_CONFIG = {
    'dbname': config('DB_NAME'),
    'user': config('DB_USER'),
    'password': config('DB_PASSWORD'),
    'host': config('DB_HOST'),
    'port': config('DB_PORT')
}

def get_connection():
    return psycopg2.connect(**DATABASE_CONFIG)
# получим общее количество записей
def get_total_records(server_name=None):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            if server_name: # если сервер указан выводим записи только по нему
                cursor.execute(
                    "SELECT COUNT(*) FROM vw_tmp_import WHERE server_name = %s",
                    (server_name,)
                )
            else:
                cursor.execute(  # иначе выводим количество всех строк датафрейма
                    "SELECT COUNT(*) FROM vw_tmp_import"
                )
            return cursor.fetchone()[0]

# получим конкретную порцию данных со смещением для вывода в пагинатор
def get_records(server_name, limit, offset):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            if server_name == "ALL" or not server_name: # обрабоатем вып. меню
                cursor.execute(
                    f"SELECT * FROM vw_tmp_import LIMIT {limit} OFFSET {offset}"
                )
            else: # в меню выбран конкретный сервер
                cursor.execute(
                    f"SELECT * FROM vw_tmp_import WHERE server_name = %s LIMIT {limit} OFFSET {offset}",
                    (server_name,)
                )
            return cursor.fetchall()


# получим список серверов для выпадающего меню
def get_servers():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT DISTINCT server_name FROM vw_tmp_import")
            return cursor.fetchall()
