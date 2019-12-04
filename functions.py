# FETCHALL RETORNA UMA LISTA DE TUPLAS, QUE SAO AS LINHAS DO DB, MESMO QUE SO HAJA 1 LINHA SELECIONADA. LOGO, PARA ACESSAR OS ELEMENTOS, PRECISA ESPECIFICAR DOIS INDICES (DBLIST[0][1] = NOME DO PRODUTO; ln.179) OU, NO CASO DE HAVER 1 LINHA SO, TORNAR ESSA LISTA UMA TUPLA DESSA LINHA (dblist = dblist[0]) E ENTAO ACESSAR OS ELEMENTOS COM UM UNICO INDICE (dblist[x]; ln.183)

import sqlite3, os, datetime


def arq_promocao(modo):
    return  open("promos.txt", str(modo))


def data_atual():
    i = str(datetime.datetime.now().strftime("%Y"))+str(datetime.datetime.now().strftime("%m"))+str(datetime.datetime.now().strftime("%d"))
    return i


class banco_de_dados():
    def __init__(self):
        pass

    def __conectardb(self):
        return sqlite3.connect("%s\\db.db" % (os.getcwd()))

    def cadastrar_usuario(self, dados):

        db = self.__conectardb()
        cur = db.cursor()
        try:
            cur.execute("INSERT INTO usuarios VALUES (?, ?, ?, ?)", (dados))
            db.commit()
            db.close()
            return True
        except:
            db.close()
            return False

    def buscar_usuario(self, email):

        db = self.__conectardb()
        cur = db.cursor()
        try:
            cur.execute("SELECT nome, senha FROM usuarios where email = '%s'" %(email))
            out = cur.fetchall()
            db.close()
            return out[0]
        except:
            db.close()
            return False

    def add_item(self, codigo, nome, preco, categoria, arq_imagem):


        db = self.__conectardb()
        cur = db.cursor()
        try:
            dataAdd = int(data_atual())
            cur.execute("""INSERT INTO itens values (?,?,?,?,?,?,?)
            """, (codigo, nome, preco, categoria, arq_imagem, dataAdd, None))
            db.commit()
            db.close()
            return True
        except:
            db.close()
            return False

    def del_item(self, codigo):

        db = self.__conectardb()
        cur = db.cursor()

        try:
            cur.execute("""DELETE FROM itens codigo = '%s'""" % (codigo))
            db.commit()
            db.close()
            return True
        except:
            db.close()
            return False

    def att_preco(self, codigo, preco_novo):

        db = self.__conectardb()
        cur = db.cursor()
        try:
            cur.execute("""UPDATE itens
                                SET preco = '%s'
                                WHERE codigo = '%s'
            """ % (preco_novo, codigo))
            db.commit()
            db.close()
            return True
        except:
            db.close()
            return False

    def listar_categoria(self, categoria):

        db = self.__conectardb()
        cur = db.cursor()
        cur.execute("""SELECT * FROM itens where categoria = '%s'
        """ % (categoria))
        itens = cur.fetchall()
        return itens

    def att_senha(self, email, senha_nova):

        db = self.__conectardb()
        cur = db.cursor()
        cur.execute("""UPDATE usuarios
                            SET senha = '%s'
                            WHERE email = '%s'
        """ % (senha, email))
        db.commite()
        db.close()
        return True

    def add_promocao(self, codigo_item, preco_novo):

        db = self.__conectardb()
        cur = db.cursor()

        try:
            cur.execute("""SELECT * FROM itens WHERE codigo = %i""" % (int(codigo_item)))
            item = cur.fetchall()
            preco_antigo = item[0][2]
        except:
            return "Não foi possível buscar as informações no banco de dados"

        if preco_antigo == int(preco_novo):
            return "O produto já está nesse preço"

        db.close()
        self.att_preco(codigo_item, preco_novo)
        arq = arq_promocao("a")
        arq.write("%s:%s\n" % (codigo_item, preco_antigo))
        arq.close()
        return "Promoção adicionada"

    def rem_promocao(self, codigo_item):

        arq = arq_promocao("r")
        itens = arq.readlines()
        arq.close()

        arq = arq_promocao("w")
        for line in itens:
            if line.strip("\n").split(":")[0] != str(codigo_item):
                arq.write(line)
        arq.close()

    def buscar_itens_novos(self):

        i = int(data_atual())-7
        db = self.__conectardb()
        cur = db.cursor()
        cur.execute("""SELECT codigo, nome, preço, imagem
        FROM itens
        WHERE data > %i
        ORDER BY data asc;
        """ % (i))
        itens = cur.fetchall()
        db.close()
        print(itens)
        # itens = [codigo, nome, preco, imagem]
        return itens

    def buscar_promos(self):

        try:
            arq = arq_promocao("r")
            itens = arq.readlines()
        except:
            arq = arq_promocao("w")
        arq.close()
        db = self.__conectardb()
        cur = db.cursor()

        for line in range(len(itens)):
            itens[line] = itens[line].strip("\n").split(":")
            cur.execute("""SELECT nome, preço, imagem FROM itens Where codigo = %i""" % (int(itens[line][0])))
            dblist = cur.fetchall()
            
            dblist = dblist[0]
            for x in dblist:
                itens[line].append(x)
            # [codigo, preco_antigo, nome, preco_novo, imagem]
        
        return itens

    def contar_itens(self,categ):
        db = self.__conectardb()
        cur = db.cursor()
        cur.execute("""SELECT nome FROM itens where categoria = %s"""%(categ))
        dblist = cur.fetchall()
        return len(dblist)


    def cria_codigo(self,categ,qtd_itens):
        dic = {
            'VITAMINAS': 100,
            'WHEYPROTEIN': 200,
            'PROTEINAS': 300,
            'OLEOSESSENCIAIS': 400,
            'HIPERCALORICOS': 500,
            'TERMOGENICOS': 600,
            'PRETREINOS': 700,
        } 
        
        codigo_produto = str(dic[categ]) + str(qtd_itens)
        return int(codigo_produto)






