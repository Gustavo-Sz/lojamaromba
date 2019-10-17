import sqlite3, os
db = sqlite3.connect(r"{}\db.db".format(os.getcwd()))
cursor = db.cursor()
cursor.execute(sqlite_insert )