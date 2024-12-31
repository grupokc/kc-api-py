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
            print(f"{df.shape[0]}") 
            dataframes.append(df)

        # Unimos todos los data frames
        result = pd.concat(dataframes, ignore_index=True)
        # Modificaciones al DataFrame resultante
        # 1. Quitar caracteres especiales a la columnas nombres!""
        indices_nombre = find_column("Nombre", dataframe = result) # Retorna los indices donde hay coincidencias
        indices_rfc = find_column("RFC", dataframe= result)

        for indice_nombre, indice_rfc in zip(indices_nombre, indices_rfc):
            result.iloc[:, indice_nombre] = result.iloc[:, indice_nombre].apply(no_special_characters)
            result.iloc[:, indice_rfc] = result.iloc[: , indice_rfc].apply(no_special_characters)

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

    Parametros.
    texto: str; cadena donde se quitaran los caracteres especiales
    """
    texto = texto.strip()

    texto = texto.replace("?", "Ñ").strip()
    try: 
        texto = texto.replace("�", "Ñ").strip()
    
    except:
        pass

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



def recortar_df(
        df : pd.DataFrame,
        col_indice: int = 1,
        col_nombre: str = None,
        sentido: str = "left"        ) -> pd.DataFrame:
    """
    Corta un dataframe dado en el indice indicado, o bien en el nombre de la columna, devuelve todo aquello que 
    estuvo antes o despues  del corte.

    Parametros.
    df: pd.DataFrame, es el df donde se realizará el recorte.
    col_indice: int; indica el indice donde cortara.
    col_nombre: str; (Opcional) indica el nombre de la columna donde se recortara.
    sentido; str, indica que lado del recorte se devolvera

    Retorna:
    pd.DataFrame; dataFrame recortado.

    """
    # Obtenemos el nombre de las columnas en lista  
    columnas = list(df.columns)
    indice_columna = {columna.upper().strip() : i 
                      for i, columna in enumerate(columnas)}
    
    print(indice_columna)
    if (col_nombre != None):
        try:
            # Obtenemos el indice para hacer el recorte 
            col_indice = indice_columna[col_nombre.upper().strip()]
        except KeyError as e:
            print(f"No existe la columna: {col_nombre} en el DataFrame proporcionado \n {e}")
            return 
    
    # Tomamos todas las columnas de la derecha 
    if (sentido == "right"):
        columnas_requeridas = columnas[col_indice: ]
    else:
        columnas_requeridas = columnas[: col_indice + 1]
        
    # Obtenerlas en un data frame
    df_recortado = df[columnas_requeridas]

    return df_recortado


def insertar_columnas(dataFrame: pd.DataFrame,
                      posicion_insertado: int,
                      nombre_insertadas: list[str],
                      datos_columnas: list[list | pd.Series]
                      ) -> pd.DataFrame:
    """
    Inserta columnas en el dataframe en el indice deseado <n>, entonces los datos insertados estarán en la posicion n + 1.

    Parametros.
    dataFrame: pd.DataFrame; dataframe para ser insertado.
    posicion_insertado: int; ubica el corte donde se hará la insercción.
    nombre_insertadas: list; nombre de las nuevas columnas a insertar
    datos_columnas: list[list | pd.Series]; representa los datos que seran insertados en cada columna por insertar.

    Retorna.
    pd.DataFrame
    """
    # Verificar que la cantidad de nombres para insertar conincida con la cantidad de listas proporcionadas
    if len(nombre_insertadas) != len(datos_columnas):
        print(f"Error: NO se ha proporcionado la misma cantidad de columnas como de datos, se proporcionaron {len(nombre_insertadas)} columnas y {len(datos_columnas)} datos")
        return 
    
    # Verificar si el tamaño de todas las series 
    for idx_dato_columna, dato_columna in enumerate(datos_columnas):
        if (len(dato_columna) != dataFrame.shape[0]):
            print(dato_columna)
            print(f"La lista numero {idx_dato_columna} deben de ser de la misma longitud que la del data frame, deben tener {dataFrame.shape[0]} las listas proporcionadas")
            return 
    try: 
        recorte_izq = recortar_df(dataFrame, posicion_insertado)
        recorte_derecha = recortar_df(dataFrame, posicion_insertado + 1, sentido= "right")

        # Formar Df temporal 
        df_temp = pd.DataFrame(data=zip(*datos_columnas), columns= nombre_insertadas)
        
        # Concatenar por df izquierda 
        df_pegado = pd.concat([recorte_izq, df_temp, recorte_derecha], axis= 1)

        return df_pegado

    except Exception as e:
        print(f"Error al insertar: {e}")
        return 
    
