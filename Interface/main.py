
from src.loja import Loja
from src.personagem import Personagem
import time

p1 = Personagem("Figado")
bot = Personagem("Cerveja", vida=50, ataque=10)
turno = 0

while p1.esta_vivo() and bot.esta_vivo():
    print(f"\nTurno: {turno}\n{p1.nome if turno % 2 == 0 else bot.nome} sua vez!")

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
            esquivando = False
        elif escolha == "2":
            dano = p1.critico(bot)
            print(f"Você causou {dano} de dano crítico ao {bot.nome}!")
            esquivando = False
        elif escolha == "3":
            esquivando = p1.esquivar()  
            if esquivando:
                print(f"{p1.nome} está preparado para esquivar do próximo ataque!")
            else:
                print("Sem stamina suficiente para esquivar!")
        else:
            print("Ação inválida.")
            esquivando = False

    else:
        if esquivando:
            print(f"{p1.nome} esquivou e evitou o ataque do {bot.nome}!")
            esquivando = False  
        elif bot.stamina >= 10:
            dano = bot.atacar(p1)
            print(f"O {bot.nome} causou {dano} de dano em você!")
        else:
            print(f"O {bot.nome} está sem stamina e tenta recuperar.")
            bot.recuperar_stamina()
        p1.recuperar_stamina()
    turno += 1
    time.sleep(1.5)

if p1.esta_vivo():
    print("\nVocê venceu!")
else:
    print("\nVocê perdeu!")

time.sleep(1.5)
loja = Loja()
while True:
    print("\n\n\nMOMENTO DE COMPRAS NA LOJA!!")
    print(f"\nSuas Moedas: {p1.moedas}\n")
    loja.mostrar_buffs()

    try:
        escolha = int(input("Qual buff você deseja? "))
    except ValueError:
        print("Por favor, digite um número válido.")
        continue

    if escolha == 0:
        print("Saindo da loja...\n")
        p1.mostrar_status()
        break
    else:
        loja.comprar_buff(escolha, p1)