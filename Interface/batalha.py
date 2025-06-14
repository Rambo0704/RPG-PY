import pygame
import threading
from src.personagem import Personagem

def executar_batalha_visual(jogador, inimigo):
    semaforo_jogador = threading.Semaphore(1)
    semaforo_inimigo = threading.Semaphore(0)
    pygame.init()
    screen = pygame.display.set_mode((720, 480))
    pygame.display.set_caption("Combate RPG")
    font = pygame.font.Font(None, 30)
    clock = pygame.time.Clock()

    WHITE = (255, 255, 255)
    RED = (200, 0, 0)
    BLUE = (0, 0, 200)
    GRAY = (50, 50, 50)

    fundo = pygame.image.load("Interface/sprites/arena.jpg").convert()
    fundo = pygame.transform.scale(fundo, (800, 600))

    sprite_jogador = pygame.image.load("Interface/sprites/figado_transparente.png").convert_alpha()
    sprite_jogador = pygame.transform.scale(sprite_jogador, (150, 150))

    sprite_inimigo = pygame.image.load("Interface/sprites/alcool_transparente.png").convert_alpha()
    sprite_inimigo = pygame.transform.scale(sprite_inimigo, (150, 150))

    def draw_bar(surface, x, y, max_val, current_val, color, label):
        pygame.draw.rect(surface, GRAY, (x, y, 200, 20))
        filled = int((max(current_val, 0) / max_val) * 200)
        pygame.draw.rect(surface, color, (x, y, filled, 20))
        text = font.render(f"{label}: {max(current_val, 0)} / {max_val}", True, WHITE)
        surface.blit(text, (x, y - 25))

    def draw_text(surface, text, x, y):
        surface.blit(font.render(text, True, WHITE), (x, y))

    mensagem = "O combate começou!"
    turno_jogador = True
    semaforo_jogador.release()
    running = True

    while running:
        screen.blit(fundo, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return "fugiu"

            if turno_jogador and event.type == pygame.KEYDOWN:
                semaforo_jogador.acquire()
                if event.key == pygame.K_1:
                    dano = jogador.atacar(inimigo)
                    mensagem = f"{jogador.nome} atacou! Dano: {dano}"
                    turno_jogador = False
                    semaforo_inimigo.release()
                elif event.key == pygame.K_2:
                    esquivou = jogador.esquivar()
                    mensagem = f"{jogador.nome} tentou esquivar." if esquivou else "Stamina insuficiente."
                    turno_jogador = False
                    semaforo_inimigo.release()
                elif event.key == pygame.K_3:
                    dano = jogador.critico(inimigo)
                    mensagem = f"Ataque crítico! Dano: {dano}"
                    turno_jogador = False
                    semaforo_inimigo.release()
                elif event.key == pygame.K_4:
                    jogador.recuperar_stamina()
                    mensagem = "Recuperando stamina..."
                    turno_jogador = False
                    semaforo_inimigo.release()

        if not turno_jogador and jogador.esta_vivo() and inimigo.esta_vivo():
            semaforo_inimigo.acquire()
            pygame.time.delay(1000)
            dano = inimigo.atacar(jogador)
            mensagem = f"{inimigo.nome} atacou! Dano: {dano}"
            turno_jogador = True
            semaforo_jogador.release()

        if not jogador.esta_vivo():
            mensagem = "Você perdeu!"
            draw_text(screen, mensagem, 300, 300)
            pygame.display.flip()
            pygame.time.delay(2000)
            return "derrota"
        elif not inimigo.esta_vivo():
            mensagem = "Você venceu!"
            draw_text(screen, mensagem, 300, 300)
            pygame.display.flip()
            pygame.time.delay(2000)
            return "vitoria"

        screen.blit(sprite_inimigo, (520, 120))
        screen.blit(sprite_jogador, (120, 300))

        draw_text(screen, f"Inimigo: {inimigo.nome}", 500, 50)
        draw_bar(screen, 500, 90, 80, inimigo.vida, RED, "HP")
        draw_bar(screen, 500, 140, 100, inimigo.stamina, BLUE, "Stamina")

        draw_text(screen, f"Jogador: {jogador.nome}", 50, 460)
        draw_bar(screen, 50, 500, 100, jogador.vida, RED, "HP")
        draw_bar(screen, 50, 550, 100, jogador.stamina, BLUE, "Stamina")

        draw_text(screen, mensagem, 200, 250)
        if turno_jogador:
            draw_text(screen, "[1] Atacar [2] Esquivar [3] Crítico [4] Recuperar", 50, 580)
        else:
            draw_text(screen, "Esperando inimigo...", 50, 580)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()