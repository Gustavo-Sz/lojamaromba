import sqlite3, os
email = "slasla"
senha = "123456"

db = sqlite3.connect(r"{}\db.db".format(os.getcwd()))
cursor = db.cursor()
cursor.execute("""SELECT senha FROM usuarios WHERE email = '{}'""".format(email))
senhadb = cursor.fetchall()
db.close()

if senhadb:
    print("e true")
else: 
    print("e false")
print(senhadb)

if senha in senhadb:
    print("senha igual")