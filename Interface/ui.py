import pygame
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE = (0, 100, 255)
GRAY = (50, 50, 50)
BLACK = (0, 0, 0)

LARGURA_BARRA_HUD = 280

def draw_bar(surface, x, y, max_val, current_val, color):
    altura_barra = 25
    val_atual = max(current_val, 0)
    sombra_rect = pygame.Rect(x+3, y+3, LARGURA_BARRA_HUD, altura_barra)
    pygame.draw.rect(surface, (0,0,0,150), sombra_rect, border_radius=8)
    pygame.draw.rect(surface, GRAY, (x, y, LARGURA_BARRA_HUD, altura_barra), border_radius=8)
    largura_preenchimento = int((val_atual / max_val) * (LARGURA_BARRA_HUD - 6)) if max_val > 0 else 0
    pygame.draw.rect(surface, color, (x + 3, y + 3, largura_preenchimento, altura_barra - 6), border_radius=6)

def draw_text(surface, text, x, y, font, center=False):
    sombra_render = font.render(text, True, BLACK)
    if center:
        sombra_rect = sombra_render.get_rect(center=(x+2, y+2))
    else:
        sombra_rect = (x+2, y+2)
    surface.blit(sombra_render, sombra_rect)
    
    rendered = font.render(text, True, WHITE)
    if center:
        rect = rendered.get_rect(center=(x, y))
        surface.blit(rendered, rect)
    else:
        surface.blit(rendered, (x, y))

def desenhar_botao(screen, texto, x, y, largura, altura, font):
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

def mostrar_tela_final(screen, mensagem_final, font_grande):
    largura_tela, altura_tela = screen.get_size()
    screen.fill("Interface/UI/wood_floor.jpg")
    texto = font_grande.render(mensagem_final, True, WHITE)
    texto_rect = texto.get_rect(center=(largura_tela // 2, altura_tela // 2))
    screen.blit(texto, texto_rect)
    pygame.display.flip()
    pygame.time.delay(3000)
class Button:
    def __init__(self, image, x_pos, y_pos, text_input=None, font=None,
                 base_color=(255, 255, 255), hover_color=(181, 101, 29), hover_scale=1.1):
        self.original_image = image  # guarda imagem original
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.font = font
        self.base_color = base_color
        self.hover_color = hover_color
        self.text_input = text_input
        self.hover_scale = hover_scale
        self.clicked = False
        self.is_hovered = False

        # Renderizar texto, se houver
        if self.text_input and self.font:
            self.text = self.font.render(self.text_input, True, self.base_color)
            self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        else:
            self.text = None
            self.text_rect = None

        # Rect da imagem
        if self.image is not None:
            self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        else:
            self.rect = pygame.Rect(0, 0, 200, 50)
            self.rect.center = (self.x_pos, self.y_pos)

    def update(self, surface):
        # Desenha imagem (já pode estar redimensionada)
        if self.image is not None:
            surface.blit(self.image, self.rect)
        else:
            pygame.draw.rect(surface, "gray", self.rect, border_radius=10)

        # Desenha texto se existir
        if self.text:
            surface.blit(self.text, self.text_rect)

    def changeColor(self, position):
        hovering = self.rect.collidepoint(position)

        # Hover visual no texto
        if self.text and self.font:
            color = self.hover_color if hovering else self.base_color
            self.text = self.font.render(self.text_input, True, color)
            self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

        # Hover visual na imagem
        if self.image and hovering != self.is_hovered:
            self.is_hovered = hovering
            if hovering:
                # aumenta imagem
                width = int(self.original_image.get_width() * self.hover_scale)
                height = int(self.original_image.get_height() * self.hover_scale)
                self.image = pygame.transform.scale(self.original_image, (width, height))
            else:
                # volta ao normal
                self.image = self.original_image

            self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def checkClick(self, position):
        if self.rect.collidepoint(position):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                return True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        return False
