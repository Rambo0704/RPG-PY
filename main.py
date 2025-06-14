from src.personagem import Personagem
from Interface.batalha import executar_batalha_visual

jogador = Personagem("Figado")
inimigo = Personagem("Alcool", ataque=15, escudo=3, vida=80)

resultado = executar_batalha_visual(jogador, inimigo)
print("Resultado da batalha:", resultado)
