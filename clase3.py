#juego de conecta 4 con 7x5 cuadros , 3 posibles entradas 
import pygame
import numpy as np
import random
#constantes
ROW_COUNT = 6 #numero de filas
COLUMN_COUNT = 7 #numero de columnas
SQUARESIZE = 100 #Tam del cuadro
RADIUS = int(SQUARESIZE/2 - 5) #Radio de la ficha
width = COLUMN_COUNT * SQUARESIZE #Anchura de la ventana
height = (ROW_COUNT+1) * SQUARESIZE
blue = (0,0,255) #Para l tablero
black = (0,0,0) #Fichas vacias
red = (255,0,0) #Fichas del jugador
yellow = (255,255,0) #Fichas de la cpu

pygame.init()
screen = pygame.display.set_mode((width,height)) #renderizando la ventana

pygame.display.set_caption("Practica de busqueda") #nombre de la ventana 
#Funciones
def is_valid_location(board,col): #checa si una posicion ya tiene ficha
    return board[ROW_COUNT-1][col] == 0 #si la ultima fila esta vacia
def get_next_open_row(board,col): #obtiene la siguiente fila vacia
    for r in range(ROW_COUNT): # empieza de 0 a 6
        if board[r][col] == 0:
            return r #regresa si la fila esta vacia
def drop_piece(board,row,col,piece): #coloca la ficha en la posicion
    board[row][col] = piece # Asignando valor a la matriz
def cpu_player(board,piece):
    best_score = -float("inf")
    best_col = random.choice([col in col in range (COLUMN_COUNT) if is_valid_location(board,col)])
    for col in range(COLUMN_COUNT):
        if is_valid_location(board,col):
            row = get_next_open_row(board,col)
            temp_board = board.copy()
            drop_piece(temp_board,row,col,piece)
            score = minimax(temp_board,3,-float("inf"),float("inf"),False)
            if score > best_score:
                best_score = score
                best_col = col
    return best_col
def minimax(board,depth,alpha,beta,maximizingPlayer):
    #si se exploro todo el arbol o encontramos un movimiento ganador
    if depth == 0 or winning_move(board,1) or winning_move(board,2):
        if winning_move(board,2):
            return 1000000000 #garantiza que la cpu gane
        elif winning_move(board,1):
            return -1000000000 #no debemos formar este movimiento
        else:
            return 0
    if maximizingPlayer:
        max_eval = -float("inf")
        for col in range(COLUMN_COUNT): #dfs
            if is_valid_location(board,col):
                row = get_next_open_row(board,col)
                temp_board = board.copy()
                drop_piece(temp_board,row,col,2)
                eval = minimax(temp_board,depth-1,alpha,beta,False)
                max_eval = max(max_eval,eval)
                alpha = max(alpha,eval)
                if beta <= alpha:
                    break #realiza la poda Beta
        return max_eval
    else: #turno del jugador
        min_eval = float("inf")
        for col in range(COLUMN_COUNT):
            if is_valid_location(board,col):
                row = get_next_open_row(board,col)
                temp_board = board.copy()
                drop_piece(temp_board,row,col,1)
                eval = minimax(temp_board,depth-1,alpha,beta,True)
                min_eval = min(min_eval,eval)
                beta = min(beta,eval)
                if beta <= alpha:
                    break
    
def winning_move(board,piece):
    return False 
def draw_board(board): #dibujar el tablero
    for c in range(COLUMN_COUNT): #dibujar las lineas verticales
        for r in range(ROW_COUNT): #dibujar las lineas horizontales
            pygame.draw.rect(screen,blue,(c*SQUARESIZE,(r+1)*SQUARESIZE,SQUARESIZE))
            pygame.draw.circle(screen,black,(int(c*SQUARESIZE+SQUARESIZE/2),int((r+1)*SQUARESIZE+SQUARESIZE/2)),RADIUS) #dnujamos un circulo
    for c in range(COLUMN_COUNT): #dibujar las lineas verticales
        for r in range(ROW_COUNT):
            if board[c][r] == 1:
                pygame.draw.circle(screen,red,(int(c*SQUARESIZE+SQUARESIZE/2),height-int(r*SQUARESIZE+SQUARESIZE/2)),RADIUS)
            elif board[c][r] == 2:
                pygame.draw.circle(screen,yellow,(int(c*SQUARESIZE+SQUARESIZE/2),height-int(r*SQUARESIZE+SQUARESIZE/2)),RADIUS)
        pygame.display.update()
def main():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    game_over = False #para saber si el juego termino
    turn = 0 #0 para el jugador, 1 para la cpu

    pygame.display.update()
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #salir del juego
                pygame.quit()
                return
            if event.type == pygame.MOUSEMOTION: #movimiento del mouse
                pygame.draw.rect(screen,black,(0,0,width,SQUARESIZE))
                posx = event.pos[0]
                if turn == 0: #si el turno es fdel
                    pygame.draw.circle(screen,red,(posx,int(SQUARESIZE/2)),RADIUS) #dibujar ficha del jugador
                pygame.display.update()
            if event.type == pygame.MOUSEBUTTONDOWN and turn==0:
                posx = event.pos[0] 
                col = int(posx//SQUARESIZE)
                if is_valid_location(board,col):
                    row = get_next_open_row(board,col)
                    drop_piece(board,row,col,1)# tiramos una ficha del jugador
                    if winning_move(board,1):
                        print("Jugador gana")
                        game_over = True
                    turn=1 #Turno de la CPU y no se ha terminado el juego
                    draw_board(board)
        if turn == 1 and not game_over:
            col=cpu_player(board,2)
            if is_valid_location(board, col):
                row = get_next_open_row(board,col)
                drop_piece(board,row,col,2)
                if winning_move(board,2):
                    print("CPU gana")
                    game_over = True

                turn = 0
                draw_board(board)
        if game_over:
            pygame.time.wait(3000)
if __name__ == "__main__":
    main()    