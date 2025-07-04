import pygame
import sys
from . import ui
from src import utils

ESTADO_TELA_INICIAL = "TELA_INICIAL"
ESTADO_EM_BATALHA = "EM_BATALHA"
ESTADO_FIM_DE_JOGO = "FIM_DE_JOGO"

PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Fígado Valente")
fontes = {
    'grande': pygame.font.SysFont("arialblack", 60)
}

def tela_inicial():
    utils.iniciar_musica("Interface/audio/figado_valente.mp3")
    BG = pygame.image.load("Interface/UI/menubg1.png").convert()
    BG = pygame.transform.scale(BG, (1920, 1080))

    def get_font(size):
        return pygame.font.SysFont("arialblack", size)

    play_image = pygame.image.load("Interface/UI/jogar1.png").convert_alpha()
    play_image = pygame.transform.scale(play_image, (350, 350))
    sair_image = pygame.image.load("Interface/UI/sair.png").convert_alpha()
    sair_image = pygame.transform.scale(sair_image, (250, 250))
    centro_x = 1920 // 2

    PLAY_BUTTON = ui.Button(image=play_image, x_pos=centro_x, y_pos=500)
    QUIT_BUTTON = ui.Button(image=sair_image, x_pos=centro_x, y_pos=800)
    title_image = pygame.image.load("Interface/UI/header3.png").convert_alpha()
    title_image = pygame.transform.scale(title_image, (700, 400))
    title_rect = title_image.get_rect(center=(centro_x, 200))

    while True:
        screen.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        screen.blit(title_image, title_rect)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

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

