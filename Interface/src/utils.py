import pygame

def iniciar_musica(caminho_musica, volume=0.5):
    if not caminho_musica:
        print("Aviso: Nenhum caminho de música fornecido.")
        return
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(caminho_musica)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1) 
    except pygame.error as e:
        print(f"Erro ao carregar ou tocar a música: {caminho_musica}")
        print(e)