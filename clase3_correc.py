import pygame
import numpy as np
import random

# FUNCIONES

def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col): # Simula la gravedad
    for r in range(ROW_COUNT): # de 0 a 6
        if board[r][col] == 0:
            return r 

def drop_piece(board, row, col, piece):
    board[row][col] = piece # Asignamos el valor de la pieza en la matriz

def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARE_SIZE, (r+1)*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARE_SIZE + SQUARE_SIZE/2), int((r+1)*SQUARE_SIZE + SQUARE_SIZE/2)), RADIUS) # Dibujamos un círculo
    
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARE_SIZE + SQUARE_SIZE/2), HEIGHT - int((r+1)*SQUARE_SIZE + SQUARE_SIZE/2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARE_SIZE + SQUARE_SIZE/2), HEIGHT - int((r+1)*SQUARE_SIZE + SQUARE_SIZE/2)), RADIUS)

    pygame.display.update()

def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

    return False

def cpu_player(board, piece):
    valid_locations = [col for col in range(COLUMN_COUNT) if is_valid_location(board, col)]
    return random.choice(valid_locations)

# CONSTANTES
ROW_COUNT = 6  # Número de filas
COLUMN_COUNT = 7  # Número de columnas
SQUARE_SIZE = 100  # Tamaño del cuadro
RADIUS = int(SQUARE_SIZE / 2.5)  # Radio de la fichita
WIDTH = COLUMN_COUNT * SQUARE_SIZE  # Anchura de la ventana
HEIGHT = (ROW_COUNT + 1) * SQUARE_SIZE
BLUE = (0, 0, 255)  # Para el tablero
BLACK = (0, 0, 0)  # Fichas vacías
RED = (255, 0, 0)  # Fichas del jugador
YELLOW = (255, 255, 0)  # Fichas de la CPU

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Practica de Busqueda")

# Main
def main():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))  # Crear el tablero
    game_over = False  # Verificar si el juego ha terminado
    turn = 0  # 0 para el usuario y 1 para la CPU

    draw_board(board)
    pygame.display.update()

    while not game_over: # Mientras no haya un ganador, haremos lo siguiente
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            if event.type == pygame.MOUSEMOTION: # Movimiento del mouse
                pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARE_SIZE))
                posx = event.pos[0]
                if turn == 0: # Si el turno es del jugador
                    pygame.draw.circle(screen, RED, (posx, int(SQUARE_SIZE/2)), RADIUS) # Dibuja la ficha del jugador
                pygame.display.update() # Actualizamos cada movimiento del mouse

            if event.type == pygame.MOUSEBUTTONDOWN and turn == 0:
                posx = event.pos[0] 
                col = int(posx // SQUARE_SIZE)
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1) # Tiramos una ficha del jugador
                    if winning_move(board, 1):
                        print("Jugador ha ganado")
                        game_over = True
                    turn = 1
                    draw_board(board)
                    
        if turn == 1 and not game_over:
            col = cpu_player(board, 2) # Se calcula el tiro del CPU
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 2)
                if winning_move(board, 2):
                    print("CPU ha ganado")
                    game_over = True
                turn = 0 
                draw_board(board)

        if game_over:
            pygame.time.wait(3000) 

if __name__ == "__main__":
    main() # Corremos el juego