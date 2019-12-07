import os, sqlite3

db = sqlite3.connect("%s\\db.db" % (os.getcwd()))

cur = db.cursor()
value = input('Digite um codigo q n existe:')
value = (str(value),)
cur.execute("SELECT * FROM itens WHERE codigo = ?", value)
saida = cur.fetchall()
print(saida)

if(saida == []):
    print('Vazia')
if(saida != []):
    print("Nao vazia")
