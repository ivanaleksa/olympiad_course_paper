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
        self.conn_url = f"postgresql://{db_params['user']}:{db_params['password']}@{db_params['host']}/{db_params['database']}"
        self.conn = psycopg2.connect(**db_params)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.cursor.close()
        self.conn.close()


class SqlExecutor(SqlConnection):
    def select_query_builder(self, table_name: str, columns: tuple = None, needed_conditions: str = '', sorting: dict = {}, all_col: bool = True):
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
        SELECT {','.join(columns) if not all_col else '*'} 
        FROM {table_name} {needed_conditions} 
        {"ORDER BY " + ', '.join([f"{key} {sorting[key]}" for key in sorting]) if sorting != {} else ''};
        """

        return pd.read_sql(sql_query, self.conn_url)

    def insert_row_query_builder(self, table_name: str, columns: tuple, values: list):
        """
        This method builds a query for inserting a new row into a table.
        Params:
            columns - a tuple of columns' names like in DB;
            values - a list of values for named columns;
            table_name - name of a table where you want to insert values.
        """

        query = f"""
        BEGIN;
        INSERT INTO {table_name} ({', '.join(columns[1:])}) VALUES ({', '.join(["'" + elem + "'" for elem in values])});
        COMMIT;
        """
        sql_query = sql.SQL(query)
        self.cursor.execute(sql_query)

    def delete_row_query_builder(self, table_name: str, id_: str):
        """
        This method builds a query for deleting a row from a table using an id of the row.
        Params:
            table_name - name of a table where you want to delete a row;
            id - an id of the row.
        """

        query = f"""
        BEGIN;
        DELETE FROM {table_name}
        WHERE id = {id_};
        COMMIT;
        """

        sql_query = sql.SQL(query)
        self.cursor.execute(sql_query)

    def update_row_query_builder(self, table_name: str, id_: str, values: dict):
        """
        This method builds a query for updating a row with id = id.
        Params:
            table_name - name of a table where you want to update a row;
            id - record's id which you want to update;
            values - a dictionary where key is a column name, value is its value.
        """

        query = f"""
        BEGIN;
        UPDATE {table_name}
        SET {', '.join([key + ' = ' + "'" + values[key] + "'" for key in values])}
        WHERE id = {id_};
        COMMIT;
        """

        sql_query = sql.SQL(query)
        self.cursor.execute(sql_query)
