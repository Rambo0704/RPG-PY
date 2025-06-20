import pygame
import threading
from src.personagem import Personagem

def executar_batalha_visual(jogador, inimigo):
    semaforo_jogador = threading.Semaphore(1)
    semaforo_inimigo = threading.Semaphore(0)

    pygame.init()
    info = pygame.display.Info()
    largura_tela, altura_tela = info.current_w, info.current_h
    screen = pygame.display.set_mode((largura_tela, altura_tela), pygame.FULLSCREEN)
    pygame.display.set_caption("Combate RPG")
    font = pygame.font.SysFont("arial", 30)
    font_nome = pygame.font.SysFont("arial", 36, bold=True)
    font_grande = pygame.font.SysFont("arial", 48, bold=True)
    clock = pygame.time.Clock()

    WHITE = (255, 255, 255)
    RED = (200, 0, 0)
    BLUE = (0, 100, 255)
    GRAY = (50, 50, 50)
    BLACK = (0, 0, 0)

    fundo = pygame.image.load("Interface/sprites/arena.jpg").convert()
    fundo = pygame.transform.scale(fundo, (largura_tela, altura_tela))

    sprite_jogador = pygame.image.load("Interface/sprites/figado_transparente.png").convert_alpha()
    sprite_jogador = pygame.transform.scale(sprite_jogador, (300, 500))

    sprite_inimigo = pygame.image.load("Interface/sprites/alcool_transparente.png").convert_alpha()
    sprite_inimigo = pygame.transform.scale(sprite_inimigo, (300, 500))

    JOGADOR_X_BASE = largura_tela * 0.15
    INIMIGO_X_BASE = largura_tela - sprite_inimigo.get_width() - (largura_tela * 0.15)
    PERSONAGEM_Y = altura_tela - sprite_jogador.get_height() + 40
    
    LARGURA_BARRA_HUD = 280

    def draw_bar(surface, x, y, max_val, current_val, color, label):
        altura_barra = 25
        val_atual = max(current_val, 0)
        sombra_rect = pygame.Rect(x+3, y+3, LARGURA_BARRA_HUD, altura_barra)
        pygame.draw.rect(surface, (0,0,0,150), sombra_rect, border_radius=8)
        pygame.draw.rect(surface, GRAY, (x, y, LARGURA_BARRA_HUD, altura_barra), border_radius=8)
        largura_preenchimento = int((val_atual / max_val) * (LARGURA_BARRA_HUD - 6))
        pygame.draw.rect(surface, color, (x + 3, y + 3, largura_preenchimento, altura_barra - 6), border_radius=6)
        texto_label = font.render(label, True, WHITE)
        surface.blit(texto_label, (x + 10, y))
        texto_valores = font.render(f"{val_atual}/{max_val}", True, WHITE)
        rect_valores = texto_valores.get_rect(right=x + LARGURA_BARRA_HUD - 15, centery=y + altura_barra / 2)
        surface.blit(texto_valores, rect_valores)

    def draw_text(surface, text, x, y, center=False, fonte=font_nome):
        sombra_render = fonte.render(text, True, BLACK)
        if center:
            sombra_rect = sombra_render.get_rect(center=(x+2, y+2))
        else:
            sombra_rect = (x+2, y+2)
        surface.blit(sombra_render, sombra_rect)
        rendered = fonte.render(text, True, WHITE)
        if center:
            rect = rendered.get_rect(center=(x, y))
            surface.blit(rendered, rect)
        else:
            surface.blit(rendered, (x, y))

    def desenhar_botao(texto, x, y, largura, altura):
        rect = pygame.Rect(x, y, largura, altura)
        mx, my = pygame.mouse.get_pos()
        cor_base = (0, 50, 100, 200)
        cor_hover = (50, 100, 180, 220)
        cor_atual = cor_hover if rect.collidepoint(mx, my) else cor_base
        botao_surf = pygame.Surface((largura, altura), pygame.SRCALPHA)
        botao_surf.fill(cor_atual)
        screen.blit(botao_surf, rect.topleft)
        pygame.draw.rect(screen, WHITE, rect, 2, border_radius=10)
        txt_surf = font.render(texto, True, WHITE)
        txt_rect = txt_surf.get_rect(center=rect.center)
        screen.blit(txt_surf, txt_rect)
        return rect

    def mostrar_tela_final(mensagem_final, cor_fundo):
        screen.fill(cor_fundo)
        texto = font_grande.render(mensagem_final, True, WHITE)
        texto_rect = texto.get_rect(center=(largura_tela // 2, altura_tela // 2))
        screen.blit(texto, texto_rect)
        pygame.display.flip()
        pygame.time.delay(3000)

    def animar_acao(personagem, lado, tipo):
        deslocamento = 60 if tipo == "ataque" else -40
        passos = 15
        for i in range(passos * 2):
            progresso = i if i < passos else (passos * 2) - i
            offset = int(deslocamento * (progresso / passos))
            x_jogador_anim = JOGADOR_X_BASE + (offset if lado == "jogador" else 0)
            x_inimigo_anim = INIMIGO_X_BASE - (offset if lado == "inimigo" else 0)
            screen.blit(fundo, (0, 0))
            screen.blit(sprite_jogador, (x_jogador_anim, PERSONAGEM_Y))
            screen.blit(sprite_inimigo, (x_inimigo_anim, PERSONAGEM_Y))
            draw_text(screen, f"{jogador.nome}", 50, altura_tela - 130)
            draw_bar(screen, 50, altura_tela - 90, 100, jogador.vida, RED, "HP")
            draw_bar(screen, 50, altura_tela - 55, 100, jogador.stamina, BLUE, "Stamina")
            hud_inimigo_x = largura_tela - LARGURA_BARRA_HUD - 50
            draw_text(screen, f"{inimigo.nome}", hud_inimigo_x, 40)
            draw_bar(screen, hud_inimigo_x, 80, 100, inimigo.vida, RED, "HP")
            draw_text(screen, mensagem, largura_tela // 2, altura_tela // 4, center=True, fonte=font_grande)
            pygame.display.flip()
            clock.tick(60)

    mensagem = "O combate começou!"
    turno_jogador = True
    running = True
    aguardando_acao_inimigo = False
    tempo_acao_inimigo = 0
    esquivou = False
    semaforo_jogador.release()

    while running:
        screen.blit(fundo, (0, 0))
        screen.blit(sprite_jogador, (JOGADOR_X_BASE, PERSONAGEM_Y))
        screen.blit(sprite_inimigo, (INIMIGO_X_BASE, PERSONAGEM_Y))

        draw_text(screen, mensagem, largura_tela // 2, altura_tela // 4, center=True, fonte=font_grande)
        draw_text(screen, f"{jogador.nome}", 50, altura_tela - 130)
        draw_bar(screen, 50, altura_tela - 90, 100, jogador.vida, RED, "HP")
        draw_bar(screen, 50, altura_tela - 55, 100, jogador.stamina, BLUE, "Stamina")

        hud_inimigo_x = INIMIGO_X_BASE
        hud_inimigo_y = PERSONAGEM_Y - 60
        draw_text(screen, f"{inimigo.nome}", hud_inimigo_x, hud_inimigo_y - 30)
        draw_bar(screen, hud_inimigo_x, hud_inimigo_y, 100, inimigo.vida, RED, "HP")

        if turno_jogador:
            LARGURA_BOTAO = 200
            ALTURA_BOTAO = 55
            ESPACO = 15
            x_botoes = JOGADOR_X_BASE + sprite_jogador.get_width() + 30
            y_base = PERSONAGEM_Y + 40

            botao_atacar    = desenhar_botao("Atacar",    x_botoes, y_base,                        LARGURA_BOTAO, ALTURA_BOTAO)
            botao_critico   = desenhar_botao("Crítico",   x_botoes, y_base + (ALTURA_BOTAO + ESPACO) * 1, LARGURA_BOTAO, ALTURA_BOTAO)
            botao_esquivar  = desenhar_botao("Esquivar",  x_botoes, y_base + (ALTURA_BOTAO + ESPACO) * 2, LARGURA_BOTAO, ALTURA_BOTAO)
            botao_recuperar = desenhar_botao("Recuperar", x_botoes, y_base + (ALTURA_BOTAO + ESPACO) * 3, LARGURA_BOTAO, ALTURA_BOTAO)

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
                    animar_acao(jogador, "jogador", "ataque")
                    acao_realizada = True
                elif botao_esquivar.collidepoint(mx, my):
                    esquivou = jogador.esquivar()
                    mensagem = "Você tentou esquivar." if esquivou else "Stamina insuficiente."
                    animar_acao(jogador, "jogador", "esquiva")
                    acao_realizada = True
                elif botao_critico.collidepoint(mx, my):
                    dano = jogador.critico(inimigo)
                    mensagem = f"Ataque crítico! Dano: {dano}" if dano != 0 else "Você errou o crítico."
                    animar_acao(jogador, "jogador", "ataque")
                    acao_realizada = True
                elif botao_recuperar.collidepoint(mx, my):
                    jogador.recuperar_stamina()
                    mensagem = "Você recuperou stamina!"
                    acao_realizada = True

                if acao_realizada:
                    turno_jogador = False
                    aguardando_acao_inimigo = True
                    tempo_acao_inimigo = pygame.time.get_ticks() + 1000
                    semaforo_inimigo.release()

        if aguardando_acao_inimigo and pygame.time.get_ticks() >= tempo_acao_inimigo:
            semaforo_inimigo.acquire()
            if esquivou:
                mensagem = f"Você esquivou do ataque!"
                esquivou = False
            else:
                dano = inimigo.atacar(jogador)
                mensagem = f"{inimigo.nome} atacou! Dano: {dano}" if dano != 0 else f"{inimigo.nome} errou."
                animar_acao(inimigo, "inimigo", "ataque")
            turno_jogador = True
            aguardando_acao_inimigo = False
            semaforo_jogador.release()

        if not jogador.esta_vivo():
            mostrar_tela_final("VOCÊ PERDEU PRA CIRROSE", (120, 0, 0))
            return "derrota"
        elif not inimigo.esta_vivo():
            mostrar_tela_final("VOCÊ VENCEU O ALCOOLISMO - NÍVEL 1", (0, 100, 0))
            return "vitoria"

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
