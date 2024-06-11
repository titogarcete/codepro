import pygame
import sys
import numpy as np

# Configuración básica
GRID_SIZE = 5
CELL_SIZE = 100
WINDOW_SIZE = GRID_SIZE * CELL_SIZE
HOLE_POSITION = np.array([4, 0])
RAT_COLOR = (255, 0, 0)
CAT_COLOR = (0, 0, 255)
HOLE_COLOR = (0, 255, 0)
BACKGROUND_COLOR = (200, 200, 200)
DEPTH = 3

pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Juego Gato y Ratón")

def draw_board():
    screen.fill(BACKGROUND_COLOR)
    for x in range(0, WINDOW_SIZE, CELL_SIZE):
        for y in range(0, WINDOW_SIZE, CELL_SIZE):
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)
    hole_x, hole_y = HOLE_POSITION
    pygame.draw.circle(screen, HOLE_COLOR, (hole_x * CELL_SIZE + CELL_SIZE // 2, hole_y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 4)

def draw_pieces(position_rat, position_cat):
    rat_x, rat_y = position_rat
    cat_x, cat_y = position_cat
    pygame.draw.circle(screen, RAT_COLOR, (rat_x * CELL_SIZE + CELL_SIZE // 2, rat_y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)
    pygame.draw.circle(screen, CAT_COLOR, (cat_x * CELL_SIZE + CELL_SIZE // 2, cat_y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)

def minimax(position_rat, position_cat, depth, is_maximizing):
    if is_terminal(position_rat, position_cat) or depth == DEPTH:
        return evaluate(position_rat, position_cat)

    if is_maximizing:
        max_eval = -float('inf')
        best_move = position_rat
        for move in get_possible_moves(position_rat):
            evaluation = minimax(move, position_cat, depth + 1, False)
            if evaluation > max_eval:
                max_eval = evaluation
                best_move = move
        if depth == 0:
            return best_move
        return max_eval
    else:
        min_eval = float('inf')
        best_move = position_cat
        for move in get_possible_moves(position_cat):
            evaluation = minimax(position_rat, move, depth + 1, True)
            if evaluation < min_eval:
                min_eval = evaluation
                best_move = move
        if depth == 0:
            return best_move
        return min_eval

def is_terminal(position_rat, position_cat):
    return np.array_equal(position_rat, HOLE_POSITION) or np.array_equal(position_rat, position_cat)

def evaluate(position_rat, position_cat):
    if np.array_equal(position_rat, HOLE_POSITION):
        return 100  # Rat wins
    if np.array_equal(position_rat, position_cat):
        return -100  # Cat wins
    rat_to_hole = np.sum(np.abs(position_rat - HOLE_POSITION))
    cat_to_rat = np.sum(np.abs(position_cat - position_rat))
    return cat_to_rat - rat_to_hole  # Minimize distance to hole and maximize distance from cat

def get_possible_moves(position):
    moves = []
    x, y = position
    if x > 0:
        moves.append(np.array([x-1, y]))
    if x < GRID_SIZE - 1:
        moves.append(np.array([x+1, y]))
    if y > 0:
        moves.append(np.array([x, y-1]))
    if y < GRID_SIZE - 1:
        moves.append(np.array([x, y+1]))
    return moves

def main():
    position_rat = np.array([0, 0])
    position_cat = np.array([4, 4])
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_board()
        draw_pieces(position_rat, position_cat)
        pygame.display.flip()

        # Movimiento del ratón
        new_position_rat = minimax(position_rat, position_cat, 0, True)
        if isinstance(new_position_rat, np.ndarray):
            position_rat = new_position_rat
        draw_board()
        draw_pieces(position_rat, position_cat)
        pygame.display.flip()
        pygame.time.wait(500)

        if is_terminal(position_rat, position_cat):
            break

        # Movimiento del gato
        new_position_cat = minimax(position_rat, position_cat, 0, False)
        if isinstance(new_position_cat, np.ndarray):
            position_cat = new_position_cat
        draw_board()
        draw_pieces(position_rat, position_cat)
        pygame.display.flip()
        pygame.time.wait(500)

        if is_terminal(position_rat, position_cat):
            break

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
