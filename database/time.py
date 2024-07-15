from datetime import datetime

# ¡Ojo! Aunque en el navegador pueda variar la interfaz
# , las fechas en HTML siempre estan en formato YYYY-MM-DD
read_format = "%Y-%m-%d"

# Clase estática, similar a un namespace de C++
class Time:
    def string_to_object(string):
        return datetime.strptime(string, read_format)

    # Todavia no sé si esta función es necesaria. Ignorar
    def object_to_string(object):
        input_format = read_format # placeholder
        return datetime.strftime(object, input_format)

    def now_as_object():
        now = datetime.now()
        return now

    # Todavia no sé si esta función es necesaria. Ignorar
    def now_as_string():
        now = datetime.now()
        return Time.object_to_string(now)

