class Produto:
    def __init__(self, codigo, nome, preco, categoria, imagem):
        self.codigo = codigo
        self.nome = nome
        self.categoria = categoria
        self.preco = preco
        self.categoria = categoria
        self.imagem = imagem

    def get_nome(self):
        return self.nome

    def get_codigo(self):
        return self.categoria

    def get_lotacao(self):
        return self.preco