# FETCHALL RETORNA UMA LISTA DE TUPLAS, QUE SAO AS LINHAS DO DB, MESMO QUE SO HAJA 1 LINHA SELECIONADA. LOGO, PARA ACESSAR OS ELEMENTOS, PRECISA ESPECIFICAR DOIS INDICES (DBLIST[0][1] = NOME DO PRODUTO; ln.179) OU, NO CASO DE HAVER 1 LINHA SO, TORNAR ESSA LISTA UMA TUPLA DESSA LINHA (dblist = dblist[0]) E ENTAO ACESSAR OS ELEMENTOS COM UM UNICO INDICE (dblist[x]; ln.183)

import sqlite3, os, datetime, smtplib


def arq_promocao(modo):
    return  open("promos.txt", str(modo))

def arq_descricao(codigo):
    end = str(os.getcwd())+"\\descricoes\\"
    try:
        arq = open(end+str(codigo)+".txt", 'r')
        descricao = arq.readlines()
        descricao = descricao[0].strip("\n")
        return descricao
    except FileNotFoundError:
        return "Arquivo de descrição não encontrado"

def data_atual():
    i = str(datetime.datetime.now().strftime("%Y"))+str(datetime.datetime.now().strftime("%m"))+str(datetime.datetime.now().strftime("%d"))
    return i

def lista_de_categorias():
    dic = {'VITAMINAS': 100,'WHEYPROTEIN': 200,'PROTEINAS': 300,'OLEOSESSENCIAIS': 400,'HIPERCALORICOS': 500,'TERMOGENICOS': 600,'PRETREINOS': 700} 
    return dic

def enviar_email(nome, nome_item, email, resposta):
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login("donotabuser@gmail.com", "hcqvmhwzrpvbiuzk")
    msg = """Ola %s. Aqui esta a resposta para sua duvida sobre nosso produto '%s'.
     %s""" % (nome, nome_item, resposta)
    server.sendmail(
    "donotabuser@gmail.com",
    email,
    msg)
    server.quit()

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

    def add_item(self, codigo, nome, preco, categoria, arq_imagem, descricao):


        db = self.__conectardb()
        cur = db.cursor()
        try:
            dataAdd = int(data_atual())
            cur.execute("""INSERT INTO itens values (?,?,?,?,?,?,?)
            """, (codigo, nome, preco, categoria, arq_imagem, dataAdd, None))
            db.commit()
            db.close()
            arq = open(str(os.getcwd())+"\\descricoes\\%s.txt" % (codigo), 'w')
            arq.write(descricao)
            arq.close()
            return True
        except:
            db.close()
            return "Não foi possível adicionar o item"

    def del_item(self, codigo):

        db = self.__conectardb()
        cur = db.cursor()
        try:
            os.remove(str(os.getcwd())+"\\descricoes\\%s.txt" % (codigo))
            status = ""
        except FileNotFoundError: 
            status = "Arquivo da descrição não encontrado."

        try:
            cur.execute("""DELETE FROM itens WHERE codigo = '%s'""" % (codigo))
            db.commit()
            db.close()
            status = status+" Item removido"
            return status
        except:
            db.close()
            status = status+" Codigo não existe"
            return status

    def att_preco(self, codigo, preco_novo):

        db = self.__conectardb()
        cur = db.cursor()
        try:
            sql = "UPDATE itens SET preco = ? WHERE codigo = ?"
            values = (preco_novo, codigo)
            cur.execute(sql, (preco_novo, codigo))
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
        db.close()
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
        status = self.att_preco(codigo_item, preco_novo) 
        if not status:
            return "Não foi possível alterar o preço"
        else:
            arq = arq_promocao("a")
            arq.write("%s:%s\n" % (codigo_item, preco_antigo))
            arq.close()
            return "Promoção adicionada"

    def rem_promocao(self, codigo_item):

        arq = arq_promocao("r")
        itens = arq.readlines()
        arq.close()
        coditens = []
        for line in itens:
                coditens.append(line.strip("\n").split(":")[0])
        if codigo_item in coditens:
            arq = arq_promocao("w")
            for line in itens:
                if line.strip("\n").split(":")[0] != str(codigo_item):
                    arq.write(line)
            arq.close()
            return "Promoção removida !"
        else:
            return "Não existe promoção para esse código"

    def buscar_itens_novos(self):

        i = int(data_atual())-7
        db = self.__conectardb()
        cur = db.cursor()
        cur.execute("""SELECT codigo, nome, preco, imagem
        FROM itens
        WHERE data > %i
        ORDER BY data asc;
        """ % (i))
        itens = cur.fetchall()
        db.close()
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
            cur.execute("""SELECT nome, preco, imagem FROM itens Where codigo = %i""" % (int(itens[line][0])))
            dblist = cur.fetchall()
            dblist = dblist[0]
            for x in dblist:
                itens[line].append(x)
            # [codigo, preco_antigo, nome, preco_novo, imagem]
        db.close()
        return itens

    def buscar_item(self, codigo):
        db = self.__conectardb()
        cur = db.cursor()
        
        cur.execute("SELECT * FROM itens WHERE codigo = ?", codigo)
        infos = cur.fetchall()
        if infos == []:
            return False
        else:
            infos = [infos[0][0],infos[0][1],infos[0][2],infos[0][3],infos[0][4],infos[0][5],infos[0][6]]
            db.close()
            descricao = arq_descricao(codigo[0])
            infos.append(descricao)
            return infos

    def contar_itens(self, categ):
        db = self.__conectardb()
        cur = db.cursor()
        cur.execute("""SELECT nome FROM itens where categoria = '%s'""" % (categ))
        dblist = cur.fetchall()
        dblist = len(dblist)
        db.close()
        return dblist

    def cria_codigo(self, categ):
        list_cat = lista_de_categorias()
        qtd_itens = self.contar_itens(categ)
        codigo_produto = str(list_cat[categ]) + str(qtd_itens)
        return int(codigo_produto)

    def enviar_duvida(self, codigo, nome, email, duvida):
        db = self.__conectardb()
        cur = db.cursor()
        cur.execute("""
                    SELECT codigo from duvidas WHERE email = (?)
        """, (email,))
        duvidas_anteriores = cur.fetchall()
        for x in range(len(duvidas_anteriores)):
            duvidas_anteriores[x] = duvidas_anteriores[x][0]
        if int(codigo) in duvidas_anteriores:
            return False
        else:
            cur.execute("""INSERT INTO duvidas values (?,?,?,?)""", (codigo, nome, email, duvida))
            db.commit()
            db.close()
            return "Duvida enviada. Aguarde um email de resposta."

    def listar_duvidas(self):
        db = self.__conectardb()
        cur = db.cursor()
        cur.execute("""
                    SELECT * FROM duvidas
        """)
        duvidas = cur.fetchall()
        return duvidas