from functions import banco_de_dados

class User():

    def __init__(self, nome, email):
        self.nome = nome
        self.email = email

    def mostrar_dados(self):
        a = [self.nome, self.email]
        return a

    