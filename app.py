from flask import Flask, abort, request, render_template, redirect
import sqlite3 as sql 
import json

app = Flask(__name__)

@app.route('/ws/registro', methods=["POST"])
def wsRegistro():
    data = request.form
    serial = data["serial"]
    marca = data["marca"]
    modelo = data["modelo"]
    color = data["color"]
    nombre = data["nombre"]
    documento = data["documento"]
    telefono = data["telefono"]
    email = data["email"]

    conn = sql.connect("database.db")
    c = conn.cursor()
    try:
        select_prop = "SELECT * FROM propietario WHERE documento = {}".format(documento)
        c.execute(select_prop)
        records = c.fetchall()
        if len(records) == 0:
            c.execute("INSERT INTO propietario VALUES ('{}', '{}', '{}', '{}')".format(documento, nombre, telefono, email))
            print("SE GUARDA")
        else:
            print("PROPIETARIO YA GUARDADO")
        
        c.execute("INSERT INTO bicicleta VALUES('{}', '{}', '{}', '{}', '{}')".format(serial, marca, modelo, color, documento))
        c.close
        type_response = "success"
        title = "Exito"
        mensaje = "La bicicleta con serial {} ha sido registrada correctamente".format(serial)
        conn.commit()
    except sql.IntegrityError as identifier:
            type_response = "error"
            title = "Error"
            mensaje = "La bicicleta con serial {} ya habia sido registrada anteriormente".format(serial)
            pass
    if conn:
        conn.close

    response = {
        "type": type_response,
        "title": title,
        "mensaje": mensaje,
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

@app.route('/detalle/<pk>', methods=["GET"])
def detalle(pk):
    bicicleta = {
    }
    return render_template("detalle.html", bicicleta=bicicleta)

if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0')