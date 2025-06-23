
class Buff:
    def __init__(self, nome, atributo, valor, preco, descricao):
        self.nome = nome
        self.atributo = atributo
        self.valor = valor
        self.preco = preco
        self.descricao = descricao

    def aplicar(self, Personagem):
        Personagem.aplicar_buff(self.atributo, self.valor)
        print(f"{Personagem.nome} aplicou o buff '{self.nome}'!")
