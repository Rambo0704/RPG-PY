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

def mostrar_tela_final(screen, mensagem_final, cor_fundo, font_grande):
    largura_tela, altura_tela = screen.get_size()
    screen.fill(cor_fundo)
    texto = font_grande.render(mensagem_final, True, WHITE)
    texto_rect = texto.get_rect(center=(largura_tela // 2, altura_tela // 2))
    screen.blit(texto, texto_rect)
    pygame.display.flip()
    pygame.time.delay(3000)