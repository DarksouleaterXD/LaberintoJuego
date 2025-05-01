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
    
    
    botones_touch = []
    # Definir los botones en la izquierda ahora:
    btn_up = pygame.Rect(150, HEIGHT - 300, 80, 80)
    btn_down = pygame.Rect(150, HEIGHT - 100, 80, 80)
    btn_left = pygame.Rect(50, HEIGHT - 200, 80, 80)
    btn_right = pygame.Rect(250, HEIGHT - 200, 80, 80)
    btn_accept = pygame.Rect(150, HEIGHT - 200, 80, 80) 
     #ig:amarillocors
 
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
        
                # 🎯 CREAR Botones touch ligados al jugador
        
        
        
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
        
        botones_touch = [
            BotonTouch(btn_up, lambda: player.move( 0, -1, maze["grid"] )),
            BotonTouch(btn_down, lambda: player.move(0, 1, maze["grid"])),
            BotonTouch(btn_left, lambda: player.move(-1, 0, maze["grid"])),
            BotonTouch(btn_right, lambda: player.move(1, 0, maze["grid"])),
            BotonTouch(btn_accept, lambda: print("OK"), color=(200, 200, 0), hover_color=(255, 255, 0), text="OK")
        ]
        while running:
            event_result =await handle_game_events(player, maze["grid"], screen,huellas,botones_touch)
            if event_result == "WIN":
                level += 1
                break
            running = event_result
           

            #botones dibujos
            pygame.draw.rect(screen, (0, 200, 0), btn_up)
            pygame.draw.rect(screen, (0, 200, 0), btn_down)
            pygame.draw.rect(screen, (0, 200, 0), btn_left)
            pygame.draw.rect(screen, (0, 200, 0), btn_right)
            pygame.draw.rect(screen, (200, 200, 0), btn_accept)

       

            
            
            
            
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
                        await mostrar_explosion(screen, player.rect.centerx - 40, player.rect.centery - 40, explosion_frames)
                        await player.retroceder_camino(screen, maze,level)
                        player.vidas-=1
                    else:
                        await show_loss_screen(screen, time.time() - player_start_time, player.moves)
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
           
                
            for boton in botones_touch:
                boton.draw(screen)
            
            
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
    await show_win_screen(screen, time_taken, player.moves)
    
async def handle_game_events(player, maze, screen, huellas, botones_touch=None):
    global music_on
    moved = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        elif event.type == pygame.KEYDOWN:
            prev_pos = (player.rect.centerx, player.rect.centery)
            if event.key == pygame.K_LEFT:
                player.move(-1, 0, maze)
                moved = True
            if event.key == pygame.K_RIGHT:
                player.move(1, 0, maze)
                moved = True
            if event.key == pygame.K_UP:
                player.move(0, -1, maze)
                moved = True
            if event.key == pygame.K_DOWN:
                player.move(0, 1, maze)
                moved = True
            if moved:
                huellas.append(Huella(prev_pos))

            if event.key == pygame.K_p:
               await show_pause_menu(screen)
            if event.key == pygame.K_m:
                if music_on:
                    pygame.mixer.music.pause()
                    music_on = False
                else:
                    pygame.mixer.music.unpause()
                    music_on = True
            elif event.key == pygame.K_g:  # Truco para ganar el nivel
                return "WIN"

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
    await asyncio.sleep(0)
    return True