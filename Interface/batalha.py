import pygame
import threading
from src.personagem import Personagem
import random
from Interface import ui, sprites, telas
from src import utils
from src.loja import Loja

def executar_batalha_visual(jogador, inimigo, caminhos_recursos, loja=None):
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
        'padrao': pygame.font.SysFont("arial", 36),
        'nome': pygame.font.SysFont("arial", 36, bold=True),
        'grande': pygame.font.SysFont("arial", 48, bold=True)
    }
    clock = pygame.time.Clock()
    
    LARGURA_BOTAO, ALTURA_BOTAO = 220, 220
    
    BRANCO = (255, 255, 255)
    PRETO = (0, 0, 0)
    VERMELHO_ESCURO = (120, 0, 0)
    
    offsets_borda = [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)]

    botoes_img = {}
    botoes_img_hover = {}
    usar_imagens_botoes = False
    try:
        img_atacar_orig = pygame.image.load("Interface/UI/atacar_button.png").convert_alpha()
        img_critico_orig = pygame.image.load("Interface/UI/critico_button.png").convert_alpha()
        img_esquivar_orig = pygame.image.load("Interface/UI/esquivar2_button.png").convert_alpha()
        img_recuperar_orig = pygame.image.load("Interface/UI/recuperar_button.png").convert_alpha()

        botoes_img['atacar'] = pygame.transform.scale(img_atacar_orig, (LARGURA_BOTAO, ALTURA_BOTAO))
        botoes_img['critico'] = pygame.transform.scale(img_critico_orig, (LARGURA_BOTAO, ALTURA_BOTAO))
        botoes_img['esquivar'] = pygame.transform.scale(img_esquivar_orig, (LARGURA_BOTAO, ALTURA_BOTAO))
        botoes_img['recuperar'] = pygame.transform.scale(img_recuperar_orig, (LARGURA_BOTAO, ALTURA_BOTAO))
        
        for nome, img in botoes_img.items():
            img_hover = img.copy()
            img_hover.fill((50, 50, 50), special_flags=pygame.BLEND_RGB_ADD)
            botoes_img_hover[nome] = img_hover
        
        usar_imagens_botoes = True
    except pygame.error:
        print("Aviso: Imagens dos botões não encontradas. Usando botões padrão.")
        usar_imagens_botoes = False

    recursos = sprites.carregar_recursos_batalha(
        largura_tela, altura_tela,
        caminhos_recursos['fundo'],
        caminhos_recursos['inimigo']
    )
    fundo = recursos['fundo']
    sprite_jogador = recursos['jogador']
    sprite_inimigo = recursos['inimigo']

    posicoes = {
        'jogador_x': int(largura_tela * 0.15),
        'inimigo_x': largura_tela - sprite_inimigo.get_width() - int(largura_tela * 0.15),
        'personagem_y': altura_tela - sprite_jogador.get_height() - 20
    }
    JOGADOR_X_BASE, INIMIGO_X_BASE, PERSONAGEM_Y = posicoes['jogador_x'], posicoes['inimigo_x'], posicoes['personagem_y']

    personagens = {'jogador': jogador, 'inimigo': inimigo}

    mensagem = "O combate começou!"
    turno_jogador = True
    running = True
    aguardando_acao_inimigo = False
    tempo_acao_inimigo = 0
    esquivou = False
    recuperou_stamina = False
    semaforo_jogador.release()

    while running:
        mx, my = pygame.mouse.get_pos()
        
        screen.blit(fundo, (0, 0))
        screen.blit(sprite_jogador, (JOGADOR_X_BASE, PERSONAGEM_Y))
        screen.blit(sprite_inimigo, (INIMIGO_X_BASE, PERSONAGEM_Y))

        hud_jog_x = JOGADOR_X_BASE + sprite_jogador.get_width() // 2
        hud_jog_y = PERSONAGEM_Y - 100
        
        texto_surf = fontes['nome'].render(f"{jogador.nome}", True, BRANCO)
        texto_rect = texto_surf.get_rect(center=(hud_jog_x, hud_jog_y))
        borda_surf = fontes['nome'].render(f"{jogador.nome}", True, PRETO)
        for offset_x, offset_y in offsets_borda:
            screen.blit(borda_surf, (texto_rect.x + offset_x, texto_rect.y + offset_y))
        screen.blit(texto_surf, texto_rect)

        ui.draw_bar(screen, hud_jog_x - ui.LARGURA_BARRA_HUD // 2, hud_jog_y + 30, jogador.max_vida, jogador.vida, ui.RED)
        ui.draw_bar(screen, hud_jog_x - ui.LARGURA_BARRA_HUD // 2, hud_jog_y + 65, jogador.max_stamina, jogador.stamina, ui.BLUE)

        inimigo_nome_x = INIMIGO_X_BASE + sprite_inimigo.get_width() // 2
        inimigo_nome_y = PERSONAGEM_Y - 100

        texto_surf = fontes['nome'].render(f"{inimigo.nome}", True, BRANCO)
        texto_rect = texto_surf.get_rect(center=(inimigo_nome_x, inimigo_nome_y))
        borda_surf = fontes['nome'].render(f"{inimigo.nome}", True, PRETO)
        for offset_x, offset_y in offsets_borda:
            screen.blit(borda_surf, (texto_rect.x + offset_x, texto_rect.y + offset_y))
        screen.blit(texto_surf, texto_rect)

        ui.draw_bar(screen, inimigo_nome_x - ui.LARGURA_BARRA_HUD // 2, inimigo_nome_y + 30, inimigo.max_vida, inimigo.vida, ui.RED)

        texto_surf = fontes['grande'].render(mensagem, True, BRANCO)
        texto_rect = texto_surf.get_rect(center=(largura_tela // 2, 50))
        borda_surf = fontes['grande'].render(mensagem, True, PRETO)
        for offset_x, offset_y in offsets_borda:
            screen.blit(borda_surf, (texto_rect.x + offset_x, texto_rect.y + offset_y))
        screen.blit(texto_surf, texto_rect)

        botoes_rect = {}
        if turno_jogador:
            ESPACO = 25
            num_botoes = 4 if not recuperou_stamina else 3
            largura_total_botoes = (num_botoes * LARGURA_BOTAO) + ((num_botoes - 1) * ESPACO)
            
            x_inicial = (largura_tela - largura_total_botoes) // 2
            y_botoes = altura_tela - ALTURA_BOTAO - 40

            nomes_botoes = ['atacar', 'critico', 'esquivar']
            if not recuperou_stamina:
                nomes_botoes.append('recuperar')
            
            for i, nome in enumerate(nomes_botoes):
                x_pos = x_inicial + i * (LARGURA_BOTAO + ESPACO)
                rect = pygame.Rect(x_pos, y_botoes, LARGURA_BOTAO, ALTURA_BOTAO)
                botoes_rect[nome] = rect
                
                hovered = rect.collidepoint(mx, my)

                if usar_imagens_botoes:
                    if hovered:
                        screen.blit(botoes_img_hover[nome], rect.topleft)
                    else:
                        screen.blit(botoes_img[nome], rect.topleft)
                else:
                    cor = ui.BRIGHT_BLUE if hovered else ui.BLUE
                    ui.desenhar_botao(screen, nome.capitalize(), x_pos, y_botoes, LARGURA_BOTAO, ALTURA_BOTAO, fontes['padrao'], cor_fundo=cor)


        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                return "fugiu"

            if turno_jogador and event.type == pygame.MOUSEBUTTONDOWN:
                acao_realizada = False
                if 'atacar' in botoes_rect and botoes_rect['atacar'].collidepoint(mx, my):
                    dano = jogador.atacar(inimigo)
                    mensagem = f"Você atacou! Dano: {dano}" if dano != 0 else "Você errou o ataque."
                    sprites.animar_acao(screen, clock, recursos, personagens, posicoes, mensagem, "jogador", "ataque", fontes)
                    acao_realizada = True
                elif 'critico' in botoes_rect and botoes_rect['critico'].collidepoint(mx, my):
                    dano = jogador.critico(inimigo)
                    mensagem = f"Ataque crítico! Dano: {dano}" if dano != 0 else "Você errou o crítico."
                    sprites.animar_acao(screen, clock, recursos, personagens, posicoes, mensagem, "jogador", "ataque", fontes)
                    acao_realizada = True
                elif 'esquivar' in botoes_rect and botoes_rect['esquivar'].collidepoint(mx, my):
                    esquivou = jogador.esquivar()
                    mensagem = "Você tentou esquivar." if esquivou else "Stamina insuficiente."
                    sprites.animar_acao(screen, clock, recursos, personagens, posicoes, mensagem, "jogador", "esquiva", fontes)
                    acao_realizada = True
                elif 'recuperar' in botoes_rect and botoes_rect['recuperar'].collidepoint(mx, my):
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
            if random.random() < 0.20 and inimigo.stamina >= 30:
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
            esquivou = False
            semaforo_jogador.release()

        if not jogador.esta_vivo():
            telas.tela_derrota()
            return "derrota"
        
        elif not inimigo.esta_vivo():
            if loja:
                telas.executar_loja(loja, jogador)
            return "vitoria"
        
        pygame.display.flip()
        clock.tick(60)

    pygame.mixer.music.stop()
    pygame.quit()