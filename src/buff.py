from personagem import Personagem
class Buff:
    def __init__(self, nome, atributo, valor, preco, descricao):
        self.nome = nome
        self.atributo = atributo
        self.valor = valor
        self.preco = preco
        self.descricao = descricao

    def aplicar(self, personagem):
        personagem.aplicar_buff(self.atributo, self.valor)
        print(f"{personagem.nome} aplicou o buff '{self.nome}'!")
