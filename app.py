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

@app.route('/ws/consulta', methods=["POST"])
def consultar():
    data = request.form
    serial = data["serial"]
    registra = True
    conn = sql.connect("database.db")
    c = conn.cursor()
    select_bici = "SELECT bici.serial, bici.marca, bici.modelo, bici.color, prop.documento, prop.nombre_completo, prop.telefono, prop.email FROM bicicleta as bici INNER JOIN propietario as prop ON bici.doc_propietario = prop.documento WHERE bici.serial = {}".format(serial)
    c.execute(select_bici)
    records = c.fetchone()
    if records == None:
        bicicleta = {}
        registra = False
    else:
        antecedentes = []
        bicicleta = {
        "serial": records[0],
        "marca": records[1],
        "modelo": records[2],
        "color": records[3],
        "documento": records[4],
        "nombre": records[5],
        "telefono": records[6],
        "email": records[7],
        }
        select_antecendentes = "SELECT antecedente FROM antecedente WHERE serial = {}".format(serial)
        c.execute(select_antecendentes)
        records = c.fetchall()
        for record in records:
            antecedentes.insert(0, record[0])
        bicicleta["antecedentes"] = antecedentes

    response = {
        "registra": registra,
        "bicicleta": bicicleta
    }
    return json.dumps(response)

@app.route('/listado', methods=["GET"])
def listado():
    bicicletas = []
    conn = sql.connect("database.db")
    c = conn.cursor()
    select_bicis = "SELECT bici.serial, bici.marca, bici.modelo, bici.color, prop.documento, prop.nombre_completo, prop.telefono, prop.email FROM bicicleta as bici INNER JOIN propietario as prop ON bici.doc_propietario = prop.documento"
    c.execute(select_bicis)
    records = c.fetchall()
    for record in records:
        antecedentes=[]
        bicicleta = {
            "serial": record[0],
            "marca": record[1],
            "modelo": record[2],
            "color": record[3],
            "documento": record[4],
            "nombre": record[5],
            "telefono": record[6],
            "email": record[7],
        }
        select_antecendentes = "SELECT antecedente FROM antecedente WHERE serial = {}".format(record[0])
        c.execute(select_antecendentes)
        records = c.fetchall()
        for antecendente in records:
            antecedentes.insert(0, antecendente[0])
        bicicleta["antecedentes"] = antecedentes

        bicicletas.insert(0,bicicleta)
        print(bicicletas)
    
    return render_template("listado.html", bicicletas= bicicletas)

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
    conn = sql.connect("database.db")
    c = conn.cursor()
    select_bici = "SELECT bici.serial, bici.marca, bici.modelo, bici.color, prop.documento, prop.nombre_completo, prop.telefono, prop.email FROM bicicleta as bici INNER JOIN propietario as prop ON bici.doc_propietario = prop.documento WHERE bici.serial = {}".format(pk)
    c.execute(select_bici)
    records = c.fetchone()
    antecedentes = []

    bicicleta = {
        "serial": records[0],
        "marca": records[1],
        "modelo": records[2],
        "color": records[3],
        "documento": records[4],
        "nombre": records[5],
        "telefono": records[6],
        "email": records[7],
    }

    select_antecendentes = "SELECT antecedente FROM antecedente WHERE serial = {}".format(pk)
    c.execute(select_antecendentes)
    records = c.fetchall()
    for record in records:
        antecedentes.insert(0, record[0])
    bicicleta["antecedentes"] = antecedentes
    print(bicicleta)
    return render_template("detalle.html", bicicleta=bicicleta)

if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0')