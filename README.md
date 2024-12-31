# kc-api-py

# En MAC

```
python3 -m venv venv
source venv/bin/activate  
pip install fastapi uvicorn python-multipart pandas
pip install -r requirements.txt
uvicorn main:app --reload

```
### Configuración del archivo .env
Este proyecto requiere un archivo `.env` en la raiz del proyecto con las siguientes variables de entorno:
SERVER=nombre_del_servidor
DATABASE=nombre_base_datos
USERNAME=usuario
PASSWORD=contraseña

### Instalación del ODBC Driver 18 para SQL Server

El proyecto requiere el **ODBC Driver 18 para SQL Server** para conectarse a la base de datos SQL Server.

#### Instrucciones para Windows:

1. Descarga el controlador desde el sitio oficial de Microsoft:  
   [Microsoft ODBC Driver 18 for SQL Server](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)
   
2. Sigue las instrucciones de instalación en el sitio.

3. Asegúrate de que el controlador esté instalado correctamente ejecutando el siguiente comando en tu terminal de Windows:
   ```bash
   odbcad32


#### **Para Linux/Mac:**

En sistemas Linux o macOS, el proceso es similar, pero las instrucciones de instalación varían según la distribución. Aquí te dejo un ejemplo para Ubuntu:

En Linux (Ubuntu), usa los siguientes comandos:

# Agregar el repositorio de Microsoft y actualizar los paquetes
sudo apt-get update
sudo apt-get install -y unixodbc-dev

# Instalar el controlador ODBC para SQL Server
sudo apt-get install -y msodbcsql18

