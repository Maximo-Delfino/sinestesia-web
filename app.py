from flask import Flask, render_template, request, jsonify
import random
import datetime
import math
import json
import os

app = Flask(__name__)

# Constantes
SIMBOLOS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
N_UNIQUE = 15
N_TOTAL = 20
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Asegurarse de que exista la carpeta data
if not os.path.exists("data"):
    os.makedirs("data")

# Ruta principal
@app.route("/")
def index():
    unique = random.sample(SIMBOLOS, N_UNIQUE)
    repeated = random.choices(unique, k=N_TOTAL - N_UNIQUE)
    sequence = unique + repeated
    random.shuffle(sequence)
    return render_template("index.html", sequence=sequence)

# Guardar los resultados
@app.route("/guardar", methods=["POST"])
def guardar():
    datos = request.get_json()
    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    distancias = []
    for i in range(len(datos["round1"])):
        c1 = datos["round1"][i][1]
        c2 = datos["round2"][i][1]
        distancias.append(math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2))))

    promedio_usuario = round(sum(distancias) / len(distancias), 2)

    # Cargar resultados previos
    ruta = "data/resultados.json"
    historico = []
    if os.path.exists(ruta):
        with open(ruta, "r") as f:
            previos = json.load(f)
            for sesion in previos:
                if "distancia_promedio" in sesion:
                    historico.append(sesion["distancia_promedio"])

    promedio_historico = round(sum(historico) / len(historico), 2) if historico else promedio_usuario

    datos_guardar = {
        "timestamp": now,
        "secuencia": datos["sequence"],
        "round1": datos["round1"],
        "round2": datos["round2"],
        "distancia_promedio": promedio_usuario
    }

    guardar_resultado_json(datos_guardar)

    return jsonify({
        "mensaje": "Guardado exitosamente",
        "promedio_usuario": promedio_usuario,
        "promedio_historico": promedio_historico
    })


# Función auxiliar para guardar resultados
def guardar_resultado_json(data_nuevo):
    ruta = "data/resultados.json"

    if os.path.exists(ruta):
        with open(ruta, "r") as f:
            datos = json.load(f)
    else:
        datos = []

    datos.append(data_nuevo)

    with open(ruta, "w") as f:
        json.dump(datos, f, indent=2)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
