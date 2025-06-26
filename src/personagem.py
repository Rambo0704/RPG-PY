import time
import threading
import random

class Personagem:
    def __init__(self, nome, max_vida=100, ataque=20, escudo=0, moedas=100, max_stamina=100):
        self.nome = nome
        self.vida = max_vida
        self.max_vida = max_vida
        self.ataque = ataque
        self.escudo = escudo
        self.moedas = moedas
        self.stamina = max_stamina
        self.max_stamina = max_stamina
        self.recuperando = False

    def esta_vivo(self):
        return self.vida > 0

    def receber_dano(self, dano):
        dano_final = max(dano - self.escudo, 0)
        self.vida -= dano_final
        self.vida = max(self.vida, 0)
        return dano_final

    def atacar(self, alvo):
        if self.stamina >= 10:
            chance_erro = random.random()
            if chance_erro < 0.30:
                print(f"{self.nome} errou o ataque")
                self.stamina -= 10
                return 0
            else:
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
            chance_erro = random.random()
            if chance_erro < 0.50:
                print(f"{self.nome} errou atque critico")
                self.stamina -= 30
                return 0
            else:
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
            print("Iniciando recuperação de stamina por 20 segundos")
            tempo_inicial = time.time()
            while self.stamina < self.max_stamina and (time.time() - tempo_inicial) < 20:
                self.stamina += 1
                self.stamina = min(self.stamina, self.max_stamina)
                time.sleep(1)
            print("Recuperação de stamina encerrada.")
            self.recuperando = False

        threading.Thread(target=processo_recuperacao, daemon=True).start() ##usando o conceito de Thread para que  o processo de recuperaçao de stamina ocorra em segundo plano.

    def mostrar_status(self):
        print(f"\nStatus de {self.nome}:")
        print(f"Vida: {self.vida}")
        print(f"Ataque: {self.ataque}")
        print(f"Escudo: {self.escudo}")
        print(f"Moedas: {self.moedas}")
        print(f"Stamina: {self.stamina}/{self.max_stamina}")

    def aplicar_buff(self, atributo, valor):
        if atributo == "ataque":
            self.ataque += valor
        elif atributo == "escudo":
            self.escudo += valor
        elif atributo == "vida":
            self.vida += valor
        else:
            print(f"Atributo {atributo} não reconhecido.")
        print(f"{self.nome} recebeu +{valor} de {atributo}!")
