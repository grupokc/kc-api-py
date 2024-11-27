from dotenv import load_dotenv
import os
import pyodbc 

# Cargar las variables desde el archivo .env
load_dotenv()

# SERVER = os.getenv("SERVER")
# DATABASE = os.getenv("DATABASE")

def create_cursor():

    print(f"{SERVER}, {DATABASE}")
    SERVER = os.getenv("SERVER")
    DATABASE = os.getenv("DATABASE")

    connection_string = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={SERVER};"  # Nombre del servidor como aparece en tu configuración
        f"DATABASE={DATABASE};"  # Cambia por el nombre de tu base de datos, 
        "Trusted_Connection=yes;"  # Usa autenticación de Windows
        "TrustServerCertificate=yes;"  # Permite confiar en el certificado
    )
    
    try:
    # Conectandonos a la data base 
        conn = pyodbc.connect(connection_string)
        print("Conexión exitosa")
        # Crear un cursor para ejecutar consultas
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION;")  # Ejemplo de consulta
        row = cursor.fetchone()
        print(f"Versión del servidor SQL: {row[0]}")
        return cursor
    except Exception as e:
        print(f"Error al conectar {e}")