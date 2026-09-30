import json

def obtener_tazas():

    with open("database/tazas.json", "r") as archivo:

        tazas = json.load(archivo)

    return tazas