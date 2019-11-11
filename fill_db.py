import sqlite3
import sys
from faker import Faker
from random import randint
conn = sqlite3.connect('database.db')
c = conn.cursor()
print ("Opened database successfully")
fake = Faker()

marcas = ["GW",
                "SHIMANO",
                "ROCKSHOCK",
                "BOSTON",
                "OPTIMUS",
                "TREK",
                "GRAVITY"]
colores = ["AZUL", "ROJO", "VERDE", "NEGRO", "BLANCO", "AMARILLO", "MORADO", "GRIS"]
modelos = ["MTB", "RUTA", "CIUDAD", "PLAYERA", "URBANA"]
propietarios = []
for i in range(1,101):
    documento = fake.msisdn()
    nombre = fake.name()
    telefono = fake.msisdn()
    email = fake.email()
    propietarios.insert(0,documento)
    insert_prop = "INSERT INTO propietario VALUES ('{}', '{}', '{}', '{}')".format(documento, nombre, telefono, email)
    print("insert_prop")
    c.execute(insert_prop)

for i in range(1,201):
    serial = fake.isbn10(separator='-')
    marca = marcas[randint(0,(len(marcas)-1))]
    modelo = modelos[randint(0,(len(modelos)-1))]
    color = colores[randint(0,(len(colores)-1))]
    propietario = propietarios[randint(0,(len(propietarios)-1))]
    insert_bici = "INSERT INTO bicicleta VALUES ('{}', '{}', '{}', '{}', '{}')".format(serial, marca, modelo, color, propietario)
    c.execute(insert_bici)
    print("insert_bici")

    if randint(0,1):
        if randint(0,1):
            if randint(0,1):
                antecedente = "Se denuncia su hurto el dia " + fake.date()
                numeroSPOA = "Número de SPOA: {}".format(randint(500016000727200000000,540016000727201800006))
                fiscalia = "Fiscalía: URI Paloquemao."
                insert_ant = "INSERT INTO antecedente(serial, antecedente) VALUES('{}', '{}'), ('{}', '{}'), ('{}', '{}')".format(serial, fiscalia, serial, numeroSPOA, serial, antecedente)
                c.execute(insert_ant)
                print("insert_ant")
c.close()
conn.commit()
conn.close()
