import pandas as pd
import os

def process_and_merge_files(file_paths):
    dataframes = []
    for file_path in file_paths:
        df = pd.read_csv(file_path)
        # Aquí puedes agregar cualquier procesamiento específico que necesites
        # Por ejemplo, podríamos añadir una columna con el nombre del archivo:
        df['archivo_origen'] = os.path.basename(file_path)
        dataframes.append(df)
    
    # Unir todos los dataframes
    result = pd.concat(dataframes, ignore_index=True)
    
    # Guardar el resultado
    result_path = os.path.join("results", "resultado_final.csv")
    result.to_csv(result_path, index=False)
    
    return result_path

