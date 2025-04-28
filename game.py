import pygame
import time
import random
from maze import generate_maze, move_walls_dynamically
from settings import WIDTH, HEIGHT, WHITE, BLACK, LEVELS
import asyncio

music_on = True
# Clases integradas directamente aquí

class Player:
    def __init__(self, tile_size):
        self.tile_size = tile_size
        self.x = 1
        self.y = 1
        self.rect = pygame.Rect(self.x * tile_size, self.y * tile_size, tile_size, tile_size)
        self.start_time = time.time()
        self.moves = 0
        self.vidas= 3
        self.historial = []
        self.frames = []
        for i in range(9):  # Asumiendo 17 frames del 0 al 16
            ruta = f"./images/player/frame_{i}_delay-0.1s.png"
            imagen = pygame.image.load(ruta).convert_alpha()
            imagen = pygame.transform.scale(imagen, (tile_size, tile_size))
            self.frames.append(imagen)

        

    def move(self, dx, dy, maze):
        if 0 <= self.x + dx < len(maze[0]) and 0 <= self.y + dy < len(maze):
            if maze[self.y + dy][self.x + dx] == 0:
                self.historial.append((self.x, self.y))
                self.x += dx
                self.y += dy
                self.rect.topleft = (self.x * self.tile_size, self.y * self.tile_size)
                self.moves += 1
    def reset(self):  
        self.x = 1
        self.y = 1
        self.rect.topleft = (self.x * self.tile_size, self.y * self.tile_size)
   
    def retroceder_camino(self, screen, maze, level):
            # Copiamos el historial para no modificarlo mientras retrocedemos
            screen.fill((0, 0, 0))
            #camino = list(reversed(self.historial))

            for pos in reversed(self.historial):
                # Actualizamos la posición del jugador
                self.x, self.y = pos
                self.rect.topleft = (self.x * self.tile_size, self.y * self.tile_size)
                
                # Limpiamos la pantalla antes de dibujar (opcional, si ves parpadeo feo)
                screen.fill((0, 0, 0))
                
                # Redibujamos todo: laberinto y jugador
                draw_maze(screen, maze, self.tile_size,level)
                self.draw(screen)
                
                # Actualizamos la pantalla
                pygame.display.update()
                
                # Pequeña pausa para dar efecto de "caminar hacia atrás"
                pygame.time.delay(50)

            # Limpiamos el historial al terminar el retroceso
            self.historial.clear()    


    def draw(self, screen, frame=0):
        screen.blit(self.frames[frame], self.rect)

class Monster:
    def __init__(self, maze, tile_size, speed, level,player):
        self.tile_size = tile_size
        self.maze = maze
        self.speed = speed
        self.level = level
        self.player=player
        self.x, self.y = self.random_position()
        self.rect = pygame.Rect(self.x * tile_size, self.y * tile_size, tile_size, tile_size)
        self.last_move_time = pygame.time.get_ticks()
        self.frames = []
        for i in range(17):  # Asumiendo 17 frames del 0 al 16
            ruta = f"./images/monster/frame_{i:02d}_delay-0.1s.png"
            imagen = pygame.image.load(ruta).convert_alpha()
            imagen = pygame.transform.scale(imagen, (tile_size, tile_size))
            self.frames.append(imagen)

    def random_position(self):
        while True:
            x = random.randint(1, len(self.maze[0]) - 2)
            y = random.randint(1, len(self.maze) - 2)
            if self.maze[y][x] == 0:
                distance = abs(x - self.player.x) + abs(y - self.player.y)
                if distance >= 10:  # ← Distancia mínima en tiles
                    return x, y

    def move(self, maze, player=None, level=1): 
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time < self.speed:
            return

        dx, dy = 0, 0

        # Definir radio de detección
        distancia_maxima = 5  # en tiles

        if player and level > 3:
            distancia = abs(player.x - self.x) + abs(player.y - self.y)  # Manhattan
            if distancia <= distancia_maxima:
                # Seguir al jugador si está cerca
                if player.x < self.x:
                    dx = -1
                elif player.x > self.x:
                    dx = 1
                if player.y < self.y:
                    dy = -1
                elif player.y > self.y:
                    dy = 1
            else:
                # Si está lejos, moverse aleatoriamente
                direction = random.choice([(0,1), (1,0), (0,-1), (-1,0)])
                dx, dy = direction
        else:
            # Niveles bajos = movimiento aleatorio
            direction = random.choice([(0,1), (1,0), (0,-1), (-1,0)])
            dx, dy = direction

        # Validar que no se salga del laberinto y que pueda moverse a esa celda
        if 0 <= self.x + dx < len(maze[0]) and 0 <= self.y + dy < len(maze):
            if maze[self.y + dy][self.x + dx] == 0:
                self.x += dx
                self.y += dy
                self.rect.topleft = (self.x * self.tile_size, self.y * self.tile_size)

        self.last_move_time = current_time

    def draw(self, screen, frame=0):
        screen.blit(self.frames[frame],self.rect)
