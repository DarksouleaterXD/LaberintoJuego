import asyncio
import pygame
import sys
from settings import WIDTH, HEIGHT, WHITE, GRAY, BLACK
from ui import Button
from game import start_game

def exit_game():
    pygame.quit()
    sys.exit()

def get_latest_stats():
    try:
        with open("stats.txt", "r") as file:
            stats = file.read().splitlines()
        last_time = stats[0] if stats else "N/A"
        last_moves = stats[1] if len(stats) > 1 else "N/A"
    except FileNotFoundError:
        last_time, last_moves = "N/A", "N/A"
    return last_time, last_moves
def select_level_menu(screen, start_game_func):
    
    background = pygame.image.load("./images/fondo.jpeg").convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    pygame.font.init()
    font = pygame.font.Font(None, 36)

    # Coordenadas base
    spacing = 20
    button_width, button_height = 80, 50
    total_width = 6 * button_width + 5 * spacing
    start_x = WIDTH // 2 - total_width // 2
    y = HEIGHT // 2

    # Crear cada botón de nivel por separado
    def create_action(lvl):
        def start():
            print(f"Seleccionaste nivel {lvl}")  # Esto te mostrará si está funcionando
            start_game_func(screen, lvl)
        return start


    button_lvl1 = Button(start_x + 0 * (button_width + spacing), y, button_width, button_height, "1", (255,255,255), action=create_action(1))
    button_lvl2 = Button(start_x + 1 * (button_width + spacing), y, button_width, button_height, "2", (255,255,255), action=create_action(2))
    button_lvl3 = Button(start_x + 2 * (button_width + spacing), y, button_width, button_height, "3", (255,255,255), action=create_action(3))
    button_lvl4 = Button(start_x + 3 * (button_width + spacing), y, button_width, button_height, "4", (255,255,255), action=create_action(4))
    button_lvl5 = Button(start_x + 4 * (button_width + spacing), y, button_width, button_height, "5", (255,255,255), action=create_action(5))
    button_lvl6 = Button(start_x + 5 * (button_width + spacing), y, button_width, button_height, "6", (255,255,255), action=create_action(6))

    buttons = [button_lvl1, button_lvl2, button_lvl3, button_lvl4, button_lvl5, button_lvl6]

    selecting = True
    while selecting:
        screen.blit(background, (0, 0))
        title = font.render("Selecciona un nivel", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))

        for button in buttons:
            button.draw(screen)
            #pygame.draw.rect(screen, (255,255,255), pygame.Rect(300, 300, 300, 300), border_radius=10)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            for button in buttons:
                button.check_click(event)

async def main_menu(screen, start_game_func):
    pygame.init()
    pygame.mixer.music.load("./images/nivel5.ogg")
    pygame.mixer.music.play()
    clock = pygame.time.Clock()
    pygame.display.set_caption("Menú - Laberinto")

    current_frame = 0

    def load_frame(n):
        frame = pygame.image.load(f"./images/menu/frame_{n:03d}_delay-0.1s.png").convert()
        return pygame.transform.scale(frame, (WIDTH, HEIGHT))

    current_frame_surface = load_frame(current_frame)


    logo = pygame.image.load("images/logo.png").convert_alpha()
    titulo_imagen = pygame.image.load("./images/titulo.png").convert_alpha()
    font_path = "./images/Fuente_Titulo.otf"
    stats_font = pygame.font.Font(font_path, 40)
    font = pygame.font.Font(None, 40)

    logo_y = 30
    title_y = logo_y + logo.get_height() + 20
    stats_y = title_y + 100
    buttons_y = stats_y + 100

    tiempo_frame = 100
    tiempo_acumulado = 0
    frame_actual = 0

    button_width, button_height = 150, 50

    # No ponemos lambda, sino un identificador de acción
    play_button = Button(WIDTH // 2 - button_width // 2 - 7, buttons_y, button_width + 80, button_height, "Jugar", WHITE, action="play")
    select_level_button = Button(WIDTH // 2 - button_width // 2 - 7, buttons_y + 70, button_width + 80, button_height, "Seleccionar Nivel", WHITE, action="select_level")
    exit_button = Button(WIDTH // 2 - button_width // 2 - 7, buttons_y + 140, button_width + 80, button_height, "Salir", (200, 0, 0), action="exit")

    running = True
    selected_action = None

    selected_option = 0
    options = ["Continuar", "Seleccionar Nivel", "Salir"]
    
    while running:
        if tiempo_acumulado >= tiempo_frame:
            frame_actual = (frame_actual + 1) % len(frames)
            tiempo_acumulado = 0
            
        last_time, last_moves = get_latest_stats()

        dt = clock.tick(60)
        tiempo_acumulado += dt

        # En tu bucle:
        if tiempo_acumulado >= tiempo_frame:
            current_frame = (current_frame + 1) % 300
            current_frame_surface = load_frame(current_frame)
            tiempo_acumulado = 0

        screen.blit(current_frame_surface, (0, 0))
    
        screen.blit(logo, (WIDTH // 2 - logo.get_width() // 2, logo_y))
        screen.blit(titulo_imagen, (WIDTH // 2 - titulo_imagen.get_width() // 2, title_y))

        time_text = stats_font.render(f"Último tiempo: {last_time} seg", True, BLACK)
        moves_text = stats_font.render(f"Últimos movimientos: {last_moves}", True, BLACK)

        screen.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, stats_y))
        screen.blit(moves_text, (WIDTH // 2 - moves_text.get_width() // 2, stats_y + 40))

        #play_button.draw(screen)
        #select_level_button.draw(screen)
        #exit_button.draw(screen)

        
        
        small_font = pygame.font.Font(None, 40)

        for i, option in enumerate(options):
            color = (255, 255, 0) if i == selected_option else (255, 255, 255)
            text = small_font.render(option, True, color)
            screen.blit(text, text.get_rect(center=(WIDTH//2, HEIGHT//2 + i * 60 + 100)))
            
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if(selected_option==0): return await start_game_func(screen, initial_level=1)
                    elif(selected_option==1): return await select_level_menu(screen, start_game_func)
                    elif(selected_option==2): return exit_game()
                
            if play_button.check_click(event):
                selected_action = "play"
                running = False
            if select_level_button.check_click(event):
                selected_action = "select_level"
                running = False
            if exit_button.check_click(event):
                selected_action = "exit"
                running = False
        
        await asyncio.sleep(0)

    # Cuando el menú termina, hacemos la acción correspondiente
    if selected_action == "play":
        await start_game_func(screen, initial_level=1)
    elif selected_action == "select_level":
        await select_level_menu(screen, start_game_func)
    elif selected_action == "exit":
        exit_game()


