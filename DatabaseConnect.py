import pyodbc

def create_connection():
    server = 'HAX'
    database = 'HEPAS'
    username = 'HAX/mohib'
    password = ''
    driver = 'ODBC Driver 17 for SQL Server'  # Use the appropriate ODBC driver

    connection_string = f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};UID={username};PWD={password};TRUSTED_CONNECTION=YES;"

    try:
        connection = pyodbc.connect(connection_string)
        print("Connected to db!")
        return connection
    except Exception as e:
        print(f"Error: {str(e)}")
        return None
