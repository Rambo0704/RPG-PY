class Personagem:
    def __init__(self, nome, vida=100, ataque=10, defesa=0, moedas=100, stamina=100):
        self.nome = nome
        self.vida = vida
        self.ataque = ataque
        self.defesa = defesa
        self.moedas = moedas
        self.stamina = stamina
        self.inventario = []
    def esta_vivo(self): #verificar se o personagem esta apto para o uso
        return self.vida > 0 
    def receber_dano(self,dano):
        dano_final = max(dano - self.defesa,0)
        self.vida -= dano_final
        self.vida = max(self.vida,0) #manter no minimo 0
        return dano_final
    def atacar(self,alvo):
        dano = self.ataque
        dano_causado = alvo.receber_dano(dano)
        return dano_causado
    def esquivar(self):
        if self.stamina >= 20:
            self.stamina -= 20
            print(f"{self.nome} esquivou (-20 de stamina)")
            return True
        else:
            print(f"{self.nome} stamina insuficiente")
            return False
    def mostrar_status(self): ##verificação
        print(f"\nStatus de {self.nome}:")
        print(f"Vida: {self.vida}")
        print(f"Ataque: {self.ataque}")
        print(f"Defesa: {self.defesa}")
        print(f"Moedas: {self.moedas}")
        print(f"Stamina: {self.stamina}")

