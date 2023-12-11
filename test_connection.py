from sql_connection import SqlConnection

conn = SqlConnection()

res = conn.execute_query("SELECT * FROM olympiad.countries")
print(res)