import pygame
import sys
from . import ui
from src import utils

ESTADO_TELA_INICIAL = "TELA_INICIAL"
ESTADO_EM_BATALHA = "EM_BATALHA"
ESTADO_FIM_DE_JOGO = "FIM_DE_JOGO"

def tela_inicial():
    pygame.init()
    utils.iniciar_musica("Interface/audio/figado_valente.mp3")
    SCREEN = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption("Menu")

    BG = pygame.image.load("Interface/UI/menubg1.png").convert()
    BG = pygame.transform.scale(BG, (1920, 1080))

    def get_font(size):
        return pygame.font.SysFont("arialblack", size)

    play_image = pygame.image.load("Interface/UI/jogar1.png").convert_alpha()
    play_image = pygame.transform.scale(play_image, (350, 350))  # botão maior

    sair_image = pygame.image.load("Interface/UI/sair.png").convert_alpha()
    sair_image = pygame.transform.scale(sair_image, (250, 250))  # botão maior

    # Centralização horizontal e ajuste vertical
    centro_x = 1920 // 2
    PLAY_BUTTON = ui.Button(image=play_image, x_pos=centro_x, y_pos=500)
    QUIT_BUTTON = ui.Button(image=sair_image, x_pos=centro_x, y_pos=800)

    try:
        title_image = pygame.image.load("Interface/UI/header3.png").convert_alpha()
        title_image = pygame.transform.scale(title_image, (700, 400))
        title_rect = title_image.get_rect(center=(centro_x, 200))
    except pygame.error as e:
        print("Erro ao carregar a imagem do título:", e)
        pygame.quit()
        sys.exit()

    while True:
        SCREEN.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.blit(title_image, title_rect)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkClick(MENU_MOUSE_POS):
                    return ESTADO_EM_BATALHA
                if QUIT_BUTTON.checkClick(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def executar_loja(Loja, Personagem):

    pygame.init()

    WIDTH, HEIGHT = 1920, 1080
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Jogo com Loja de Buffs")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("arialblack", 24)

    # Cores
    WHITE = (255, 255, 255)
    GRAY = (180, 180, 180)
    GREEN = (50, 255, 100)

    loja_bg = pygame.image.load("Interface/UI/wood_floor.jpg").convert()
    loja_bg = pygame.transform.scale(loja_bg, (WIDTH, HEIGHT))

    titulo_loja_img = pygame.image.load("Interface/UI/loja.png").convert_alpha()
    titulo_loja_img = pygame.transform.scale(titulo_loja_img, (450, 370))
    titulo_loja_rect = titulo_loja_img.get_rect(center=(WIDTH // 2, 70))

    class ItemButton:
        def __init__(self, buff, image_path, x, y, largura=120, altura=110, pos_texto=None):
            self.buff = buff
            self.original_image = pygame.image.load(image_path).convert_alpha()
            self.largura_padrao = largura
            self.altura_padrao = altura
            self.image = pygame.transform.scale(self.original_image, (largura, altura))
            self.rect = self.image.get_rect(center=(x, y))
            self.hovered = False
            self.pos_texto = pos_texto

        def update(self, mouse_pos):
            self.hovered = self.rect.collidepoint(mouse_pos)
            tamanho = (int(self.largura_padrao * 1.2), int(self.altura_padrao * 1.2)) if self.hovered else (self.largura_padrao, self.altura_padrao)
            self.image = pygame.transform.scale(self.original_image, tamanho)
            self.rect = self.image.get_rect(center=self.rect.center)

        def draw(self, surface):
            surface.blit(self.image, self.rect)

        def check_click(self, mouse_pos):
            return self.rect.collidepoint(mouse_pos)

    class Button:
        def __init__(self, x, y, w, h, text, callback):
            self.rect = pygame.Rect(x, y, w, h)
            self.text = text
            self.callback = callback
            self.hovered = False

        def draw(self, surface):
            cor = GREEN if self.hovered else GRAY
            pygame.draw.rect(surface, cor, self.rect, border_radius=8)
            text_render = font.render(self.text, True, WHITE)
            surface.blit(text_render, text_render.get_rect(center=self.rect.center))

        def update(self, mouse_pos, mouse_click):
            self.hovered = self.rect.collidepoint(mouse_pos)
            if self.hovered and mouse_click:
                self.callback()

    loja = Loja()

    atributo_para_imagem = {
        "ataque": "Interface/UI/seringa.png",
        "escudo": "Interface/UI/escudo.png",
        "vida": "Interface/UI/agua.png",
    }

    itens_loja = []
    posicoes_botoes = [(250, 170), (550, 170), (250, 350), (550, 350)]
    posicoes_textos = [(140, 250), (440, 250), (140, 420), (440, 420)]

    for i, buff in enumerate(loja.buffs):
        img_path = atributo_para_imagem.get(buff.atributo, "Interface/UI/stamina.png")
        x, y = posicoes_botoes[i]
        pos_txt = posicoes_textos[i]
        itens_loja.append(ItemButton(buff, img_path, x, y, pos_texto=pos_txt))

    def aplicar_efeito(item_button):
        buff = item_button.buff
        if Personagem.moedas >= buff.preco:
            Personagem.moedas -= buff.preco
            buff.aplicar(Personagem)
            print(f"Comprou: {buff.nome}")
        else:
            print("Moedas insuficientes!")

    estado_do_jogo = "luta"

    def continuar_luta():
        nonlocal estado_do_jogo
        estado_do_jogo = "luta"

    botao_continuar = Button(500, 500, 180, 50, "Continuar", continuar_luta)

    def mostrar_loja():
        screen.blit(loja_bg, (0, 0))
        screen.blit(titulo_loja_img, titulo_loja_rect)

        moedas_txt = font.render(f"Moedas: {Personagem.moedas}", True, WHITE)
        screen.blit(moedas_txt, (20, 20))

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        for item in itens_loja:
            item.update(mouse_pos)
            item.draw(screen)

            txt = font.render(f"{item.buff.nome} - {item.buff.preco}", True, WHITE)
            if item.pos_texto:
                screen.blit(txt, item.pos_texto)
            else:
                screen.blit(txt, (item.rect.left, item.rect.bottom + 5))

            if mouse_click and item.check_click(mouse_pos):
                aplicar_efeito(item)

        botao_continuar.update(mouse_pos, mouse_click)
        botao_continuar.draw(screen)

    def mostrar_luta():
        screen.fill((10, 10, 20))
        txt = font.render("Luta terminada! Pressione espaço para ir à loja.", True, WHITE)
        screen.blit(txt, (50, HEIGHT//2))

        stats = font.render(f"Vida: {Personagem.vida} | Ataque: {Personagem.ataque} | Escudo: {Personagem.escudo} | Stamina: {Personagem.stamina}", True, GREEN)
        screen.blit(stats, (50, 50))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if estado_do_jogo == "luta":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    estado_do_jogo = "loja"

        if estado_do_jogo == "luta":
            mostrar_luta()
        elif estado_do_jogo == "loja":
            mostrar_loja()

        pygame.display.flip()
        clock.tick(60)
