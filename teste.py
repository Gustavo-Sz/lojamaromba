import sqlite3, os

codigo_item =int(input("Digite o codigo do item"))

db = sqlite3.connect("%s\\db.db" % (os.getcwd()))

cur = db.cursor()

cur.execute("""SELECT * FROM itens WHERE codigo = %i""" %(codigo_item))

item = cur.fetchall()

print(item)
