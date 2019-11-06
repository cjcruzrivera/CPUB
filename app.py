from flask import Flask, abort, request, render_template, redirect
import sqlite3 as sql 
import json

app = Flask(__name__)

@app.route('/ws/registro', methods=["POST"])
def wsRegistro():
    print(request.form)
    data = request.form
    serial = data["serial"]
    response = {
        "type": "success",
        "title": "Exito",
        "mensaje": "La bicicleta con serial {} ha sido registrada correctamente".format(serial),
    }
    return json.dumps(response)

@app.route('/inicio',methods=['GET'])
@app.route('/',methods=['GET'])
def index():
    return render_template("inicio.html")

@app.route('/registro',methods=['GET'])
def registro():
    if request.method == "GET":
        return render_template("registro.html")

@app.route('/consulta',methods=['GET'])
def consulta():
    return render_template("consulta.html")


if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0')