import pygame
import numpy as np
from chomplogic import *

def generate_board_rects(board, num_rows, num_columns):
    square_size = min(700 // num_columns, 700 // num_rows)
    board_rects = [pygame.Rect(square_size * board[0, i], square_size * board[1, i], square_size, square_size) for i in range(board.shape[1])]
    return board_rects

def draw_board(surface, board, color = "white", border_size = 0):
    for square in board:
        pygame.draw.rect(surface, color, square, border_size)
    return

def draw_button(surface, button_rect, text = ""):
    text_surface = font.render(text, True, "white")
    text_rect = text_surface.get_rect(center = button_rect.center)
    pygame.draw.rect(screen, "white", button_rect, 5)
    surface.blit(text_surface, text_rect)

def generate_starting_board(num_rows, num_columns):
    square_size = min(700 // num_columns, 700 // num_rows)

    row_indices = list(range(num_columns)) * num_rows
    column_indices = []
    for j in range(num_rows):
        column_indices += [j] * num_columns
    square_indices = list(zip(row_indices, column_indices))

    starting_board = [pygame.Rect(square_size * i, square_size * j, square_size, square_size) for i, j in square_indices]

    return starting_board

def chomp_board(board, eaten_square):
    squares_to_remove = []
    for square in board:
        if (square.left >= eaten_square.left) and (square.top >= eaten_square.top):
            squares_to_remove.append(square)
    
    for square in squares_to_remove:
        board.remove(square)
    
    return(board)

def switch_player(player):
    if player == 1:
        player = 2
        color = "blue"
    elif player == 2:
        player = 1
        color = "red"
    return player, color



pygame.init()
screen = pygame.display.set_mode((1280, 720))
font = pygame.font.SysFont('Arial', 25)
clock = pygame.time.Clock()
running = True

#board = generate_starting_board(10, 10)
board = generate_board_rects(BitBoard(size = 10).board, 10, 10)
#board_rects = generate_board_rects(test_board, 10, 10)
player, color = 1, "red"
reset_rect = pygame.Rect(800, 100, 150, 50)

row_input_rect = pygame.Rect(1000, 100, 60, 50)
row_input = '10'
row_input_active = False

column_input_rect = pygame.Rect(1100, 100, 60, 50)
column_input = '10'
column_input_active = False

while running:
    # All event checking
    click = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            click = True
        if event.type == pygame.KEYDOWN: 
            # TODO: ADD LOGIC TO ENSURE KEY IS A NUMBER
            if row_input_active == True:
                # Check for backspace 
                if event.key == pygame.K_BACKSPACE: 
                    row_input = row_input[:-1] # get text input from 0 to -1 i.e. end. 
                else: 
                    row_input += event.unicode # Unicode standard is used for string formation
            if column_input_active == True:
                # Check for backspace 
                if event.key == pygame.K_BACKSPACE: 
                    column_input = column_input[:-1] # get text input from 0 to -1 i.e. end. 
                else: 
                    column_input += event.unicode # Unicode standard is used for string formation

    # Identify if a board square was clicked
    clicked_square = None
    if click == True:
        # If the user clicked on either the row or column input, activate it to allow input, else they clicked outside of the input so deactivate
        if row_input_rect.collidepoint(pygame.mouse.get_pos()):
            row_input_active = True
            column_input_active = False
        elif column_input_rect.collidepoint(pygame.mouse.get_pos()):
            column_input_active = True
            row_input_active = False
        else:
            row_input_active = column_input_active = False

        # If user clicked the reset button, reset board
        if reset_rect.collidepoint(pygame.mouse.get_pos()):
            board = generate_starting_board(int(row_input), int(column_input))
            player, color = 1, "red"

        # If user clicked a square on the board, 
        #TODO: ADD LOGIC TO ONLY ENTER THIS LOOP IF USER CLICKED IN THE BOARD
        for square in board:
                if square.collidepoint(pygame.mouse.get_pos()):
                    clicked_square = square
                    exit

    # If player makes a move, chomp the board and switch to the next player's turn
    if clicked_square is not None:
        board = chomp_board(board, clicked_square)
        player, color = switch_player(player)


    # RENDER GRAPHICS
    screen.fill("black")
    draw_button(screen, reset_rect, "RESET") # Reset button
    draw_button(screen, row_input_rect, row_input) # Row input button
    draw_button(screen, column_input_rect, column_input) # Column input button
    draw_board(screen, board, border_size = 5)

    # Color the square the player is hovering over
    for square in board:
        if square.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, color, square, 5)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()