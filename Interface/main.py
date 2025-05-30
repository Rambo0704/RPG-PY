import sys
import os
sys.path.append(os.path.abspath('..'))
from src.buff import Buff
from src.loja import Loja
from src.personagem import Personagem
import time
p1 = Personagem("Figado")
bot = Personagem("Cerveja", vida=50, ataque=10)
turno = 0

while p1.esta_vivo() and bot.esta_vivo():
    print(f"Turno: {turno}\n{p1.nome if turno % 2 == 0 else bot.nome} sua vez!")

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
time.sleep(1.5)
print("\n\n\n MOMENTO DE COMPRAS NA LOJA!!")