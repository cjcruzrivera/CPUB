import sqlite3
import sys
from faker import Faker
conn = sqlite3.connect('database.db')
print ("Opened database successfully")


conn.execute(sql_create_propietario)
conn.execute(sql_create_bicicleta)
conn.execute(sql_create_antecedentes)
print("CREATED TABLES")
# conn.execute('CREATE TABLE bicicleta (serial TEXT, addr TEXT, city TEXT, pin TEXT)')
# print "Table created successfully";
conn.close()
