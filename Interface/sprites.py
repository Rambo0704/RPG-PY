import pygame
from . import ui # Importação relativa do nosso módulo de UI

def carregar_recursos_batalha(largura_tela, altura_tela, caminho_fundo, caminho_sprite_inimigo):
    recursos = {}
 
    fundo_img = pygame.image.load(caminho_fundo).convert()
    recursos['fundo'] = pygame.transform.scale(fundo_img, (largura_tela, altura_tela))
    jogador_img = pygame.image.load("Interface/sprites/figado_transparente.png").convert_alpha()
    recursos['jogador'] = pygame.transform.scale(jogador_img, (300, 500))
    inimigo_img = pygame.image.load(caminho_sprite_inimigo).convert_alpha()
    recursos['inimigo'] = pygame.transform.scale(inimigo_img, (300, 500))
    
    return recursos

def animar_acao(screen, clock, recursos, personagens, posicoes, mensagem, lado, tipo, fontes):
    deslocamento = 60 if tipo == "ataque" else -40
    passos = 15
    jogador, inimigo = personagens['jogador'], personagens['inimigo']
    sprite_jogador, sprite_inimigo = recursos['jogador'], recursos['inimigo']
    fundo = recursos['fundo']
    
    JOGADOR_X_BASE, INIMIGO_X_BASE, PERSONAGEM_Y = posicoes['jogador_x'], posicoes['inimigo_x'], posicoes['personagem_y']
    
    font_nome, font_grande = fontes['nome'], fontes['grande']

    for i in range(passos * 2):
        progresso = i if i < passos else (passos * 2) - i
        offset = int(deslocamento * (progresso / passos))
        
        x_jogador_anim = JOGADOR_X_BASE + (offset if lado == "jogador" else 0)
        x_inimigo_anim = INIMIGO_X_BASE - (offset if lado == "inimigo" else 0)
        screen.blit(fundo, (0, 0))
        screen.blit(sprite_jogador, (x_jogador_anim, PERSONAGEM_Y))
        screen.blit(sprite_inimigo, (x_inimigo_anim, PERSONAGEM_Y))

        # HUD do Jogador
        hud_jog_x = x_jogador_anim + sprite_jogador.get_width() // 2
        hud_jog_y = PERSONAGEM_Y - 100
        ui.draw_text(screen, f"{jogador.nome}", hud_jog_x, hud_jog_y, font_nome, center=True)
        ui.draw_bar(screen, hud_jog_x - ui.LARGURA_BARRA_HUD // 2, hud_jog_y + 30, jogador.max_vida, jogador.vida, ui.RED)
        ui.draw_bar(screen, hud_jog_x - ui.LARGURA_BARRA_HUD // 2, hud_jog_y + 65, jogador.max_stamina, jogador.stamina, ui.BLUE)

        # HUD do Inimigo
        inimigo_nome_x = x_inimigo_anim + sprite_inimigo.get_width() // 2
        inimigo_nome_y = PERSONAGEM_Y - 100
        ui.draw_text(screen, f"{inimigo.nome}", inimigo_nome_x, inimigo_nome_y, font_nome, center=True)
        ui.draw_bar(screen, inimigo_nome_x - ui.LARGURA_BARRA_HUD // 2, inimigo_nome_y + 30, inimigo.max_vida, inimigo.vida, ui.RED)

        # Mensagem de ação
        ui.draw_text(screen, mensagem, screen.get_width() // 2, screen.get_height() // 4, font_grande, center=True)
        
        pygame.display.flip()
        clock.tick(60)