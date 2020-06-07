import mysql.connector


db = mysql.connector.connect(
    host="localhost",
    port="3307",
    user="admin",
    passwd="@L0j4M4r0mb4",
    auth_plugin="mysql_native_password",
    database="lojadb"
)

cur = db.cursor()

codigo = "1004"
nome = "gustavo"
email="gustavo997108@gmail.com"
duvida="Teste index"
try:
    cur.execute("""INSERT INTO duvidas (codigo, nome, email, duvida) values ('%s','%s','%s','%s')""" % (codigo, nome, email, duvida))
except mysql.connector.errors.IntegrityError:
    print("ja ")
db.commit()
db.close()