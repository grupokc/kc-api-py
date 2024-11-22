import pandas as pd
import os

def process_and_merge_files(file_paths) -> tuple:
    dataframes = []
    for file_path in file_paths:
        df = pd.read_csv(file_path, sep= ",", encoding= "latin1")
        # Aquí puedes agregar cualquier procesamiento específico que necesites
        # Por ejemplo, podríamos añadir una columna con el nombre del archivo:
        df.loc[:, 'archivo_origen'] = os.path.basename(file_path) # Dentro del df se añade de que archivo se obtuvo el registro
        dataframes.append(df)
    
    # Unir todos los dataframes
    result = pd.concat(dataframes, ignore_index=True)
    
    # Guardar el resultado
    result_path = os.path.join("results", "resultado_final.csv") #Devuelve /results/resultado_final.csv
    result.to_csv(result_path, index=False)  

    info_processed = f"Se procesaron {len(file_paths)} archivos, con {result.shape[0]} registros"
    
    return result_path, info_processed