def executar_loja(loja, personagem):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arialblack", 24)
    WHITE = (255, 255, 255)
    GRAY = (180, 180, 180)
    GREEN = (50, 255, 100)

    largura_tela, altura_tela = 1920, 1080
    screen = pygame.display.set_mode((largura_tela, altura_tela))

    loja_bg = pygame.image.load("Interface/UI/wood_floor.jpg").convert()
    loja_bg = pygame.transform.scale(loja_bg, (largura_tela, altura_tela))
    titulo_loja_img = pygame.image.load("Interface/UI/loja.png").convert_alpha()
    titulo_loja_img = pygame.transform.scale(titulo_loja_img, (450, 370))
    titulo_loja_rect = titulo_loja_img.get_rect(center=(largura_tela // 2, 120))
    mensagem_buff = ""
    tempo_mensagem = 3000

    class ItemButton:
        def __init__(self, buff, image_path, center_x, center_y, largura=120, altura=110):
            self.buff = buff
            self.original_image = pygame.image.load(image_path).convert_alpha()
            self.largura_padrao = largura
            self.altura_padrao = altura
            self.image = pygame.transform.scale(self.original_image, (largura, altura))
            self.rect = self.image.get_rect(center=(center_x, center_y))
            self.hovered = False

        def update(self, mouse_pos):
            self.hovered = self.rect.collidepoint(mouse_pos)
            tamanho = (int(self.largura_padrao * 1.2), int(self.altura_padrao * 1.2)) if self.hovered else (self.largura_padrao, self.altura_padrao)
            self.image = pygame.transform.scale(self.original_image, tamanho)
            self.rect = self.image.get_rect(center=self.rect.center)

        def draw(self, surface):
            surface.blit(self.image, self.rect)
            texto = font.render(f"{self.buff.nome} - {self.buff.preco}", True, WHITE)
            surface.blit(texto, texto.get_rect(center=(self.rect.centerx, self.rect.bottom + 20)))

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

    atributo_para_imagem = {
        "ataque": "Interface/UI/seringa.png",
        "escudo": "Interface/UI/escudo.png",
        "vida": "Interface/UI/agua.png",
        "stamina": "Interface/UI/stamina.png",
    }

    itens_loja = []
    espaco_x = 250
    espaco_y = 200
    offset_x = largura_tela // 2 - espaco_x
    offset_y = 300

    for i, buff in enumerate(loja.buffs):
        img_path = atributo_para_imagem.get(buff.atributo, "Interface/UI/stamina.png")
        col = i % 2
        row = i // 2
        x = offset_x + col * espaco_x * 2
        y = offset_y + row * espaco_y
        itens_loja.append(ItemButton(buff, img_path, x, y))

    def aplicar_efeito(item_button):
        buff = item_button.buff
        if personagem.moedas >= buff.preco:
            ataque_antes = personagem.ataque
            escudo_antes = personagem.escudo
            vida_antes = personagem.vida
            stamina_antes = personagem.stamina

            personagem.moedas -= buff.preco
            buff.aplicar(personagem)

            ataque_depois = personagem.ataque
            escudo_depois = personagem.escudo
            vida_depois = personagem.vida
            stamina_depois = personagem.stamina

            print(f"\nAplicando buff: {buff.nome}")
            print(f"Ataque: {ataque_antes} -> {ataque_depois} {'(buffado!)' if ataque_depois != ataque_antes else ''}")
            print(f"Escudo: {escudo_antes} -> {escudo_depois} {'(buffado!)' if escudo_depois != escudo_antes else ''}")
            print(f"Vida: {vida_antes} -> {vida_depois} {'(buffado!)' if vida_depois != vida_antes else ''}")
            print(f"Stamina: {stamina_antes} -> {stamina_depois} {'(buffado!)' if stamina_depois != stamina_antes else ''}")
            nonlocal mensagem_buff, tempo_mensagem
            mensagem_buff = f"{buff.nome} aplicado! +{buff.valor} {buff.atributo}"
            tempo_mensagem = pygame.time.get_ticks() + 3000
        else:
            print("Moedas insuficientes para comprar este buff.")

    estado_do_jogo = "luta"

    def continuar_luta():
        nonlocal estado_do_jogo
        estado_do_jogo = "sair"

    botao_continuar = Button(largura_tela // 2 - 90, altura_tela - 120, 180, 50, "Continuar", continuar_luta)

    def mostrar_loja():
        screen.blit(loja_bg, (0, 0))
        screen.blit(titulo_loja_img, titulo_loja_rect)

        moedas_txt = font.render(f"Moedas: {personagem.moedas}", True, WHITE)
        screen.blit(moedas_txt, moedas_txt.get_rect(topright=(largura_tela - 30, 30)))

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        for item in itens_loja:
            item.update(mouse_pos)
            item.draw(screen)

        botao_continuar.update(mouse_pos, mouse_click)
        botao_continuar.draw(screen)

        if mensagem_buff and pygame.time.get_ticks() < tempo_mensagem:
            msg_render = font.render(mensagem_buff, True, WHITE)
            screen.blit(msg_render, msg_render.get_rect(center=(largura_tela // 2, altura_tela - 180)))

    def caminho_loja():
        fundo_caminho_img = pygame.image.load("Interface/UI/fundo_caminho.jpg").convert()
        fundo_caminho_img = pygame.transform.scale(fundo_caminho_img, (largura_tela, altura_tela))
        screen.blit(fundo_caminho_img, (0, 0))

        fonte_titulo = pygame.font.SysFont("arialblack", 48)
        fonte_stats = pygame.font.SysFont("arialblack", 38)

        texto_loja = "Luta terminada! Pressione espaço para ir à loja."
        texto_stats = f"Vida Maxima: {personagem.max_vida} | Ataque: {personagem.ataque} | Escudo: {personagem.escudo} | Stamina Maxima: {personagem.max_stamina}"

        txt_render = fonte_titulo.render(texto_loja, True, WHITE)
        stats_render = fonte_stats.render(texto_stats, True, GREEN)

        for dx in [-2, 0, 2]:
            for dy in [-2, 0, 2]:
                if dx != 0 or dy != 0:
                    screen.blit(fonte_titulo.render(texto_loja, True, (0, 0, 0)),
                                txt_render.get_rect(center=(largura_tela // 2 + dx, altura_tela // 2 + dy)))
                    screen.blit(fonte_stats.render(texto_stats, True, (0, 0, 0)),
                                stats_render.get_rect(center=(largura_tela // 2 + dx, 50 + dy)))

        screen.blit(txt_render, txt_render.get_rect(center=(largura_tela // 2, altura_tela // 2)))
        screen.blit(stats_render, stats_render.get_rect(center=(largura_tela // 2, 50)))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if estado_do_jogo == "luta":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    estado_do_jogo = "loja"

            elif estado_do_jogo == "loja":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    for item in itens_loja:
                        if item.check_click(mouse_pos):
                            aplicar_efeito(item)

        if estado_do_jogo == "luta":
            caminho_loja()
        elif estado_do_jogo == "loja":
            mostrar_loja()
        elif estado_do_jogo == "sair":
            personagem.vida = personagem.max_vida
            personagem.stamina = personagem.max_stamina
            personagem.moedas += 50
            return "proxima_fase"

        pygame.display.flip()
        clock.tick(60)

def tela_derrota():
    utils.iniciar_musica("Interface/audio/musica2_derrota.mp3")
    largura_tela, altura_tela = screen.get_size()
    fundo = pygame.image.load("Interface/UI/fundo_derrota.jpg").convert()
    fundo = pygame.transform.scale(fundo, (largura_tela, altura_tela))
    screen.blit(fundo, (0, 0))

    texto = "VOCÊ SUCUMBIU PARA A CIRROSE"
    fonte = fontes['grande']
    texto_surf = fonte.render(texto, True, PRETO)
    texto_rect = texto_surf.get_rect(center=(largura_tela // 2, altura_tela // 2))
    offsets_borda = [(-2, -2), (2, -2), (-2, 2), (2, 2)]
    borda_surf = fonte.render(texto, True, BRANCO)

    for offset_x, offset_y in offsets_borda:
        screen.blit(borda_surf, (texto_rect.x + offset_x, texto_rect.y + offset_y))

    screen.blit(texto_surf, texto_rect)
    pygame.display.flip()
    pygame.time.wait(5000)
def tela_fim_de_jogo():
    utils.iniciar_musica("Interface/audio/musica_final.mp3")
    pygame.mouse.set_visible(True)
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    largura_tela, altura_tela = screen.get_size()

    fundo = pygame.image.load("Interface/UI/fundo_fim.jpeg").convert()
    fundo = pygame.transform.scale(fundo, (largura_tela, altura_tela))

    fonte_titulo = pygame.font.SysFont("arial", 48, bold=True)
    fonte_creditos = pygame.font.SysFont("arial", 36)
    fonte_botao = pygame.font.SysFont("arial", 32)

    botao_largura, botao_altura = 300, 60
    botao_rect = pygame.Rect((largura_tela - botao_largura) // 2, altura_tela - 120, botao_largura, botao_altura)

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if botao_rect.collidepoint(evento.pos):
                    return ESTADO_TELA_INICIAL

        screen.blit(fundo, (0, 0))

        mensagem = "OBRIGADO POR JOGAR FIGADO'S ADVENTURE"
        texto_surf = fonte_titulo.render(mensagem, True, PRETO)
        texto_rect = texto_surf.get_rect(center=(largura_tela // 2, altura_tela // 2 - 100))
        borda_surf = fonte_titulo.render(mensagem, True, BRANCO)

        for dx, dy in [(-2, -2), (2, -2), (-2, 2), (2, 2)]:
            screen.blit(borda_surf, (texto_rect.x + dx, texto_rect.y + dy))
        screen.blit(texto_surf, texto_rect)

        nomes = ["Créditos:", "Gabriel Rambo", "Pedro Viegas", "Pedro Miguel", "Rafael Machado"]
        for i, nome in enumerate(nomes):
            y_pos = altura_tela // 2 + 20 + i * 50
            nome_surf = fonte_creditos.render(nome, True, BRANCO)
            screen.blit(nome_surf, nome_surf.get_rect(center=(largura_tela // 2, y_pos)))

        pygame.draw.rect(screen, PRETO, botao_rect, border_radius=12)
        texto_botao = fonte_botao.render("Voltar ao menu", True, BRANCO)
        screen.blit(texto_botao, texto_botao.get_rect(center=botao_rect.center))

        pygame.display.flip()
        pygame.time.Clock().tick(60)