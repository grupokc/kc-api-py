from datetime import datetime

# Obtiene el timestamp actual en segundos.

def get_unix_datetime():

    unix_timestamp = int(datetime.now().timestamp())
    return (unix_timestamp)
