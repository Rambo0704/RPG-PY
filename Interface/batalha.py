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
    font = pygame.font.SysFont("arial", 32)
    font_grande = pygame.font.SysFont("arial", 48, bold=True)
    clock = pygame.time.Clock()

    WHITE = (255, 255, 255)
    RED = (200, 0, 0)
    BLUE = (0, 0, 200)
    GRAY = (50, 50, 50)
    BLACK = (0, 0, 0)

    fundo = pygame.image.load("Interface/sprites/arena.jpg").convert()
    fundo = pygame.transform.scale(fundo, (largura_tela, altura_tela))

    sprite_jogador = pygame.image.load("Interface/sprites/figado_transparente.png").convert_alpha()
    sprite_jogador = pygame.transform.scale(sprite_jogador, (300, 500))

    sprite_inimigo = pygame.image.load("Interface/sprites/alcool_transparente.png").convert_alpha()
    sprite_inimigo = pygame.transform.scale(sprite_inimigo, (300, 500))

    def draw_bar(surface, x, y, max_val, current_val, color, label):
        pygame.draw.rect(surface, GRAY, (x, y, 200, 20), border_radius=10)
        filled = int((max(current_val, 0) / max_val) * 200)
        pygame.draw.rect(surface, color, (x, y, filled, 20), border_radius=10)
        text = font.render(f"{label}: {max(current_val, 0)} / {max_val}", True, WHITE)
        surface.blit(text, (x, y - 25))

    def draw_text(surface, text, x, y, center=False, fonte=font):
        rendered = fonte.render(text, True, WHITE)
        if center:
            rect = rendered.get_rect(center=(x, y))
            surface.blit(rendered, rect)
        else:
            surface.blit(rendered, (x, y))

    def desenhar_botao(texto, x, y, largura, altura):
        rect = pygame.Rect(x, y, largura, altura)
        pygame.draw.rect(screen, GRAY, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        txt = font.render(texto, True, WHITE)
        screen.blit(txt, (x + 10, y + 10))
        return rect

    def mostrar_tela_final(mensagem_final, cor_fundo):
        screen.fill(cor_fundo)
        texto = font_grande.render(mensagem_final, True, WHITE)
        texto_rect = texto.get_rect(center=(largura_tela // 2, altura_tela // 2))
        screen.blit(texto, texto_rect)
        pygame.display.flip()
        pygame.time.delay(3000)

    def animar_acao(personagem, lado, tipo):
        deslocamento = 40 if tipo == "ataque" else -30
        passos = 10
        for i in range(passos):
            screen.blit(fundo, (0, 0))

            offset = int(deslocamento * (i / passos))
            x_jogador = largura_tela // 10 + (offset if lado == "jogador" else 0)
            x_inimigo = largura_tela - largura_tela // 4 - (offset if lado == "inimigo" else 0)

            screen.blit(sprite_inimigo, (x_inimigo, altura_tela - altura_tela // 3))
            screen.blit(sprite_jogador, (x_jogador, altura_tela - altura_tela // 3))

            draw_text(screen, f"{jogador.nome}", 50, altura_tela - 140)
            draw_bar(screen, 50, altura_tela - 100, 100, jogador.vida, RED, "HP")
            draw_bar(screen, 50, altura_tela - 50, 100, jogador.stamina, BLUE, "Stamina")

            draw_text(screen, f"{inimigo.nome}", largura_tela - 250, altura_tela - 140)
            draw_bar(screen, largura_tela - 250, altura_tela - 100, 100, inimigo.vida, RED, "HP")
            draw_bar(screen, largura_tela - 250, altura_tela - 50, 100, inimigo.stamina, BLUE, "Stamina")

            draw_text(screen, mensagem, largura_tela // 2, altura_tela // 2 - 50, center=True, fonte=font_grande)
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

        if turno_jogador:
            botao_1 = desenhar_botao("Atacar", 400, altura_tela - 100, 160, 40)
            botao_2 = desenhar_botao("Esquivar", 580, altura_tela - 100, 160, 40)
            botao_3 = desenhar_botao("Crítico", 760, altura_tela - 100, 160, 40)
            botao_4 = desenhar_botao("Recuperar", 940, altura_tela - 100, 180, 40)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return "fugiu"

            if turno_jogador and event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if botao_1.collidepoint(mx, my):
                    animar_acao(jogador, "jogador", "ataque")
                    dano = jogador.atacar(inimigo)
                    if dano != 0:
                        mensagem = f"{jogador.nome} atacou! Dano: {dano}"
                elif botao_2.collidepoint(mx, my):
                    animar_acao(jogador, "jogador", "esquiva")
                    esquivou = jogador.esquivar()
                    mensagem = f"{jogador.nome} tentou esquivar." if esquivou else "Stamina insuficiente."
                elif botao_3.collidepoint(mx, my):
                    animar_acao(jogador, "jogador", "ataque")
                    dano = jogador.critico(inimigo)
                    mensagem = f"Ataque crítico! Dano: {dano}"
                elif botao_4.collidepoint(mx, my):
                    jogador.recuperar_stamina()
                    mensagem = "Recuperando stamina..."
                else:
                    continue

                turno_jogador = False
                aguardando_acao_inimigo = True
                tempo_acao_inimigo = pygame.time.get_ticks() + 1000
                semaforo_inimigo.release()

        if aguardando_acao_inimigo and pygame.time.get_ticks() >= tempo_acao_inimigo:
            semaforo_inimigo.acquire()
            if esquivou:
                mensagem = f"{jogador.nome} esquivou do ataque de {inimigo.nome}!"
            else:
                animar_acao(inimigo, "inimigo", "ataque")
                dano = inimigo.atacar(jogador)
                if dano != 0:
                    mensagem = f"{inimigo.nome} atacou! Dano: {dano}"
                else:
                    mensagem = f"{inimigo.nome} errou o ataque"
            turno_jogador = True
            aguardando_acao_inimigo = False
            esquivou = False
            semaforo_jogador.release()

        if not jogador.esta_vivo():
            mostrar_tela_final("VOCÊ PERDEU PRA CIRROSE", (120, 0, 0))
            return "derrota"
        elif not inimigo.esta_vivo():
            mostrar_tela_final("VOCÊ VENCEU O ALCOOLISMO - NÍVEL 1", (0, 100, 0))
            return "vitoria"

        screen.blit(sprite_inimigo, (largura_tela - largura_tela // 4, altura_tela - altura_tela // 3))
        screen.blit(sprite_jogador, (largura_tela // 10, altura_tela - altura_tela // 3))

        draw_text(screen, f"{jogador.nome}", 50, altura_tela - 140)
        draw_bar(screen, 50, altura_tela - 100, 100, jogador.vida, RED, "HP")
        draw_bar(screen, 50, altura_tela - 50, 100, jogador.stamina, BLUE, "Stamina")

        draw_text(screen, f"{inimigo.nome}", largura_tela - 250, altura_tela - 140)
        draw_bar(screen, largura_tela - 250, altura_tela - 100, 100, inimigo.vida, RED, "HP")
        draw_bar(screen, largura_tela - 250, altura_tela - 50, 100, inimigo.stamina, BLUE, "Stamina")

        draw_text(screen, mensagem, largura_tela // 2, altura_tela // 2 - 50, center=True, fonte=font_grande)

        if not turno_jogador:
            draw_text(screen, "Esperando inimigo...", largura_tela // 2, altura_tela - 40, center=True)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
