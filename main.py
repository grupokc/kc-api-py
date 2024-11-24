from fastapi import FastAPI, File, UploadFile
from typing import Annotated

from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException
import pandas as pd
import os
from typing import List
from process_files import process_and_merge_files

API_VERSION = "0.0.4"

app = FastAPI(
    title = "KC-API",
    version= API_VERSION
)

UPLOAD_DIRECTORY = "uploads"
RESULT_DIRECTORY = "results"

# Asegúrate de que los directorios existan
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
os.makedirs(RESULT_DIRECTORY, exist_ok=True)

@app.post("/upload/")
async def upload_files(files: List[UploadFile] = File(...)):
    try:
        for file in files:
            print(file)
            # Lista para almecenarlos en la carpeta uploads
            file_paths = []
            # Quitamos los que no sean .csv y detenemos la ejecucion 
            if not file.filename.endswith(".csv"):
                raise HTTPException(status_code=400, detail=f"El archivo {file.filename} NO es un CSV")
            else:

                file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
                with open(file_path, "wb") as buffer:
                    buffer.write(await file.read())
                file_paths.append(file_path)

            print(file_paths)

        result_path, info_porcessed = process_and_merge_files(file_paths)

        return FileResponse(result_path,
                            headers= {"Info-Message": f"{info_porcessed}"},
            
                            filename="resultado_final.csv")
    except:
        raise HTTPException(status_code=400, detail="Se deben subir exactamente 6 archivos")


@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]): 
    return {"file_size": len(file)}


@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de procesamiento de archivos"}

@app.get("/version")
async def get_version():
    return {"version": API_VERSION}


@app.get("/saludo")
async def saludar():
    return {"message": "Saludos Fraternos"}

