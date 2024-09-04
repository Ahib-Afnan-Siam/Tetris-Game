import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
WINDOW_WIDTH = 300
WINDOW_HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = WINDOW_WIDTH // BLOCK_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // BLOCK_SIZE
GRID_TOP = 0
GRID_LEFT = 0
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Tetris")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)

# Define tetromino shapes
tetrominoes = [
    [[1, 1, 1, 1]],  # I-shape
    [[1, 1, 0], [0, 1, 1]],  # Z-shape
    [[0, 1, 1], [1, 1, 0]],  # S-shape
    [[1, 1, 1], [0, 1, 0]],  # T-shape
    [[1, 1], [1, 1]],  # O-shape
    [[1, 1, 1], [1, 0, 0]],  # L-shape
    [[1, 1, 1], [0, 0, 1]]   # J-shape
]

# Define colors for tetrominoes
tetromino_colors = [CYAN, BLUE, ORANGE, YELLOW, GREEN, PURPLE, GRAY]

# Define directions
LEFT = (-1, 0)
RIGHT = (1, 0)
DOWN = (0, 1)

def create_grid():
    return [[BLACK] * GRID_WIDTH for _ in range(GRID_HEIGHT)]

def draw_grid(surface, grid):
    for y, row in enumerate(grid):
        for x, color in enumerate(row):
            pygame.draw.rect(surface, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(surface, WHITE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

def draw_piece(surface, piece, position):
    shape = tetrominoes[piece['shape']]
    for y, row in enumerate(shape):
        for x, block in enumerate(row):
            if block:
                pygame.draw.rect(surface, piece['color'], ((position[0] + x) * BLOCK_SIZE, (position[1] + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(surface, WHITE, ((position[0] + x) * BLOCK_SIZE, (position[1] + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

def check_collision(grid, piece, position):
    shape = tetrominoes[piece['shape']]
    for y, row in enumerate(shape):
        for x, block in enumerate(row):
            if block:
                if position[1] + y >= GRID_HEIGHT:
                    return True
                if position[0] + x < 0 or position[0] + x >= GRID_WIDTH:
                    return True
                if grid[position[1] + y][position[0] + x] != BLACK:
                    return True
    return False

def clear_rows(grid):
    full_rows = [row for row in range(GRID_HEIGHT) if all(grid[row])]
    for row in full_rows:
        del grid[row]
        grid.insert(0, [BLACK] * GRID_WIDTH)
    return len(full_rows)

def main():
    grid = create_grid()
    current_piece = {'shape': random.randint(0, len(tetrominoes) - 1), 'color': random.choice(tetromino_colors), 'position': [GRID_WIDTH // 2 - 2, 0]}
    next_piece = {'shape': random.randint(0, len(tetrominoes) - 1), 'color': random.choice(tetromino_colors)}

    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.5
    score = 0

    while True:
        WINDOW.fill(BLACK)
        draw_grid(WINDOW, grid)
        draw_piece(WINDOW, current_piece, current_piece['position'])

        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece['position'][1] += 1
            if check_collision(grid, current_piece, current_piece['position']):
                current_piece['position'][1] -= 1
                for y, row in enumerate(tetrominoes[current_piece['shape']]):
                    for x, block in enumerate(row):
                        if block:
                            grid[current_piece['position'][1] + y][current_piece['position'][0] + x] = current_piece['color']
                cleared_rows = clear_rows(grid)
                score += cleared_rows
                if cleared_rows > 0:
                    fall_speed -= 0.05  # Increase fall speed after clearing rows
                current_piece = next_piece
                next_piece = {'shape': random.randint(0, len(tetrominoes) - 1), 'color': random.choice(tetromino_colors)}
                current_piece['position'] = [GRID_WIDTH // 2 - 2, 0]  # Reset position

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece['position'][0] -= 1
                    if check_collision(grid, current_piece, current_piece['position']):
                        current_piece['position'][0] += 1
                if event.key == pygame.K_RIGHT:
                    current_piece['position'][0] += 1
                    if check_collision(grid, current_piece, current_piece['position']):
                        current_piece['position'][0] -= 1
                if event.key == pygame.K_DOWN:
                    current_piece['position'][1] += 1
                    if check_collision(grid, current_piece, current_piece['position']):
                        current_piece['position'][1] -= 1
                if event.key == pygame.K_UP:
                    current_piece['shape'] = (current_piece['shape'] + 1) % len(tetrominoes)
                    if check_collision(grid, current_piece, current_piece['position']):
                        current_piece['shape'] = (current_piece['shape'] - 1) % len(tetrominoes)

        pygame.display.update()

if __name__ == "__main__":
    main()