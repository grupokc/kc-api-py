import streamlit as st
import pandas as pd 
import subprocess
import os 


def inicio():

    st.title("Bienvenido a la KC-API de procesamiento de archivos")
    st.header(f"Version: {"0.0.9"}", divider = "blue")


def boton_cargar():
    btnn_carga = st.button("Cargar archivos",
                           key= "btnn_carga",
                           type= "primary",
                           help="selecciona los archivos que deseas procesar",
                           use_container_width= True)
    
    if (btnn_carga):
        print("SE HA PRESIONADO EL BOTON DE CARGA")

        st.header("HOLA ")


def test():

    bttn = st.file_uploader(label= "Subir archivos",
                            type = "csv",
                            accept_multiple_files= True, 
                            key= "bttn_uploader", 
                            label_visibility= 'visible',
                            
                            )
    for file in bttn:
        print(file)


def ventana_carga():
    ...