import pygame
import numpy as np
from chomp_logic import *

class Button():
    def __init__(self, position: tuple, size: tuple, on_click: function = None, text = "", properties: dict = {}):
        self.rect = pygame.Rect(*position, *size)
        self.properties = properties
        self.text = text
        self.on_click = on_click

    def clicked(self, click_position: tuple) -> bool: 
        return self.rect.collidepoint(click_position)

    def draw(self, surface, rect_color = "white", text_color = "white"):
        text_surface = font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center = self.rect.center)
        pygame.draw.rect(surface, rect_color, self.rect, 5)
        surface.blit(text_surface, text_rect)

def generate_board_rects(board, square_size):
    board_rects = [pygame.Rect(square_size * board[0, i], square_size * board[1, i], square_size, square_size) for i in range(board.shape[1])]
    return board_rects

def draw_board(surface, board_rects, color = "white", border_size = 0):
    for square in board_rects:
        pygame.draw.rect(surface, color, square, border_size)
    return

def draw_button(surface, button_rect, text = ""):
    text_surface = font.render(text, True, "white")
    text_rect = text_surface.get_rect(center = button_rect.center)
    pygame.draw.rect(screen, "white", button_rect, 5)
    surface.blit(text_surface, text_rect)

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

board_render_width = board_render_height = 700
num_rows = num_columns = 10
border_size = 5

square_size = min(board_render_height // num_rows, board_render_width // num_columns)

player, color = 1, "red"

reset_button = Button((800, 100), (150, 50), text = "RESET")
reset_rect = pygame.Rect(800, 100, 150, 50)

row_input_properties = column_input_properties = {
    'active': False
}
row_input_button = Button(position = (1000, 100), size = (60, 50), text = str(num_rows))
column_input_button = Button(position = (1100, 100), size = (60, 5), text = str(num_columns))

row_input_rect = pygame.Rect(1000, 100, 60, 50)
row_input = str(num_rows)
row_input_active = False

column_input_rect = pygame.Rect(1100, 100, 60, 50)
column_input = str(num_columns)
column_input_active = False

board = BitBoard(size = (num_rows, num_columns))

board_rects = generate_board_rects(board.board, square_size)

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
    clicked_square_index = None
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
            num_rows = int(row_input)
            num_columns = int(column_input)
            square_size = min(board_render_height // num_rows, board_render_width // num_columns)

            board = BitBoard(size = (num_rows, num_columns))
            player, color = 1, "red"

        # If user clicked a square on the board, 
        #TODO: ADD LOGIC TO ONLY ENTER THIS LO5OP IF USER CLICKED IN THE BOARD
        clicked_square_index 
        for i in range(len(board_rects)):
                if board_rects[i].collidepoint(pygame.mouse.get_pos()):
                    clicked_square_index = i
                    exit

    # If player makes a move, chomp the board and switch to the next player's turn
    if clicked_square_index is not None:
        board.chomp(board.board[:, clicked_square_index])
        player, color = switch_player(player)
        clicked_square_index = None


    # RENDER GRAPHICS
    board_rects = generate_board_rects(board.board, square_size)

    screen.fill("black")
    draw_button(screen, reset_rect, "RESET") # Reset button
    draw_button(screen, row_input_rect, row_input) # Row input button
    draw_button(screen, column_input_rect, column_input) # Column input button
    draw_board(screen, board_rects, border_size = 5)

    # Color the square the player is hovering over
    for square in board_rects:
        if square.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, color, square, 5)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()