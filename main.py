import pygame
from src.personagem import Personagem
from Interface.batalha import executar_batalha_visual
from Interface import telas
from src.loja import Loja

FASES = [
    {
        "nome_inimigo": "Cerveja",
        "ataque_inimigo": 15, "defesa_inimigo": 5, "stamina_inimigo": 200,
        "caminhos": {
            "fundo": "Interface/sprites/arena.jpg",
            "inimigo": "Interface/sprites/cerveja.png",
            "musica": "Interface/audio/musica_tema.mp3"
        },
        "mensagem_vitoria": "VOCÊ VENCEU O ALCOOLISMO - NÍVEL 1"
    },
    {
        "nome_inimigo": "Cachaça",
        "ataque_inimigo": 18, "defesa_inimigo": 12, "stamina_inimigo": 200,
        "caminhos": {
            "fundo": "Interface/sprites/arena.jpg",
            "inimigo": "Interface/sprites/cachaca.png",
            "musica": "Interface/audio/musica_tema.mp3"
        },
        "mensagem_vitoria": "VOCÊ VENCEU O ALCOOLISMO - NÍVEL 2"
    },
]

def rodar_jogo():
    pygame.init()
    info = pygame.display.Info()
    screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
    pygame.display.set_caption("RPG")
    clock = pygame.time.Clock()
    
    fontes = {
        'padrao': pygame.font.SysFont("arial", 30),
        'grande': pygame.font.SysFont("arial", 48, bold=True)
    }

    estado_atual = telas.ESTADO_TELA_INICIAL
    nivel_fase_atual = 0

    while True:
        if estado_atual == telas.ESTADO_TELA_INICIAL:
            nivel_fase_atual = 0
            estado_atual = telas.tela_inicial()

        elif estado_atual == telas.ESTADO_EM_BATALHA:
            if nivel_fase_atual >= len(FASES):
                estado_atual = telas.ESTADO_FIM_DE_JOGO
                continue

            fase_data = FASES[nivel_fase_atual]
            jogador = Personagem(nome="Fígado")
            inimigo_atual = Personagem(
                nome=fase_data["nome_inimigo"],
                ataque=fase_data["ataque_inimigo"], escudo=fase_data["defesa_inimigo"], max_stamina=fase_data["stamina_inimigo"]
            )
            resultado = executar_batalha_visual(jogador, inimigo_atual, fase_data["caminhos"])
            if resultado == "derrota" or resultado == "fugiu":
                estado_atual = telas.ESTADO_FIM_DE_JOGO
            elif resultado == "vitoria":
                loja = Loja()
                retorno_loja = telas.executar_loja(loja, jogador)
                if retorno_loja == "proxima_fase":
                    nivel_fase_atual += 1
                    if nivel_fase_atual >= len(FASES):
                        estado_atual = telas.ESTADO_FIM_DE_JOGO
                    else:
                        estado_atual = telas.ESTADO_EM_BATALHA

        elif estado_atual == telas.ESTADO_FIM_DE_JOGO:
            estado_atual = telas.tela_fim_de_jogo(screen, clock, fontes)

if __name__ == '__main__':
    rodar_jogo()
