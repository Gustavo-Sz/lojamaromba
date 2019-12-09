import os, sqlite3

codigo = input('codigo')
try:
    os.remove(str(os.getcwd())+"\\descricoes\\%s.txt" % (codigo))
except FileNotFoundError:
    print("Nao existe")