class Corazon:
    def __init__(self, maze, tile_size, level,player):
        self.tile_size = tile_size
        self.maze = maze
        self.level = level
        self.player=player
        self.x, self.y = self.random_position()
        self.rect = pygame.Rect(self.x * tile_size, self.y * tile_size, tile_size, tile_size)
        self.last_move_time = pygame.time.get_ticks()
        self.frames = []
        for i in range(9):  # Asumiendo 17 frames del 0 al 16
            ruta = f"./images/corazon/frame_{i}_delay-0.17s.png"
            imagen = pygame.image.load(ruta).convert_alpha()
            imagen = pygame.transform.scale(imagen, (tile_size, tile_size))
            self.frames.append(imagen)

    def random_position(self):
        while True:
            x = random.randint(1, len(self.maze[0]) - 2)
            y = random.randint(1, len(self.maze) - 2)
            if self.maze[y][x] == 0:
                distance = abs(x - self.player.x) + abs(y - self.player.y)
                if distance >= 10:  # ← Distancia mínima en tiles
                    return x, y

    def draw(self, screen, frame=0):
        screen.blit(self.frames[frame],self.rect)
    
class Huella:
    def __init__(self, pos, duracion=2000):
        self.pos = pos
        self.duracion = duracion  # tiempo en milisegundos
        self.tiempo_restante = duracion

    def actualizar(self, dt):
        self.tiempo_restante -= dt
        if self.tiempo_restante <= 0:
            self.tiempo_restante = 0  # Asegura que no sea negativo
    def draw(self, screen, imagen):
        screen.blit(imagen, (self.pos[0] - imagen.get_width()//2, self.pos[1] - imagen.get_height()//2))             

# Funciones de visualización y eventos

def draw_maze(screen, maze, tile_size,level):
    floor_path = f"./images/suelo{level}.png"
    wall_path = f"./images/piedra{level}.png"
    
    try:
        floor_img = pygame.image.load(floor_path)
    except:
        floor_img = pygame.image.load("./images/suelo1.png")

    try:
        wall_img = pygame.image.load(wall_path)
    except:
        wall_img = pygame.image.load("./images/piedra.png")
    
    
    floor_img = pygame.transform.scale(floor_img, (tile_size, tile_size))
    wall_img = pygame.transform.scale(wall_img, (tile_size, tile_size))
    for y, row in enumerate(maze):
        for x, tile in enumerate(row):
            if tile == 0:
                screen.blit(floor_img, (x * tile_size, y * tile_size))
            else:
                screen.blit(wall_img, (x * tile_size, y * tile_size))

def mostrar_explosion(screen, x, y, explosion_frames):
    """Muestra una animación de explosión en (x, y)."""
    for frame in explosion_frames:
        screen.fill((0, 0, 0))  # Limpiar la pantalla a negro
        screen.blit(frame, (x, y))
        pygame.display.update()
        pygame.time.delay(50)  # Velocidad de animación

def show_pause_menu(screen):
    font = pygame.font.Font(None, 60)
    small_font = pygame.font.Font(None, 40)
    clock = pygame.time.Clock()
    
    selected_option = 0
    options = ["Continuar", "Volver al Menú Principal"]

    while True:
        screen.fill((30, 30, 30))

        # Título
        title = font.render("Juego en Pausa", True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=(WIDTH//2, HEIGHT//4)))

        # Opciones
        for i, option in enumerate(options):
            color = (255, 255, 0) if i == selected_option else (255, 255, 255)
            text = small_font.render(option, True, color)
            screen.blit(text, text.get_rect(center=(WIDTH//2, HEIGHT//2 + i * 60)))
        
        pygame.display.flip()
        from menu import main_menu
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if(selected_option==1):
                        return main_menu(screen, start_game)
                    return
        clock.tick(30)


def handle_game_events(player, maze,screen,huellas):
    global music_on
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            prev_pos = (player.rect.centerx, player.rect.centery)
            if event.key == pygame.K_LEFT: player.move(-1, 0, maze)
            if event.key == pygame.K_RIGHT: player.move(1, 0, maze)
            if event.key == pygame.K_UP: player.move(0, -1, maze)
            if event.key == pygame.K_DOWN: player.move(0, 1, maze)
            moved = True
            if moved:
                huellas.append(Huella(prev_pos))
            if event.key == pygame.K_p: show_pause_menu(screen)
            if event.key == pygame.K_m: 
                if music_on:
                    pygame.mixer.music.pause()
                    music_on = False
                else:
                    pygame.mixer.music.unpause()
                    music_on = True
            elif event.key == pygame.K_g:  # 👈 Truco para ganar el nivel
                return "WIN"
    return True
def render_multiline_text(text, font, color, max_width):
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    lines.append(current_line.strip())
    return lines
# Game Over, transición y pantallas de victoria/derrota
import asyncio

async def show_comic(screen, level):
    comic_texts = {
        1: "Despertás sin recuerdos. Sin un mapa. Solo sabés una cosa… tenés que salir. Pero, ¿qué acecha en las sombras?",
        2: "Cada paso deja huella. Pero no todas las huellas llevan a un final. Algunas solo te devuelven al principio… y otras, te llevan a lo desconocido",
        3: "¿Ya pasé por acá… o es solo mi mente que me traiciona? Algo me observa…",
        4: "Ahora, el laberinto no solo te encierra. Te corre. Cada segundo cuenta, y el eco de tus latidos se convierte en un grito ensordecedor",
        5: "En la penumbra… hay rutas que no todos pueden ver. Este nivel no es para cualquiera. ¿Te atreverás a desentrañar sus secretos?",
        6: "Lo lograste. Pero… ¿qué sacrificaste en el camino? Cada decisión tiene un precio."
    }
    path = f"./images/Viñeta-{level}.png"
    comic_img = pygame.image.load(path).convert()
    pygame.mixer.music.load(f"./images/nivel{level}.ogg")
    pygame.mixer.music.play(-1)

    img_width, img_height = comic_img.get_size()
    screen_ratio = WIDTH / HEIGHT
    img_ratio = img_width / img_height

    if img_ratio > screen_ratio:
        scale_width = WIDTH
        scale_height = int(WIDTH / img_ratio)
    else:
        scale_height = HEIGHT
        scale_width = int(HEIGHT * img_ratio)

    comic_scaled = pygame.transform.smoothscale(comic_img, (scale_width, scale_height))
    x_offset = (WIDTH - scale_width) // 2
    y_offset = (HEIGHT - scale_height) // 2

    black_overlay = pygame.Surface((WIDTH, HEIGHT))
    black_overlay.fill((0, 0, 0))

    font = pygame.font.Font(None, 28)
    text_color = (255, 255, 255)
    narrative = comic_texts.get(level, "")
    lines = render_multiline_text(narrative, font, text_color, WIDTH - 80)

    # Fade in
    for alpha in range(255, -1, -15):
        screen.fill((0, 0, 0))
        screen.blit(comic_scaled, (x_offset, y_offset))
        black_overlay.set_alpha(alpha)
        screen.blit(black_overlay, (0, 0))

        text_bg = pygame.Surface((WIDTH, 100))
        text_bg.fill((0, 0, 0))
        text_bg.set_alpha(200)
        screen.blit(text_bg, (0, HEIGHT - 110))

        for i, line in enumerate(lines):
            rendered = font.render(line, True, text_color)
            screen.blit(rendered, (WIDTH // 2 - rendered.get_width() // 2, HEIGHT - 100 + i * 25))

        pygame.display.flip()
        await asyncio.sleep(0.03)  # 30 ms, reemplaza pygame.time.delay(300)

    # Mostrar imagen final unos segundos
    pygame.display.flip()
    await asyncio.sleep(4)  # 4000 ms = 4 segundos


async def transition_screen(screen, level):#si se usa
    background = pygame.image.load("./images/carga.jpg").convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    font = pygame.font.Font(None, 60)
    text = font.render(f"CARGANDO NIVEL {level }...", True, WHITE)
    screen.blit(background, (0, 0))
    #screen.fill(WHITE)#cambio
    screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
    pygame.display.flip()
    pygame.time.delay(500)
    await show_comic(screen,level)

def wait_for_key():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                return

def wait_for_restart():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    start_game()
                    return
                elif event.key == pygame.K_ESCAPE:
                    return

def draw_lives(screen, player,heart_img,width):
    font = pygame.font.SysFont(None, 30)
    text = font.render(f"x {player.vidas}", True, WHITE)
    screen.blit(heart_img, (width-30, 10))
    screen.blit(text, (width, 12))

def show_win_screen(screen, time_taken, moves):
    
    pygame.mixer.music.load("./win_sound.wav")
    pygame.mixer.music.play()
    
    with open("stats.txt", "w") as file:
        file.write(f"{round(time_taken, 2)}\n{moves}")
    background = pygame.image.load("./images/Fondo-final-verdadero.jpg").convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    
    font_big = pygame.font.Font(None, 60)
    font_small = pygame.font.Font(None, 40)
    screen.blit(background, (0, 0))
    text1 = font_big.render("¡Ganaste!", True, WHITE)
    text2 = font_small.render("Presiona una tecla para continuar", True, WHITE)
    screen.blit(text1, (WIDTH//2 - text1.get_width()//2, HEIGHT//3))
    screen.blit(text2, (WIDTH//2 - text2.get_width()//2, HEIGHT//2))
    pygame.display.flip()
    wait_for_key()
    
    pygame.mixer.music.stop()
    
    from menu import main_menu
    screen = pygame.display.set_mode((WIDTH, HEIGHT))#, pygame.FULLSCREEN)
    main_menu(screen, start_game)

def show_loss_screen(screen, time_taken, moves):#se usa 
    
    with open("stats.txt", "w") as file:
        file.write(f"{round(time_taken, 2)}\n{moves}")
        
    pygame.mixer.music.load("lose_sound.wav")
    pygame.mixer.music.play()
    font = pygame.font.Font(None, 50)
    screen.fill((200, 0, 0))
    text1 = font.render("¡Has sido atrapado!", True, WHITE)
    text2 = font.render("Presiona cualquier tecla para volver", True, WHITE)
    screen.blit(text1, (WIDTH//2 - text1.get_width()//2, HEIGHT//3))
    screen.blit(text2, (WIDTH//2 - text2.get_width()//2, HEIGHT//2))
    pygame.display.flip()
    wait_for_key()
    from menu import main_menu
    screen = pygame.display.set_mode((WIDTH, HEIGHT))#, pygame.FULLSCREEN)
    main_menu(screen, start_game)  # Pasa ambos argumentos: screen y start_game

'''def draw_level_indicator(screen, level):
    
    from settings import BLACK
    font = pygame.font.Font(None, 36)
    text = font.render(f"Nivel {level}", True, BLACK)
    screen.blit(text, (10, 10))'''


# Juego principal

async def start_game(screen,initial_level=1):
    
    
    
    "./images/player/frame_{i}_delay-0.1s.png"
    explosion_frames = []
    for i in range(9):  # Cambia NUMERO_FRAMES por el número correcto
        frame = pygame.image.load(f"./images/explosion/frame_{i:02d}_delay-0.08s.png").convert_alpha()
        frame = pygame.transform.scale(frame, (80, 80))  # Ajusta tamaño si quieres
        explosion_frames.append(frame)
    huellas = []
    level = initial_level
    screen = pygame.display.set_mode((WIDTH, HEIGHT))#, pygame.FULLSCREEN)
    pygame.display.set_caption("Laberinto")
    clock = pygame.time.Clock()
    player_start_time = time.time()
    efecto_hurt = pygame.mixer.Sound("./images/hurt.ogg")
    win_sound = pygame.mixer.Sound("./win_sound.wav")
    
    while level <= LEVELS:
        desired_rows = 21 + level * 2
        desired_cols = 35 + level * 2
        
        tile_size = min(WIDTH // desired_cols, HEIGHT // desired_rows)
        rows = HEIGHT // tile_size
        cols = WIDTH // tile_size

        # 🖼️ Cargar y escalar imágenes
        goal_img = pygame.image.load("./images/meta.png")
        goal_img = pygame.transform.scale(goal_img, (tile_size, tile_size))
        
        floors = {
            1: pygame.image.load("./images/suelo1.png"),
            2: pygame.image.load("./images/suelo2.png"),
            3: pygame.image.load("./images/suelo3.png"),
            4: pygame.image.load("./images/suelo4.png"),
            5: pygame.image.load("./images/suelo5.png"),
            6: pygame.image.load("./images/suelo6.png"),
        }
        walls = {
            1: pygame.image.load("./images/piedra.png"),
            2: pygame.image.load("./images/piedra2.png"),  # si tenés otra imagen de pared para niveles superiores
            3: pygame.image.load("./images/piedra3.png"),
            4: pygame.image.load("./images/piedra4.png"),
            5: pygame.image.load("./images/piedra5.png"),
            6: pygame.image.load("./images/piedra6.png"),
        }
        
        floor_img = floors.get(level, floors[1])
        wall_img = walls.get(level, walls[1])
        floor_img = pygame.transform.scale(floor_img, (tile_size, tile_size))
        wall_img = pygame.transform.scale(wall_img, (tile_size, tile_size))
              
        heart_img = pygame.image.load("./images/corazon.png")
        heart_img = pygame.transform.scale(heart_img, (tile_size, tile_size))
        imagen_huella = pygame.image.load("./images/huellas.png")
        imagen_huella = pygame.transform.scale(imagen_huella, (tile_size/2, tile_size/2))
        
        # Cargar sonido de comer corazón
        eat_heart_sound = pygame.mixer.Sound("./images/corazon/corazon-comido.wav")
        
        
        
        
        maze = generate_maze(rows, cols)
        player = Player(tile_size)
        monsters = [Monster(maze["grid"], tile_size, 800 - level * 100, level,player) for _ in range(6 + level * 2)]
        corazones = [Corazon(maze["grid"], tile_size, level,player) for _ in range(6 + level * 2)]
        goal = pygame.Rect((cols - 2) * tile_size, (rows - 2) * tile_size, tile_size, tile_size)

        await transition_screen(screen, level)
        
        tiempo_frame = 100  # milisegundos entre frames (0.1s)
        tiempo_acumulado = 0
        frame_actual_player = 0
        frame_actual_monster = 0
        
        running = True
        last_wall_move_time = pygame.time.get_ticks()

        while running:
            event_result = handle_game_events(player, maze["grid"], screen,huellas)
            if event_result == "WIN":
                level += 1
                break
            running = event_result
            
            
            # Control de animacion
            if tiempo_acumulado >= tiempo_frame:
                frame_actual_monster = (frame_actual_monster + 1) % len(monsters[0].frames)
                frame_actual_player = (frame_actual_player + 1) % len(player.frames)
                tiempo_acumulado = 0

            for corazon in corazones:
                if player.rect.colliderect(corazon.rect):
                    print(player.vidas)                    
                    player.vidas+=1
                    eat_heart_sound.play()
                    corazones.remove(corazon)

            for monster in monsters:
                monster.move(maze["grid"], player, level)
                if player.rect.colliderect(monster.rect):
                    efecto_hurt.play()
                    if(player.vidas>0):
                        #player.reset()
                        mostrar_explosion(screen, player.rect.centerx - 40, player.rect.centery - 40, explosion_frames)
                        player.retroceder_camino(screen, maze,level)
                        player.vidas-=1
                    else:
                        show_loss_screen(screen, time.time() - player_start_time, player.moves)
                        return

            if player.rect.colliderect(goal):
                win_sound.play()
                level += 1
                break

            screen.fill(WHITE)
             #parte que se muestran las huellas
            for huella in huellas[:]:
                huella.actualizar(dt)
            
            huellas = [h for h in huellas if h.tiempo_restante > 0]
            
            
            for y, row in enumerate(maze["grid"]):
                for x, tile in enumerate(row):
                    if tile == 0:
                        if random.randint(0,2)==1:
                            screen.blit(floor_img, (x * tile_size, y * tile_size))
                        else:
                            screen.blit(floor_img, (x * tile_size, y * tile_size))
                            
                    else:
                        screen.blit(wall_img, (x * tile_size, y * tile_size))

            screen.blit(goal_img, goal.topleft)
            
            huellas.append(Huella(player.rect.center))
            for huella in huellas:
                 huella.draw(screen, imagen_huella)
            
            
            
            player.draw(screen, frame_actual_player)
            for monster in monsters:
                monster.draw(screen, frame_actual_monster)
           # draw_level_indicator(screen, level)
            
            for corazon in corazones:
                corazon.draw(screen, frame_actual_player)
            
            draw_lives(screen, player,heart_img,1220)
            pygame.display.flip()

            current_time = pygame.time.get_ticks()
            if level >= 3 and current_time - last_wall_move_time > 1750:
                move_walls_dynamically(maze["grid"], player)
                last_wall_move_time = current_time

            dt = clock.tick(60)
            tiempo_acumulado += dt
            await asyncio.sleep(0)

    time_taken = round(time.time() - player_start_time, 2)
    show_win_screen(screen, time_taken, player.moves)
def draw_sound_button(screen, rect, muted, sound_on_img, sound_off_img):
    screen.blit(sound_off_img if muted else sound_on_img, rect.topleft)