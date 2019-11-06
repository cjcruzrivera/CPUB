import sqlite3

conn = sqlite3.connect('database.db')
print ("Opened database successfully")


sql_create_propietario = """CREATE TABLE IF NOT EXISTS propietario(
                            documento integer PRIMARY KEY,
                            nombre_completo text NOT NULL,
                            telefono text NOT NULL,
                            email email NOT NULL
                        )"""

sql_create_bicicleta = """CREATE TABLE IF NOT EXISTS bicicleta(
                            serial text PRIMARY KEY,
                            modelo text NOT NULL,
                            marca text NOT NULL,
                            color text NOT NULL,
                            doc_propietario integer NOT NULL,
                            FOREIGN KEY (doc_propietario) REFERENCES propietario(documento)

                        )"""

sql_create_antecedentes = """CREATE TABLE IF NOT EXISTS antecedente(
                            id_antecente integer PRIMARY KEY AUTOINCREMENT,
                            serial text NOT NULL,
                            antecedente text NOT NULL,
                            FOREIGN KEY (serial) REFERENCES bicicleta(serial)
                        )"""


conn.execute(sql_create_propietario)
conn.execute(sql_create_bicicleta)
conn.execute(sql_create_antecedentes)
# conn.execute('CREATE TABLE bicicleta (serial TEXT, addr TEXT, city TEXT, pin TEXT)')
# print "Table created successfully";
conn.close()
