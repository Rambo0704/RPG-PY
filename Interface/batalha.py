import pygame
import threading
from src.personagem import Personagem
import random
from Interface import ui, sprites
from src import utils

def executar_batalha_visual(jogador, inimigo, caminhos_recursos, mensagem_vitoria):
    semaforo_jogador = threading.Semaphore(1)
    semaforo_inimigo = threading.Semaphore(0)

    caminho_musica_fase = caminhos_recursos.get('musica')

    thread_musica = threading.Thread(
        target=utils.iniciar_musica,
        args=(caminho_musica_fase,) 
    )
    thread_musica.daemon = True
    thread_musica.start()

    pygame.init()
    info = pygame.display.Info()
    largura_tela, altura_tela = info.current_w, info.current_h
    screen = pygame.display.set_mode((largura_tela, altura_tela), pygame.FULLSCREEN)
    pygame.display.set_caption("Combate RPG")
    
    fontes = {
        'padrao': pygame.font.SysFont("arial", 30),
        'nome': pygame.font.SysFont("arial", 36, bold=True),
        'grande': pygame.font.SysFont("arial", 48, bold=True)
    }
    clock = pygame.time.Clock()

    recursos = sprites.carregar_recursos_batalha(
        largura_tela, altura_tela,
        caminhos_recursos['fundo'],
        caminhos_recursos['inimigo']
    )
    fundo = recursos['fundo']
    sprite_jogador = recursos['jogador']
    sprite_inimigo = recursos['inimigo']
    
    # Organiza dados em dicionários para passar para outras funções
    posicoes = {
        'jogador_x': int(largura_tela * 0.15),
        'inimigo_x': largura_tela - sprite_inimigo.get_width() - int(largura_tela * 0.15),
        'personagem_y': altura_tela - sprite_jogador.get_height() + 40
    }
    JOGADOR_X_BASE, INIMIGO_X_BASE, PERSONAGEM_Y = posicoes['jogador_x'], posicoes['inimigo_x'], posicoes['personagem_y']

    personagens = {'jogador': jogador, 'inimigo': inimigo}
    
    # Variáveis de estado da batalha
    mensagem = "O combate começou!"
    turno_jogador = True
    running = True
    aguardando_acao_inimigo = False
    tempo_acao_inimigo = 0
    esquivou = False
    recuperou_stamina = False
    semaforo_jogador.release()

    while running:

        screen.blit(fundo, (0, 0))
        screen.blit(sprite_jogador, (JOGADOR_X_BASE, PERSONAGEM_Y))
        screen.blit(sprite_inimigo, (INIMIGO_X_BASE, PERSONAGEM_Y))

   
        hud_jog_x = JOGADOR_X_BASE + sprite_jogador.get_width() // 2
        hud_jog_y = PERSONAGEM_Y - 100
        ui.draw_text(screen, f"{jogador.nome}", hud_jog_x, hud_jog_y, fontes['nome'], center=True)
        ui.draw_bar(screen, hud_jog_x - ui.LARGURA_BARRA_HUD // 2, hud_jog_y + 30, jogador.max_vida, jogador.vida, ui.RED)
        ui.draw_bar(screen, hud_jog_x - ui.LARGURA_BARRA_HUD // 2, hud_jog_y + 65, jogador.max_stamina, jogador.stamina, ui.BLUE)

        # HUD do Inimigo
        inimigo_nome_x = INIMIGO_X_BASE + sprite_inimigo.get_width() // 2
        inimigo_nome_y = PERSONAGEM_Y - 100
        ui.draw_text(screen, f"{inimigo.nome}", inimigo_nome_x, inimigo_nome_y, fontes['nome'], center=True)
        ui.draw_bar(screen, inimigo_nome_x - ui.LARGURA_BARRA_HUD // 2, inimigo_nome_y + 30, inimigo.max_vida, inimigo.vida, ui.RED)
        

        ui.draw_text(screen, mensagem, largura_tela // 2, altura_tela // 4, fontes['grande'], center=True)

        if turno_jogador:
            LARGURA_BOTAO, ALTURA_BOTAO, ESPACO = 200, 55, 15
            x_botoes = JOGADOR_X_BASE - LARGURA_BOTAO - 40
            y_base = altura_tela // 2 - (2 * (ALTURA_BOTAO + ESPACO)) + 100

            botao_atacar = ui.desenhar_botao(screen, "Atacar", x_botoes, y_base, LARGURA_BOTAO, ALTURA_BOTAO, fontes['padrao'])
            botao_critico = ui.desenhar_botao(screen, "Crítico", x_botoes, y_base + (ALTURA_BOTAO + ESPACO), LARGURA_BOTAO, ALTURA_BOTAO, fontes['padrao'])
            botao_esquivar = ui.desenhar_botao(screen, "Esquivar", x_botoes, y_base + (ALTURA_BOTAO + ESPACO) * 2, LARGURA_BOTAO, ALTURA_BOTAO, fontes['padrao'])
            botao_recuperar = None
            if not recuperou_stamina:
                botao_recuperar = ui.desenhar_botao(screen, "Recuperar", x_botoes, y_base + (ALTURA_BOTAO + ESPACO) * 3, LARGURA_BOTAO, ALTURA_BOTAO, fontes['padrao'])


        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                return "fugiu"

  
            if turno_jogador and event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                acao_realizada = False

                if botao_atacar.collidepoint(mx, my):
                    dano = jogador.atacar(inimigo)
                    mensagem = f"Você atacou! Dano: {dano}" if dano != 0 else "Você errou o ataque."
                    sprites.animar_acao(screen, clock, recursos, personagens, posicoes, mensagem, "jogador", "ataque", fontes)
                    acao_realizada = True
                elif botao_esquivar.collidepoint(mx, my):
                    esquivou = jogador.esquivar()
                    mensagem = "Você tentou esquivar." if esquivou else "Stamina insuficiente."
                    sprites.animar_acao(screen, clock, recursos, personagens, posicoes, mensagem, "jogador", "esquiva", fontes)
                    acao_realizada = True
                elif botao_critico.collidepoint(mx, my):
                    dano = jogador.critico(inimigo)
                    mensagem = f"Ataque crítico! Dano: {dano}" if dano != 0 else "Você errou o crítico."
                    sprites.animar_acao(screen, clock, recursos, personagens, posicoes, mensagem, "jogador", "ataque", fontes)
                    acao_realizada = True
                elif botao_recuperar and botao_recuperar.collidepoint(mx, my):
                    jogador.recuperar_stamina()
                    mensagem = "Você recuperou stamina!"
                    recuperou_stamina = True
                    acao_realizada = True

                if acao_realizada:
                    turno_jogador = False
                    aguardando_acao_inimigo = True
                    tempo_acao_inimigo = pygame.time.get_ticks() + 1000
                    semaforo_inimigo.release()

        if aguardando_acao_inimigo and pygame.time.get_ticks() >= tempo_acao_inimigo:
            semaforo_inimigo.acquire()
            if random.random() < 0.20 and inimigo.stamina >= 30: # 20% de chance de crítico
                if esquivou:
                    mensagem = "Você esquivou do ataque crítico!"
                    esquivou = False
                else:
                    dano = inimigo.critico(jogador)
                    mensagem = f"{inimigo.nome} realizou um ataque crítico! Dano: {dano}" if dano != 0 else f"{inimigo.nome} errou."
                sprites.animar_acao(screen, clock, recursos, personagens, posicoes, mensagem, "inimigo", "ataque", fontes)
            else:
                if esquivou:
                    mensagem = f"Você esquivou do ataque!"
                    esquivou = False
                else:
                    dano = inimigo.atacar(jogador)
                    mensagem = f"{inimigo.nome} atacou! Dano: {dano}" if dano != 0 else f"{inimigo.nome} errou."
                    sprites.animar_acao(screen, clock, recursos, personagens, posicoes, mensagem, "inimigo", "ataque", fontes)
            
            turno_jogador = True
            aguardando_acao_inimigo = False
            recuperou_stamina = False
            esquivou = False # Reseta a esquiva no final do turno do inimigo
            semaforo_jogador.release()
        if not jogador.esta_vivo():
            ui.mostrar_tela_final(screen, "VOCÊ SUCUMBIU PRA CIRROSE", (120, 0, 0), fontes['grande'])
            return "derrota"
        elif not inimigo.esta_vivo():
            # Mostra a mensagem de vitória específica da fase
            ui.mostrar_tela_final(screen, mensagem_vitoria, (0, 100, 0), fontes['grande'])
            return "vitoria"

        pygame.display.flip()
        clock.tick(60)

    # --- FINALIZAÇÃO ---
    pygame.mixer.music.stop()
    pygame.quit()