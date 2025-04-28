import pygame
from menu import main_menu
from settings import WIDTH, HEIGHT
from game import start_game  # Asegúrate de importar correctamente start_game

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))#, pygame.FULLSCREEN)
    main_menu(screen, start_game)  # Pasa ambos argumentos: screen y start_game

if __name__ == "__main__":
    main()
