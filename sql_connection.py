import psycopg2
from psycopg2 import sql
from env_vars_local import db_params


class SqlConnection:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.conn = psycopg2.connect(**db_params)
        self.cursor = self.conn.cursor()

    def execute_query(self, query: str):
        sql_query = sql.SQL(query)
        self.cursor.execute(sql_query)
        rows = self.cursor.fetchall()

        return rows

    def __del__(self):
        self.cursor.close()
        self.conn.close()

