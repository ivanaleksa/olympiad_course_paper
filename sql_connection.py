import psycopg2
from psycopg2 import sql
from env_vars_local import db_params
import pandas as pd


class SqlConnection:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.conn_url = f"postgresql://student:student@127.0.0.1/alexandrov"
        self.conn = psycopg2.connect(**db_params)
        self.cursor = self.conn.cursor()

    def execute_query(self, query: str):
        return pd.read_sql(query, self.conn_url)

    def insert_row(self, columns: tuple, values: list, table_name: str):
        query = f"""
        BEGIN;
        INSERT INTO {table_name} ({', '.join(columns[1:])}) VALUES ({', '.join(values)});
        COMMIT;
        """
        sql_query = sql.SQL(query)
        self.cursor.execute(sql_query)

    def __del__(self):
        self.cursor.close()
        self.conn.close()


class SqlExecutor(SqlConnection):
    def select_query_builder(self, table_name: str, columns: tuple, needed_conditions: str = '', sorting: dict = {}):
        """
        This method builds a query for item selection.
        Params:
            table_name - a name of needed table with schema, for example olympiad.participants;
            columns - a tuple of columns for rendering;
            needed_conditions - a string with WHOLE "WHERE" sql statement, like "WHERE id > 5";
            sorting - a dictionary where kays are columns and values their sorting type "DESC" or "ASC", be careful with its order.
        Returns pd.DataFrame object if everything's ok.
        """
        sql_query = f"""
        SELECT {','.join(columns)} 
        FROM {table_name} {needed_conditions} 
        {"ORDER BY " + ', '.join([f"{key} {sorting[key]}" for key in sorting]) if sorting != {} else ''};
        """

        return pd.read_sql(sql_query, self.conn_url)

    def insert_row_query(self, columns: tuple, values: list, table_name: str):
        query = f"""
        BEGIN;
        INSERT INTO {table_name} ({', '.join(columns[1:])}) VALUES ({', '.join(values)});
        COMMIT;
        """
        sql_query = sql.SQL(query)
        self.cursor.execute(sql_query)
