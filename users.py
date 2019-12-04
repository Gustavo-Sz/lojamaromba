from functions import banco_de_dados

class User():

    def __init__(self, nome, email):
        self.nome = nome
        self.email = email

    def mostrar_dados(self):
        a = [self.nome, self.email]
        return a

    def alterar_senha(self, senha_antiga, senha_nova):
        db = banco_de_dados()
        dados = db.buscar_usuario(self.email)
        if senha_antiga == dados[1]:
            db.att_senha(self.email, senha_nova)
            return True
        else:
            return False
