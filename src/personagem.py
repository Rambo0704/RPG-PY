import time
import threading
class Personagem:
    def __init__(self, nome, vida=100, ataque=20, defesa=0, moedas=100, max_stamina=100):
        self.nome = nome
        self.vida = vida
        self.ataque = ataque
        self.defesa = defesa
        self.moedas = moedas
        self.stamina = max_stamina
        self.max_stamina = max_stamina
        self.recuperando = False  # Flag para controle da thread

    def esta_vivo(self):
        return self.vida > 0

    def receber_dano(self, dano):
        dano_final = max(dano - self.defesa, 0)
        self.vida -= dano_final
        self.vida = max(self.vida, 0)
        return dano_final

    def atacar(self, alvo):
        if self.stamina >= 10:
            dano = self.ataque
            dano_causado = alvo.receber_dano(dano)
            self.stamina -= 10
            print("Ataque realizado (-10 stamina)")
            return dano_causado
        else:
            print("Stamina insuficiente para atacar")
            return 0

    def critico(self, alvo):
        if self.stamina >= 30:
            critico = self.ataque * 2
            critico_causado = alvo.receber_dano(critico)
            self.stamina -= 30
            print("Ataque crítico realizado (-30 stamina)")
            return critico_causado
        else:
            print("Stamina insuficiente para ataque crítico")
            return 0

    def esquivar(self):
        if self.stamina >= 20:
            self.stamina -= 20
            print(f"{self.nome} esquivou (-20 de stamina)")
            return True
        else:
            print(f"{self.nome} stamina insuficiente para esquivar")
            return False

    def recuperar_stamina(self):
        if self.recuperando:
            print("Já está recuperando stamina.")
            return

        def processo_recuperacao():
            self.recuperando = True
            print("Iniciando recuperação de stamina...")
            while self.stamina < self.max_stamina:
                self.stamina += 1
                time.sleep(1)
            print("Stamina cheia!")
            self.recuperando = False

        threading.Thread(target=processo_recuperacao, daemon=True).start() ##usando o conceito de Thread para que  o processo de recuperaçao de stamina ocorra em segundo plano.

    def mostrar_status(self):
        print(f"\nStatus de {self.nome}:")
        print(f"Vida: {self.vida}")
        print(f"Ataque: {self.ataque}")
        print(f"Escudo: {self.defesa}")
        print(f"Moedas: {self.moedas}")
        print(f"Stamina: {self.stamina}/{self.max_stamina}")
def teste():
    p1 = Personagem("Fígado")
    bot = Personagem("Cerveja",vida=50,ataque=10)
    turno = 0
    while p1.esta_vivo() and bot.esta_vivo():
        print(f"Turno: {turno}\n{p1.nome if turno%2 == 0 else bot.nome} sua vez!")
        if turno % 2 == 0:
            p1.mostrar_status()
            print("Escolha uma ação:")
            print("1 - Atacar (-10 stamina)")
            print("2 - Ataque crítico (-30 stamina)")
            print("3 - Esquivar (-20 stamina)")
            

            escolha = input("Digite o número da ação: ")   
            if escolha == "1":
                dano = p1.atacar(bot)
                print(f"Você causou {dano} de dano ao {bot.nome}!")
            elif escolha == "2":
                dano = p1.critico(bot)
                print(f"Você causou {dano} de dano crítico ao {bot.nome}!")
            elif escolha == "3":
                p1.esquivar()
            else:
                print("Ação inválida.")

        else:
            print("\nTurno do bot!")
            if escolha == 3:
                print(f"{p1.nome} esquivou e evitou o ataque do {bot.nome}!")
            elif bot.stamina >= 10:
                dano = bot.atacar(p1)
                print(f"O {bot.nome} causou {dano} de dano em você!")
            else:
                print(f"O {bot.nome} está sem stamina e tenta recuperar.")
                bot.recuperar_stamina()

        turno += 1
        time.sleep(1.5) 

    if p1.esta_vivo():
        print("\nVocê venceu!")
    else:
        print("\nVocê perdeu!")     
teste()