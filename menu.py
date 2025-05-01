import asyncio
import pygame
import sys
from settings import WIDTH, HEIGHT, WHITE, GRAY, BLACK
from ui import Button
from game import start_game, BotonTouch

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
async def select_level_menu(screen, start_game_func):
    background = pygame.image.load("./images/fondo.jpeg").convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    pygame.font.init()
    font = pygame.font.Font(None, 36)
    logo = pygame.image.load("images/select-level.png").convert_alpha()
    
    spacing = 20
    button_width, button_height = 80, 50
    total_width = 6 * button_width + 6 * spacing
    start_x = WIDTH // 2 - total_width // 2
    y = HEIGHT // 2

    def create_action(lvl):
        def start():
            print(f"Seleccionaste nivel {lvl}")
            start_game_func(screen, lvl)
        return start

    
    buttons = [
    Button(
        start_x + i * (button_width + spacing),
        y,
        button_width,
        button_height,
        action=create_action(i + 1),
        image=pygame.transform.scale(
            pygame.image.load(f"./images/SELECT/{i + 1}.png").convert_alpha(),
            (button_width, button_height)
        )
    )
    for i in range(6)
    ]

    return_to_menu_button = Button(
        start_x + 6 * (button_width + spacing), y, button_width, button_height,
        image=pygame.transform.scale(
            pygame.image.load(f"./images/SELECT/your_text.png").convert_alpha(),
            (button_width, button_height)
        )
    )
    buttons.append(return_to_menu_button)
    
    selected_option = 0

    # Funciones para botones táctiles
    def option_left():
        nonlocal selected_option
        selected_option = (selected_option - 1) % len(buttons)

    def option_right():
        nonlocal selected_option
        selected_option = (selected_option + 1) % len(buttons)

    def option_select():
        nonlocal selected_option
        enter_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
        pygame.event.post(enter_event)

    # Crear botones táctiles: IZQUIERDA - OK - DERECHA
    btn_size = 80
    btn_y = y + button_height + 60
    btn_left = pygame.Rect(WIDTH // 2 - btn_size*2, btn_y, btn_size, btn_size)
    btn_ok = pygame.Rect(WIDTH // 2 - btn_size // 2, btn_y, btn_size, btn_size)
    btn_right = pygame.Rect(WIDTH // 2 + btn_size, btn_y, btn_size, btn_size)

    botones_touch = [
        BotonTouch(btn_left, option_left, color=(200, 200, 0), hover_color=(255, 255, 0), text="<"),
        BotonTouch(btn_ok, option_select, color=(200, 255, 200), hover_color=(255, 255, 255), text="OK"),
        BotonTouch(btn_right, option_right, color=(200, 200, 0), hover_color=(255, 255, 0), text=">")
    ]

    selecting = True
    while selecting:
        screen.blit(background, (0, 0))
        screen.blit(logo, (WIDTH // 2 - logo.get_width() // 2, HEIGHT // 3))

        # Dibujar botones de nivel
        for i, button in enumerate(buttons):
            if i == selected_option:
                pygame.draw.rect(screen, (255, 255, 0), button.rect.inflate(10, 10), 3)
            button.draw(screen)

        # Dibujar botones táctiles
        for boton in botones_touch:
            boton.draw(screen)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected_option = (selected_option - 1) % len(buttons)
                elif event.key == pygame.K_RIGHT:
                    selected_option = (selected_option + 1) % len(buttons)
                elif event.key == pygame.K_RETURN:
                    
                    if selected_option == 0:
                        return await start_game_func(screen, initial_level=1)
                    elif selected_option == 1:
                        return await start_game_func(screen, 2)
                    elif selected_option == 2:
                        return await start_game_func(screen, 3)
                    
                    elif selected_option == 3:
                        return await start_game_func(screen, 4)
                    elif selected_option == 4:
                        return await start_game_func(screen, 5)
                    elif selected_option == 5:
                        return await start_game_func(screen, 6)
                    elif selected_option == 6:
                        return await main_menu(screen, start_game_func)
                    
                        
            for button in buttons:
                button.check_click(event)
            if event.type in (pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN):
                pos = event.pos if event.type == pygame.MOUSEBUTTONDOWN else (event.x * WIDTH, event.y * HEIGHT)
                for boton in botones_touch:
                    if boton.rect.collidepoint(pos):
                        boton.action()
        await asyncio.sleep(0)

    

async def main_menu(screen, start_game_func):
    pygame.init()

    pygame.mixer.music.load("./images/nivel5.ogg")
    pygame.mixer.music.play()
    clock = pygame.time.Clock()
    pygame.display.set_caption("Menú - Laberinto")
    icon_up = pygame.transform.scale(
    pygame.image.load("./images/flecha-arriba.png").convert_alpha(), (80, 80)
    )
    icon_down = pygame.transform.scale(
    pygame.image.load("./images/flecha-abajo.png").convert_alpha(), (80, 80)
    )
    icon_ok = pygame.transform.scale(
    pygame.image.load("./images/ok_button.png").convert_alpha(), (80, 80)
    )


    current_frame = 0
    selected_option = 0
    def option_up():
        nonlocal selected_option
        selected_option = (selected_option - 1) % len(options)
    def option_down():
        nonlocal selected_option
        selected_option = (selected_option + 1) % len(options)
    def select_option():
        nonlocal selected_option
        enter_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
        pygame.event.post(enter_event)
        
    botones_touch = []
    # Definir los botones en la izquierda ahora:
    btn_up = pygame.Rect(150, HEIGHT - 300, 80, 80)
    btn_down = pygame.Rect(150, HEIGHT - 100, 80, 80)
    btn_accept = pygame.Rect(150, HEIGHT - 200, 80, 80) 
    botones_touch = [
            BotonTouch(btn_up, lambda: option_up(), image=icon_up),
            BotonTouch(btn_down, lambda: option_down(), image=icon_down),
            BotonTouch(btn_accept, lambda: select_option(), image=icon_ok),
    ]
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
    
    spacing = 20
    button_width, button_height = 200, 50
    total_width = 6 * button_width + 6 * spacing
    start_x = WIDTH // 2 - button_width // 2
    y = HEIGHT // 2 + 30
    
    buttons = [
        
    Button(
        start_x,
        y + 1 * (button_height + spacing),
        button_width,
        button_height,
        image=pygame.transform.scale(
            pygame.image.load(f"./images/MAIN/1.png").convert_alpha(),
            (button_width, button_height)
        )
    ),
    Button(
        WIDTH // 2 - (button_width + 150) // 2,
        y + 2 * (button_height + spacing),
        button_width + 150,
        button_height,
        image=pygame.transform.scale(
            pygame.image.load(f"./images/MAIN/2.png").convert_alpha(),
            (button_width + 150, button_height)
        )
    ),
    Button(
        start_x,
        y + 3 * (button_height + spacing),
        button_width,
        button_height,
        image=pygame.transform.scale(
            pygame.image.load(f"./images/MAIN/3.png").convert_alpha(),
            (button_width, button_height)
        )
    ),
    
    
    ]
    
    while running:
        '''if tiempo_acumulado >= tiempo_frame:
            frame_actual = (frame_actual + 1) % len(frames)
            tiempo_acumulado = 0'''
            
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
        
        for boton in botones_touch:
            boton.draw(screen)    
            
        # Dibujar botones de nivel
        for i, button in enumerate(buttons):
            if i == selected_option:
                pygame.draw.rect(screen, (255, 255, 0), button.rect.inflate(10, 10), 3)
            button.draw(screen)
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
            elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN):
                pos = None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos  # (x, y) del click
                elif event.type == pygame.FINGERDOWN:
                    pos = (event.x * WIDTH, event.y * HEIGHT)  # Normalizado (0-1) en FINGERDOWN

                
                if pos and botones_touch:
                    for boton in botones_touch:
                        if boton.rect.collidepoint(pos):
                            boton.action()    
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


