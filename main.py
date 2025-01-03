from email.utils import formatdate
from fastapi import FastAPI, File, UploadFile
from typing import Annotated
from tools import get_unix_datetime
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException
import pandas as pd
from typing import List
import os
from process_files import process_and_merge_files
import streamlit as st
from streamlit_from_user import inicio, boton_cargar, test
import subprocess
import uvicorn


API_VERSION = "0.0.9"

app = FastAPI(
    title = "KC-API",
    version= API_VERSION
)

def start_server():
    print("Servidor iniciado")
    uvicorn.run(app= app, port = 8000, host= '127.0.0.1')

UPLOAD_DIRECTORY = "uploads"
RESULT_DIRECTORY = "results"

# Asegúrate de que los directorios existan
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
os.makedirs(RESULT_DIRECTORY, exist_ok=True)

@app.post("/upload/")
async def upload_files(files: List[UploadFile] = File(...)):
    try:
        file_paths = []
        dateUnix = get_unix_datetime() # Para nombrar a los archivos
        for file in files:
            if (file.filename == ""):
                raise HTTPException(status_code=400, detail=f"Debe mandar al menos 1 archivo .csv")
            # Lista para almecenarlos en la carpeta uploads
            # Quitamos los que no sean .csv y detenemos la ejecucion 
            if file.filename.endswith(".csv") == False:
                raise HTTPException(status_code=400, detail=f"El archivo {file.filename} NO es un CSV")
            else:
                new_name_file = file.filename.replace(".csv","_" + dateUnix + ".csv")
                file_path = os.path.join(UPLOAD_DIRECTORY, new_name_file)
                with open(file_path, "wb") as buffer:
                    buffer.write(await file.read())
                file_paths.append(file_path)

        [print(x) for x in file_paths]
        result_path, info_porcessed = process_and_merge_files(file_paths)

        print(result_path)
        return FileResponse(path= result_path,
                            status_code= 200,
                            headers= {"Info-Message": f"{info_porcessed}"},
                            media_type= ".csv",
                            filename= os.path.basename(result_path), 
                            )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")

# @app.post("/files/") �
# async def create_file(file: Annotated[bytes, File(...)]): 
#     return {"file_size": len(file)}


@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de procesamiento de archivos"}

@app.get("/version")
async def get_version():
    return {"version": API_VERSION}


@app.get("/saludo")
async def saludar():
    return {"message": "Saludos Fraternos"}



def levantar_servidor():
    os.system('echo Levantando servidor...')
    try:
        os.system(r'uvicorn main:app')
        
    except Exception as e:
        print(f"echo No ha sido posible levantar el servidor {e}")





if __name__ == "__main__":
    print("Servicio inicializado")

    # Pantalla de inicio 
    inicio()

    # Mostrar boton de carga al usuario 
    # boton_cargar()
    test()

    # levantamos el servidor 
    # start_server()
