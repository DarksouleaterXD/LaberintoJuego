import pygame
from menu import main_menu
from settings import WIDTH, HEIGHT
from game import start_game  # Asegúrate de importar correctamente start_game
import asyncio

async def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))#, pygame.FULLSCREEN)
    await main_menu(screen, start_game)  # Pasa ambos argumentos: screen y start_game

asyncio.run(main())
