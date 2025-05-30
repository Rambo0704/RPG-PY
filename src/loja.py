from buff import Buff

class Loja:
    def __init__(self):
        self.buffs = [
            Buff("Buff de Ataque", "ataque", 5, 50, "Aumenta o ataque em 5 pontos."),
            Buff("Buff de Escudo", "escudo", 5, 50, "Aumenta o escudo em 5 pontos."),
            Buff("Buff de Vida", "vida", 20, 30, "Recupera 20 de vida."),
            Buff("Buff de Stamina", "stamina", 30, 20, "Recupera 30 de stamina."),
        ]

    def mostrar_buffs(self):
        print("\n------ Loja de Buffs ------")
        for idx, buff in enumerate(self.buffs, start=1):
            print(f"{idx} - {buff.nome} | {buff.descricao} | Preço: {buff.preco} moedas")
        print("0 - Sair da loja")

    def comprar_buff(self, escolha, personagem):
        if escolha == 0:
            print("Saindo da loja...")
            return False

        if escolha < 1 or escolha > len(self.buffs):
            print("Escolha inválida.")
            return True

        buff = self.buffs[escolha - 1]

        if personagem.moedas >= buff.preco:
            personagem.moedas -= buff.preco
            buff.aplicar(personagem)
            print(f"Você comprou '{buff.nome}'!")
        else:
            print("Moedas insuficientes para comprar este buff.")

        return True
