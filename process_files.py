import pandas as pd
import os
import tools

def process_and_merge_files(file_paths: list) -> tuple:
    try:
        print("Procesando ...")
        dataframes = []
        for file_path in file_paths:
            df = pd.read_csv(file_path, sep= ",", encoding= "latin1")
            # Añadir la procendencia del registro en la ultima columna
            df.loc[:, 'archivo_origen'] = os.path.basename(file_path) 
            dataframes.append(df)

        # Unimos todos los data frames
        result = pd.concat(dataframes, ignore_index=True)
        # Modificaciones al DataFrame resultante
        # 1. Quitar caracteres especiales a la columnas nombres
        indices_nombre = find_column("Nombre", dataframe = result) # Retorna los indices donde hay coincidencias
        for indice_nombre in indices_nombre:
            result.iloc[:, indice_nombre] = result.iloc[:, indice_nombre].apply(no_special_characters)
        # 2. Quitar letras de la penultima columna
        result.iloc[:, -2] = result.iloc[:, -2].apply(no_letters)

        # Guardar el resultado
        dateFromatUnix = tools.get_unix_datetime() # Formato Unix
        new_name = f"processed_{dateFromatUnix}.csv"
        result_path = os.path.join("results", new_name) #Devuelve /results/new_name
        result.to_csv(result_path, index=False)  

        info_processed = f"Se procesaron {len(file_paths)} archivos,  con {result.shape[0]} registros"

        print(result_path, " || ", info_processed)
    except Exception as ex:
        info_processed = f"Error: {ex}"
        print(info_processed)
    finally:
        return result_path, info_processed


def no_letters(texto: str) -> int:
    """
    La función elimina letras de cualquier cadena,
    dejando solo los números como un entero.
    """
    texto = str(texto)
    sin_letras = "".join(char for char in texto if char.isdigit())
    return int(sin_letras) if sin_letras else 0


def no_special_characters(texto :str) -> str:
    """
    La función se encarga de quitar caracteres que no sean literales
    """
    texto = texto.strip()
    texto = texto.replace("?", "Ñ").strip()

    return texto

def find_column(to_find: str, dataframe: pd.DataFrame) -> list:
    """
    Encuentra en las columnas del data frame alguna coincidencia para retornar su indice, no es necesaria
    lo coincidencia caracter a caracter, basta que to_find este contenido o propiamente contenido en la 
    columna.

    Parametros.
    to_find: str; la cadena que se buscara dentro de las columnas,

    Retorna. 
    coincidencias: list<int>, si encontró una coincidencia.
    None, si no encontro coincidencias.
    """
    coincidencias = []
    try:
        indice_columna = [(x,i) for x,i in zip(list(dataframe.columns), range(len(dataframe.columns)))]

        for columna, idx_columna in indice_columna:
            if (to_find.strip().upper() in columna.upper()):
                coincidencias.append(idx_columna)
            
        if (len(coincidencias) == 0):
            print("Ninguna columna coincide con el criterio de busqueda")
            return None
        
    except Exception as e:
        print(f"No se pudo ejecutar: {e}")
    return coincidencias
