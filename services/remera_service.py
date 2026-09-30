import json

def obtener_remeras():

    with open("database/remeras.json", "r") as archivo:

        remeras = json.load(archivo)

    return remeras