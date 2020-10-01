from dotenv import load_dotenv
import pyodbc
import os
load_dotenv()

def get_db_connection():
  print("Connecting to DB Host: ", os.getenv('DB_HOST'))
  return pyodbc.connect(f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={os.getenv('DB_HOST')},{os.getenv('DB_PORT')};DATABASE={os.getenv('DB_DATABASE')};UID={os.getenv('DB_USERNAME')};PWD={os.getenv('DB_PASSWORD')}")

def get_cursor(cnxn):
  cursor = cnxn.cursor()
  cursor.execute("select @@version;")
  row = cursor.fetchone()
  while row:
    row = cursor.fetchone()
  return cursor

def select_query(query):
  cursor = get_cursor(get_db_connection())
  cursor.execute(f'''
    {query}
  ''' )
  columns = [column[0] for column in cursor.description]
  results = []
  for row in cursor.fetchall():
    results.append(dict(zip(columns, row)))
  return results

def execute_sql(sql):
  db = get_db_connection()
  cursor = get_cursor(db)
  try:
    cursor.execute(sql)
    db.commit()
    return 0
  except Exception as e:
    print(e)
    return e
