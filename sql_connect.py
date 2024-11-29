from dotenv import load_dotenv
import os
import pyodbc 

# Cargar las variables desde el archivo .env

def create_cursor() -> pyodbc.Cursor:
    """
    Genera un cursor para ejecutar comandos en la base de datos, las credenciales han de ser almacenadas en un archivo .env.

    Retorna:\n
    cursor: pyodbc.Cursor; cursor donde se podran ejecutar comandos SQL.
    """
    variables = get_variables()

    connection_string = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={variables["SERVER"]};"
        f"DATABASE={variables["DATABASE"]};"
        f"PWD={variables["PWD"]};"
        f"UID={variables["UID"]};"
        "UseIntegrated Security=No;"
        "DataEncryption=Optional;"
        "Language=(Default);"
        "DataEncryption=Optional;"
        "TrustServerCertificate=Yes;"

        # "Trusted_Connection=no;"  
        # "TrustServerCertificate=no;"
    )
    # print(connection_string)
    try:
        # Conectandonos a la data base 
        conn = pyodbc.connect(connection_string)
        print("Conexión exitosa a SQL SERVER")
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION;")  
        row = cursor.fetchone()
        print(f"Versión del servidor SQL: {row[0]}")
        return cursor
    
    except Exception as e:
        print(f"Error al conectar {e}")
        return None
     
def get_variables() -> dict:
    """
    Obtiene las variables del entorno almacenadas en un archivo .env.

    Parametros:
    None.

    Retorna:
    variables: dict; diccionario donde se almacenarán las variables para la base de datos
    """
    try:
        load_dotenv()  # Cargar el archivo .env
        variables = {
            "SERVER": os.getenv("SERVER"),
            "DATABASE": os.getenv("DATABASE"),
            "UID": os.getenv("UID"),
            "PWD": os.getenv("PWD")
        }
        print(f"Usuario: {variables['UID']}; Servidor: {variables['SERVER']}; Base de Datos: {variables['DATABASE']}")
        return variables
    except Exception as ex:
        print("Ocurrió un error al cargar las variables de entorno: ", ex)
        return None



if __name__ == "__main__":
    create_cursor()