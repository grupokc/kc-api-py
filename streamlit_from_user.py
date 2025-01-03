import streamlit as st
import pandas as pd 
import subprocess
import os 


def inicio():
    st.sidebar.title("Inicio")

    st.title("Bienvenido a la :blue[KC-API] de procesamiento de archivos")
    st.header(f"Version: :gray[{"0.0.33"}]", divider = "blue")



def boton_cargar():
    btnn_carga = st.button("Cargar archivos",
                           key= "btnn_carga",
                           type= "primary",
                           help="selecciona los archivos que deseas procesar",
                           use_container_width= True)
    
    if (btnn_carga):
        print("SE HA PRESIONADO EL BOTON DE CARGA")

import requests
# Función para cargar archivos
import streamlit as st
import requests

# Función para cargar archivos desde Streamlit
def test():
    uploaded_files = st.file_uploader(
        label="Subir archivos",
        type="csv",
        accept_multiple_files=True,
        key="bttn_uploader",
        label_visibility="visible",
    )

    if uploaded_files:
        st.write(f"Archivos subidos: :green[{[file.name for file in uploaded_files]}]")
    else:
        st.warning("No se han subido archivos aún.")
    
    return uploaded_files

# Función para enviar los archivos como un grupo a la API

import io 
# Función para enviar archivos y manejar el archivo de respuesta
def enviar_descargar_archivos(url_upload: str, archivos):
    if archivos:
        bttn_enviar = st.button(
            label="Transformar archivos",
            use_container_width=True,
            type="primary"
        )
        if bttn_enviar:
            try:
                st.warning("Cargando ...")

                # Preparar archivos para enviar
                files = [("files", (archivo.name, archivo.getvalue())) for archivo in archivos]

                # Enviar archivos
                response = requests.post(
                    url=url_upload,
                    files=files
                )
                # Verificar si la solicitud fue exitosa
                if response.status_code == 200:
                    st.success("Archivos enviados correctamente.")

                    # Guardar el archivo devuelto temporalmente
                    result_filename = response.headers.get(
                        "Content-Disposition", "result.csv"
                    ).split("filename=")[-1]
                    
                    st.info(f"Archivo devuelto: {result_filename}")

                    file_content = io.StringIO(response.content.decode("utf-8"))
                    df = pd.read_csv(file_content)
                    st.dataframe(df.head(100))


                    # Mostrar botón para descargar el archivo
                    st.download_button(
                        label="Descargar archivo procesado",
                        data=response.content,
                        file_name=result_filename,
                        mime="text/csv"
                    )

       
                else:
                    st.error(f"Error al enviar los archivos. Status: {response.status_code}")
                    st.write(response.json())
            except Exception as e:
                st.error(f"Ocurrió un error: {e}")
    else:
        st.warning("Sube archivos antes de enviarlos.")



import pandas as pd 
def ver_respuesta(df : pd.DataFrame):
    df.head()