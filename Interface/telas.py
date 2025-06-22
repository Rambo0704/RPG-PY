import pygame
import sys
from . import ui
from src import utils

ESTADO_TELA_INICIAL = "TELA_INICIAL"
ESTADO_EM_BATALHA = "EM_BATALHA"
ESTADO_FIM_DE_JOGO = "FIM_DE_JOGO"

def tela_inicial(screen, clock, fontes):
    utils.iniciar_musica("Interface/audio/figado_valente.mp3")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if botao_iniciar.collidepoint(event.pos):
                    pygame.mixer.music.fadeout(500)
                    return ESTADO_EM_BATALHA
                if botao_sair.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        screen.fill((0, 10, 25))
        ui.draw_text(screen, "FIGADO'S ADVENTURE", screen.get_width() // 2, screen.get_height() * 0.2, fontes['grande'], center=True)
        
        largura_botao, altura_botao = 250, 60
        x_botoes = screen.get_width() // 2 - largura_botao // 2
        y_botao_iniciar = screen.get_height() // 2 - altura_botao
        y_botao_sair = screen.get_height() // 2 + 20

        botao_iniciar = ui.desenhar_botao(screen, "Iniciar Jogo", x_botoes, y_botao_iniciar, largura_botao, altura_botao, fontes['padrao'])
        botao_sair = ui.desenhar_botao(screen, "Sair", x_botoes, y_botao_sair, largura_botao, altura_botao, fontes['padrao'])

        pygame.display.flip()
        clock.tick(60)


def tela_fim_de_jogo(screen, clock, fontes):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if botao_menu.collidepoint(event.pos):
                    return ESTADO_TELA_INICIAL

        screen.fill((50, 0, 0))
        ui.draw_text(screen, "FIM DE JOGO", screen.get_width() // 2, screen.get_height() * 0.4, fontes['grande'], center=True)

        largura_botao, altura_botao = 300, 60
        x_botoes = screen.get_width() // 2 - largura_botao // 2
        y_botoes = screen.get_height() // 2

        botao_menu = ui.desenhar_botao(screen, "Voltar ao Menu", x_botoes, y_botoes, largura_botao, altura_botao, fontes['padrao'])

        pygame.display.flip()
        clock.tick(60)