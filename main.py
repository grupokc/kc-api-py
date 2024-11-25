from fastapi import FastAPI, File, UploadFile
from typing import Annotated

from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException
import pandas as pd
import os
from typing import List
from process_files import process_and_merge_files

API_VERSION = "0.0.3"

app = FastAPI()

UPLOAD_DIRECTORY = "uploads"
RESULT_DIRECTORY = "results"

# Asegúrate de que los directorios existan
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
os.makedirs(RESULT_DIRECTORY, exist_ok=True)

@app.post("/upload/")
async def upload_files(files: List[UploadFile] = File(...)):
    print(files)
    # if len(files) != 6:
    #     # return {"error": "Se deben subir exactamente 6 archivos"}
    #     raise HTTPException(status_code=400, detail="Se deben subir exactamente 6 archivos")

    # file_paths = []
    # for file in files:
    #     if not file.filename.endswith(".csv"):
    #         # El raise va a detener la ejecución en cuanto suceda la excepción 
    #         raise HTTPException(status_code=400, detail=f"El archivo {file.filename} NO es un CSV")
    #     file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
    #     with open(file_path, "wb") as buffer:
    #         buffer.write(await file.read())
    #     file_paths.append(file_path)
    # Obtenemos la ruta del resultado y la información del precosado 
    # result_path, info_porcessed = process_and_merge_files(file_paths)
    return {"message": "Upload finalizado"}

    # return FileResponse(result_path,
    #                     headers= {"Info-Message": f"{info_porcessed}"},
    #     
    #                 filename="resultado_final.csv")
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

