import pygame
from src.personagem import Personagem
from Interface.batalha import executar_batalha_visual
from Interface import telas
from src.loja import Loja

FASES = [
    {
        "nome_inimigo": "Cerveja",
        "ataque_inimigo": 18, "defesa_inimigo": 2, "stamina_inimigo": 200,
        "caminhos": {
            "fundo": "Interface/sprites/arena.jpg",
            "inimigo": "Interface/sprites/cerveja.png",
            "musica": "Interface/audio/musica_tema.mp3"
        },
    },
    {
        "nome_inimigo": "Cachaça",
        "ataque_inimigo": 20, "defesa_inimigo": 4, "stamina_inimigo": 200,
        "caminhos": {
            "fundo": "Interface/sprites/arena.jpg",
            "inimigo": "Interface/sprites/cachaca.png",
            "musica": "Interface/audio/musica_tema.mp3"
        },
    },
    {
        "nome_inimigo": "Absinto",
        "ataque_inimigo": 24, "defesa_inimigo": 6, "stamina_inimigo": 200,
        "caminhos": {
            "fundo": "Interface/sprites/arena.jpg",
            "inimigo": "Interface/sprites/absinto.png",
            "musica": "Interface/audio/musica_tema.mp3"
        },
    },
]

def rodar_jogo():
    pygame.init()
    pygame.display.set_caption("RPG")

    estado_atual = telas.ESTADO_TELA_INICIAL
    nivel_fase_atual = 0
    jogador = Personagem(nome="Fígado",ataque=180)

    while True:
        if estado_atual == telas.ESTADO_TELA_INICIAL:
            nivel_fase_atual = 0
            jogador = Personagem(nome="Fígado",ataque=180)
            estado_atual = telas.tela_inicial()

        elif estado_atual == telas.ESTADO_EM_BATALHA:
            if nivel_fase_atual >= len(FASES):
                estado_atual = telas.ESTADO_FIM_DE_JOGO
                continue

            fase_data = FASES[nivel_fase_atual]
            inimigo_atual = Personagem(
                nome=fase_data["nome_inimigo"],
                ataque=fase_data["ataque_inimigo"],
                escudo=fase_data["defesa_inimigo"],
                max_stamina=fase_data["stamina_inimigo"]
            )
            resultado = executar_batalha_visual(jogador, inimigo_atual, fase_data["caminhos"])

            if resultado == "derrota" or resultado == "fugiu":
                estado_atual = telas.ESTADO_FIM_DE_JOGO
            elif resultado == "vitoria":
                if nivel_fase_atual < len(FASES) - 1:
                    loja = Loja()
                    retorno_loja = telas.executar_loja(loja, jogador)
                    if retorno_loja == "proxima_fase":
                        nivel_fase_atual += 1
                        estado_atual = telas.ESTADO_EM_BATALHA
                else:
                    estado_atual = telas.ESTADO_FIM_DE_JOGO

        elif estado_atual == telas.ESTADO_FIM_DE_JOGO:
            estado_atual = telas.tela_fim_de_jogo()

if __name__ == '__main__':
    rodar_jogo()
