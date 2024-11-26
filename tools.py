from datetime import datetime

# Obtiene el timestamp actual en segundos.

def get_unix_datetime():

    datetime_today = (datetime.now())
    formato = datetime_today.strftime("%Y%m%d%H%M")
    return (str(formato))
