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

    image1= pygame.image.load(f"./images/SELECT/1.png").convert_alpha()
    image2= pygame.image.load(f"./images/SELECT/2.png").convert_alpha()
    image3= pygame.image.load(f"./images/SELECT/3.png").convert_alpha()
    image4= pygame.image.load(f"./images/SELECT/4.png").convert_alpha()
    image5= pygame.image.load(f"./images/SELECT/5.png").convert_alpha()
    image6= pygame.image.load(f"./images/SELECT/6.png").convert_alpha()

    button_lvl1 = Button(start_x + 0 * (button_width + spacing), y, button_width, button_height, "1", (255,255,255), action=create_action(1), image=image1)
    button_lvl2 = Button(start_x + 1 * (button_width + spacing), y, button_width, button_height, "2", (255,255,255), action=create_action(2), image=image2)
    button_lvl3 = Button(start_x + 2 * (button_width + spacing), y, button_width, button_height, "3", (255,255,255), action=create_action(3), image=image3)
    button_lvl4 = Button(start_x + 3 * (button_width + spacing), y, button_width, button_height, "4", (255,255,255), action=create_action(4), image=image4)
    button_lvl5 = Button(start_x + 4 * (button_width + spacing), y, button_width, button_height, "5", (255,255,255), action=create_action(5), image=image5)
    button_lvl6 = Button(start_x + 5 * (button_width + spacing), y, button_width, button_height, "6", (255,255,255), action=create_action(6), image=image6)

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

def main_menu(screen, start_game_func):
    
    pygame.init()
    pygame.mixer.music.load("./images/nivel5.ogg")
    pygame.mixer.music.play()
    clock = pygame.time.Clock()
    pygame.display.set_caption("Menú - Laberinto")
    
    frames = []
    for i in range(300):
        frame = pygame.image.load(f"./images/menu/frame_{i:03d}_delay-0.1s.png").convert()
        frame = pygame.transform.scale(frame, (WIDTH, HEIGHT))
        frames.append(frame)
    background = pygame.image.load("./images/fondo.jpeg").convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    
    logo = pygame.image.load("images/logo.png").convert_alpha()
    
    # Cargamos directamente la imagen del título
    titulo_imagen = pygame.image.load("./images/titulo.png").convert_alpha()
    
     # Fuente personalizada
    font_path = "./images/Fuente_Titulo.otf"
  
    stats_font = pygame.font.Font(font_path, 40)   # Más pequeño para los stats (último tiempo, movimientos)
    
    # Redimensionar el título si es necesario
    # titulo_imagen = pygame.transform.scale(titulo_imagen, (nuevo_ancho, nuevo_alto))

    font = pygame.font.Font(None, 40)

    logo_y = 30
    title_y = logo_y + logo.get_height() + 20
    stats_y = title_y + 100  # subimos stats para dar espacio al título imagen
    buttons_y = stats_y + 100

    tiempo_frame = 100
    tiempo_acumulado = 0
    frame_actual = 0
    play_img = pygame.image.load("./images/MAIN/1.png").convert_alpha()
    select_img = pygame.image.load("./images/MAIN/2.png").convert_alpha()
    exit_img = pygame.image.load("./images/MAIN/3.png").convert_alpha()
    
    button_width, button_height = 150, 50
    play_button = Button(WIDTH // 2 - button_width // 2 - 7, buttons_y, button_width + 80, button_height, "Jugar", WHITE, action=lambda: start_game_func(screen, initial_level=1), image=play_img) 
    exit_button = Button(WIDTH // 2 - button_width // 2 - 7, buttons_y + 140, button_width + 80, button_height, "Salir", (200, 0, 0), exit_game, image=exit_img)
    select_level_button = Button(WIDTH // 2 - button_width // 2 - 7, buttons_y + 70, button_width + 80, button_height, "Seleccionar Nivel", WHITE, action=lambda: select_level_menu(screen, start_game_func), image=select_img)
    
    running = True
    while running:
        if tiempo_acumulado >= tiempo_frame:
            frame_actual = (frame_actual + 1) % len(frames)
            tiempo_acumulado = 0
            
        screen.blit(frames[frame_actual], (0, 0))
        last_time, last_moves = get_latest_stats()

        dt = clock.tick(60)
        tiempo_acumulado += dt
        
        screen.blit(logo, (WIDTH // 2 - logo.get_width() // 2, logo_y))
        
        # Mostrar la imagen del título
        screen.blit(titulo_imagen, (WIDTH // 2 - titulo_imagen.get_width() // 2, title_y))
        
        time_text = stats_font.render(f"Último tiempo: {last_time} seg", True, BLACK)
        moves_text = stats_font.render(f"Últimos movimientos: {last_moves}", True, BLACK)
        
        screen.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, stats_y))
        screen.blit(moves_text, (WIDTH // 2 - moves_text.get_width() // 2, stats_y + 40))

        play_button.draw(screen)
        select_level_button.draw(screen)
        exit_button.draw(screen)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            play_button.check_click(event)
            select_level_button.check_click(event)
            exit_button.check_click(event)

