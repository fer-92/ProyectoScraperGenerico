from datetime import datetime
import time


ts = time.time()

def mi_time():
    fecha = datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    hora = datetime.fromtimestamp(ts).strftime('%H:%M:%S')

    return (fecha,hora)