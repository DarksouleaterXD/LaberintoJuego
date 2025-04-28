import pygame
import random
import time
import math
from settings import DIRECTIONS, BLUE, RED, HEIGHT

def generate_maze(rows, cols):
    maze = [[1 for _ in range(cols)] for _ in range(rows)]
    walls = []
    start_x, start_y = 1, 1
    maze[start_y][start_x] = 0

    for dx, dy in DIRECTIONS:
        nx, ny = start_x + dx, start_y + dy
        if 1 <= nx < cols - 1 and 1 <= ny < rows - 1:
            walls.append((nx, ny, start_x, start_y))

    while walls:
        wx, wy, px, py = random.choice(walls)
        walls.remove((wx, wy, px, py))
        if maze[wy][wx] == 1:
            maze[wy][wx] = 0
            maze[(wy + py) // 2][(wx + px) // 2] = 0
            for dx, dy in DIRECTIONS:
                nx, ny = wx + dx, wy + dy
                if 1 <= nx < cols - 1 and 1 <= ny < rows - 1:
                    walls.append((nx, ny, wx, wy))

    if not is_accessible(start_x, start_y, maze):
        maze[start_y][start_x] = 1
        maze = regenerate_path(start_x, start_y, maze, rows, cols)

    exit_x, exit_y = cols - 2, rows - 2
    maze[exit_y][exit_x] = 0
    if maze[exit_y - 1][exit_x] == 1 and maze[exit_y][exit_x - 1] == 1:
        maze[exit_y - 1][exit_x] = 0

    return {"grid": maze, "tile_size": HEIGHT // rows}

def is_accessible(start_x, start_y, maze):
    visited = [[False for _ in row] for row in maze]
    stack = [(start_x, start_y)]
    
    while stack:
        x, y = stack.pop()
        if visited[y][x]:
            continue
        visited[y][x] = True
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze[0]) and 0 <= ny < len(maze) and maze[ny][nx] == 0:
                stack.append((nx, ny))

    return visited[start_y][start_x]

def regenerate_path(start_x, start_y, maze, rows, cols):
    maze[start_y][start_x] = 0
    walls = [(start_x, start_y)]
    while walls:
        wx, wy = random.choice(walls)
        walls.remove((wx, wy))
        if maze[wy][wx] == 1:
            maze[wy][wx] = 0
            for dx, dy in DIRECTIONS:
                nx, ny = wx + dx, wy + dy
                if 1 <= nx < cols - 1 and 1 <= ny < rows - 1 and maze[ny][nx] == 1:
                    walls.append((nx, ny))
    return maze

def move_walls_dynamically(maze, player):
    """
    Abre o cierra caminos en función del movimiento del jugador.
    """
    # Obtener las dimensiones del laberinto
    height = len(maze)
    width = len(maze[0])

    # Coordenadas del jugador
    player_x, player_y = player.x, player.y

    # Direcciones posibles para mover paredes
    directions = [
        (0, -1),  # Arriba
        (0, 1),   # Abajo
        (-1, 0),  # Izquierda
        (1, 0)    # Derecha
    ]

    # Abrir caminos en la dirección hacia la que se mueve el jugador
    for dx, dy in directions:
        nx, ny = player_x + dx, player_y + dy

        # Asegúrate de que no estás fuera del rango del laberinto
        if 1 <= nx < width - 1 and 1 <= ny < height - 1:
            # Abrir el camino si es una pared
            if maze[ny][nx] == 1:
                maze[ny][nx] = 0  # Cambiar a camino

    # Opcional: Cerrar caminos detrás del jugador
    # Aquí podríamos cerrar caminos no utilizados por el jugador
    for dx, dy in directions:
        nx, ny = player_x - dx, player_y - dy

        # Asegúrate de que no estás fuera del rango del laberinto
        if 1 <= nx < width - 1 and 1 <= ny < height - 1:
            # Si es un camino, convertirlo en pared con cierta probabilidad
            if maze[ny][nx] == 0 and random.random() < 0.3:  # 30% de probabilidad
                maze[ny][nx] = 1  # Cambiar a pared

    # Nota: Nunca cerrar el inicio o la salida
    maze[1][1] = 0  # Inicio
    maze[height - 2][width - 2] = 0  # Salida

class Player:
    def __init__(self, tile_size):
        self.x, self.y = 1, 1
        self.color = BLUE
        self.tile_size = tile_size
        self.rect = pygame.Rect(self.x * tile_size, self.y * tile_size, tile_size, tile_size)
        self.moves = 0
        self.start_time = time.time()

    def move(self, dx, dy, maze):
        new_x, new_y = self.x + dx, self.y + dy
        if 0 <= new_x < len(maze[0]) and 0 <= new_y < len(maze) and maze[new_y][new_x] == 0:
            self.x, self.y = new_x, new_y
            self.rect.topleft = (self.x * self.tile_size, self.y * self.tile_size)
            self.moves += 1

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Monster:
    def __init__(self, maze, tile_size, speed, level):
        while True:
            self.x = random.randint(1, len(maze[0]) - 2)
            self.y = random.randint(1, len(maze) - 2)
            if maze[self.y][self.x] == 0:
                break
        self.tile_size = tile_size
        self.rect = pygame.Rect(self.x * tile_size, self.y * tile_size, tile_size, tile_size)
        self.direction = random.choice(DIRECTIONS)
        self.last_move_time = pygame.time.get_ticks()
        self.speed = speed
        self.level = level

    
    def move(self, maze, player=None, level=1):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time >= self.speed:
            if level >= 3 and player:
                self.chase_player(player, maze)
            else:
                new_x = self.x + self.direction[0] // 2
                new_y = self.y + self.direction[1] // 2
                if 0 <= new_x < len(maze[0]) and 0 <= new_y < len(maze) and maze[new_y][new_x] == 0:
                    self.x, self.y = new_x, new_y
                else:
                    self.direction = random.choice(DIRECTIONS)
                self.rect.topleft = (self.x * self.tile_size, self.y * self.tile_size)
            self.last_move_time = current_time

    def draw(self, screen):
       
        

        # Crear un color pulsante basado en el tiempo
        time = pygame.time.get_ticks() / 500  # Controla la velocidad del cambio
        red = int(128 + 127 * math.sin(time + self.x * 0.1))
        green = int(128 + 127 * math.sin(time + self.y * 0.1))
        blue = int(128 + 127 * math.sin(time))

        color = (red, green, blue)

        pygame.draw.rect(screen, color, self.rect)

    def chase_player(self, player, maze):
        dx = player.x - self.x
        dy = player.y - self.y

        if abs(dx) > abs(dy):
            step_x = 1 if dx > 0 else -1
            new_x = self.x + step_x
            if 0 <= new_x < len(maze[0]) and maze[self.y][new_x] == 0:
                self.x = new_x
            else:
                step_y = 1 if dy > 0 else -1
                new_y = self.y + step_y
                if 0 <= new_y < len(maze) and maze[new_y][self.x] == 0:
                    self.y = new_y
        else:
            step_y = 1 if dy > 0 else -1
            new_y = self.y + step_y
            if 0 <= new_y < len(maze) and maze[new_y][self.x] == 0:
                self.y = new_y
            else:
                step_x = 1 if dx > 0 else -1
                new_x = self.x + step_x
                if 0 <= new_x < len(maze[0]) and maze[self.y][new_x] == 0:
                    self.x = new_x

        self.rect.topleft = (self.x * self.tile_size, self.y * self.tile_size)
