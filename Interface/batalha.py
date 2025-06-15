import pygame
import threading
from src.personagem import Personagem

def executar_batalha_visual(jogador, inimigo):
    semaforo_jogador = threading.Semaphore(1)
    semaforo_inimigo = threading.Semaphore(0)
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Combate RPG")
    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()

    WHITE = (255, 255, 255)
    RED = (200, 0, 0)
    BLUE = (0, 0, 200)
    GRAY = (50, 50, 50)

    fundo = pygame.image.load("Interface/sprites/arena.jpg").convert()
    fundo = pygame.transform.scale(fundo, (1280, 720))

    sprite_jogador = pygame.image.load("Interface/sprites/figado_transparente.png").convert_alpha()
    sprite_jogador = pygame.transform.scale(sprite_jogador, (200, 200))

    sprite_inimigo = pygame.image.load("Interface/sprites/alcool_transparente.png").convert_alpha()
    sprite_inimigo = pygame.transform.scale(sprite_inimigo, (200, 200))

    def draw_bar(surface, x, y, max_val, current_val, color, label):
        pygame.draw.rect(surface, GRAY, (x, y, 300, 25))
        filled = int((max(current_val, 0) / max_val) * 300)
        pygame.draw.rect(surface, color, (x, y, filled, 25))
        text = font.render(f"{label}: {max(current_val, 0)} / {max_val}", True, WHITE)
        surface.blit(text, (x, y - 30))

    def draw_text(surface, text, x, y):
        surface.blit(font.render(text, True, WHITE), (x, y))

    mensagem = "O combate começou!"
    turno_jogador = True
    esquivou_jogador = False
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
                    esquivou_jogador = False
                    semaforo_inimigo.release()
                elif event.key == pygame.K_2:
                    esquivou_jogador = jogador.esquivar()
                    if esquivou_jogador:
                        mensagem = f"{jogador.nome} se preparou para esquivar!"
                    else:
                        mensagem = "Stamina insuficiente para esquivar."
                    turno_jogador = False
                    semaforo_inimigo.release()
                elif event.key == pygame.K_3:
                    dano = jogador.critico(inimigo)
                    mensagem = f"Ataque crítico! Dano: {dano}"
                    turno_jogador = False
                    esquivou_jogador = False
                    semaforo_inimigo.release()
                elif event.key == pygame.K_4:
                    jogador.recuperar_stamina()
                    mensagem = "Recuperando stamina..."
                    turno_jogador = False
                    esquivou_jogador = False
                    semaforo_inimigo.release()

        if not turno_jogador and jogador.esta_vivo() and inimigo.esta_vivo():
            semaforo_inimigo.acquire()
            pygame.time.delay(1000)
            if esquivou_jogador:
                mensagem = f"{jogador.nome} esquivou do ataque!"
                esquivou_jogador = False
            else:
                dano = inimigo.atacar(jogador)
                mensagem = f"{inimigo.nome} atacou! Dano: {dano}"
            turno_jogador = True
            semaforo_jogador.release()

        if not jogador.esta_vivo():
            mensagem = "Você perdeu!"
            draw_text(screen, mensagem, 540, 340)
            pygame.display.flip()
            pygame.time.delay(2000)
            return "derrota"
        elif not inimigo.esta_vivo():
            mensagem = "Você venceu!"
            draw_text(screen, mensagem, 540, 340)
            pygame.display.flip()
            pygame.time.delay(2000)
            return "vitoria"

        screen.blit(sprite_inimigo, (900, 150))
        screen.blit(sprite_jogador, (180, 400))

        draw_text(screen, f"Inimigo: {inimigo.nome}", 900, 50)
        draw_bar(screen, 900, 90, 80, inimigo.vida, RED, "HP")
        draw_bar(screen, 900, 140, 100, inimigo.stamina, BLUE, "Stamina")

        draw_text(screen, f"Jogador: {jogador.nome}", 80, 620)
        draw_bar(screen, 80, 660, 100, jogador.vida, RED, "HP")
        draw_bar(screen, 80, 700, 100, jogador.stamina, BLUE, "Stamina")

        draw_text(screen, mensagem, 480, 320)
        if turno_jogador:
            draw_text(screen, "[1] Atacar  [2] Esquivar  [3] Crítico  [4] Recuperar", 400, 660)
        else:
            draw_text(screen, "Esperando inimigo...", 500, 660)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
