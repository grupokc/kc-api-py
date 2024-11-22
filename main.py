from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import pandas as pd
import os
from typing import List
from process_files import process_and_merge_files

API_VERSION = "0.0.1"

app = FastAPI()

UPLOAD_DIRECTORY = "uploads"
RESULT_DIRECTORY = "results"

# Asegúrate de que los directorios existan
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
os.makedirs(RESULT_DIRECTORY, exist_ok=True)

@app.post("/upload/")
async def upload_files(files: List[UploadFile] = File(...)):
    if len(files) != 6:
        return {"error": "Se deben subir exactamente 6 archivos"}

    file_paths = []
    for file in files:
        file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        file_paths.append(file_path)

    result_path = process_and_merge_files(file_paths)
    return FileResponse(result_path, filename="resultado_final.csv")

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de procesamiento de archivos"}

@app.get("/version")
async def get_version():
    return {"version": API_VERSION}

