from src.buff import Buff
from src.loja import Loja
from src.personagem import Personagem
import time

p1 = Personagem("Figado",max_stamina=0)
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

    turno += 1
    time.sleep(1.5)

if p1.esta_vivo():
    print("\nVocê venceu!")
else:
    print("\nVocê perdeu!")

time.sleep(1.5)
print("\n\n\n MOMENTO DE COMPRAS NA LOJA!!")
loja = Loja
loja.mostrar_buffs()
escolha = None
while escolha != 0:
    
    if escolha == 1:
        loja.comprar_buff(1,p1)
    elif escolha == 2:
        loja.comprar_buff(2,p1)
    elif escolha == 3:
        loja.comprar_buff(3,p1)
    elif escolha == 4:
        loja.comprar_buff(4,p1)
    elif escolha == 0:
        print("Saindo da loja...\n")
        time.sleep(1.5)
        p1.mostrar_status()
    else:
        print("Opção Invalida")
