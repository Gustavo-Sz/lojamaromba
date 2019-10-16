class Produto:
    def __init__(self, nome, categoria, preco):
        self.nome = nome
        self.categoria = categoria
        self.preco = preco

    def get_nome(self):
        return self.nome

    def get_codigo(self):
        return self.categoria

    def get_lotacao(self):
        return self.preco