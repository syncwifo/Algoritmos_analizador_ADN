import json
import random

datos = []

for i in range(500):
    nombre = i
    secuencia = ""
    for j in range(8):
        letra = random.choice(["A", "T", "G", "C"])
        secuencia += letra
    informacion = f"Informacion de la secuencia {nombre}"
    dato = {"nombre": f"Secuencia {nombre}", "secuencia": secuencia, "informacion": informacion}
    datos.append(dato)

with open("Secuencias.json", "w") as f:
    json.dump(datos, f, indent=4)






