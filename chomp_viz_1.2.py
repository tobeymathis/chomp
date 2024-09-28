import pygame
import numpy as np
from chomp_logic import *

class Game():
    def __init__(self, board, render_size):
        self.board = board
        self.square_size = None
        self.board_rects = None
        self.color = 'red'
        self.player = 1
        self.move_history = []
        self.board_history = [self.board]

    def switch_player(self):
        if self.player == 1:
            self.player = 2
            self.color = "blue"
        elif self.player == 2:
            self.player = 1
            self.color = "red"

    def undo(self):
        self.board = self.board_history[-2]
        self.move_history = self.move_history[:-1]
        self.switch_player()

    def generate_board_rects(board, square_size):
        board_rects = [pygame.Rect(square_size * board[0, i], square_size * board[1, i], square_size, square_size) for i in range(board.shape[1])]
        return board_rects
    
    def draw_board(surface, board_rects, color = "white", border_size = 0):
        for square in board_rects:
            pygame.draw.rect(surface, color, square, border_size)

    def reset_board(self, board_render_size, board_shape):
        self.square_size = min(board_render_size[0] // max(board_shape[0], 1), board_render_size[1] // max(board_shape[1], 1))
        self.board = BitBoard(size = board_shape)
        self.board_rects = self.generate_board_rects(self.board.board, self.square_size)
        self.player = 1
        self.color = 'red'
        return board, board_rects, square_size, player, color


class Button():
    def __init__(self, position: tuple, size: tuple, surface: pygame.surface, **kwargs):
        self.rect = pygame.Rect(*position, *size)
        self.surface = surface

        self.active = kwargs.get('active')
        self.text = kwargs.get('text')
        self.text_color = kwargs.get('text_color', (255, 255, 255))
        self.rect_color = kwargs.get('rect_color', (255, 255, 255))
        self.border_size = kwargs.get('border_size', 0)
        self.on_click = kwargs.get('on_click')
        self.on_hover = kwargs.get('on_hover')

    def clicked(self, click_position: tuple) -> bool: 
        return self.rect.collidepoint(click_position)
    
    def hovered_over(self, mouse_position: tuple) -> bool:
        return self.rect.collidepoint(mouse_position)

    def draw(self):
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center = self.rect.center)
        pygame.draw.rect(self.surface, self.rect_color, self.rect, self.border_size)
        self.surface.blit(text_surface, text_rect)

def generate_board_rects(board, square_size):
    board_rects = [pygame.Rect(square_size * board[0, i], square_size * board[1, i], square_size, square_size) for i in range(board.shape[1])]
    return board_rects

def draw_board(surface, board_rects, color = "white", border_size = 0):
    for square in board_rects:
        pygame.draw.rect(surface, color, square, border_size)
    return

def initialize_board(board_render_size, board_shape):
    square_size = min(board_render_size[0] // max(board_shape[0], 1), board_render_size[1] // max(board_shape[1], 1))
    board = BitBoard(size = board_shape)
    board_rects = generate_board_rects(board.board, square_size)
    player = 1
    color = 'red'
    return board, board_rects, square_size, player, color

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

board_render_size = (700, 700) # Height and width of board on screen
board_shape = (10, 10) # Num rows and num_columns of board
num_rows, num_columns = board_shape

board, board_rects, square_size, player, color = initialize_board(board_render_size, board_shape)

border_size = 5
reset_button_kwargs = {
    'text': "RESET",
    'border_size': border_size,
    'on_click': initialize_board
}
reset_button = Button(position = (800, 100), size = (150, 50), surface = screen, **reset_button_kwargs)

row_input_kwargs = {
    'active': False,
    'text': str(num_rows),
    'border_size': border_size
}
row_input_button = Button(position = (1000, 100), size = (60, 50), surface = screen, **row_input_kwargs)

column_input_kwargs = {
    'active': False,
    'text': str(num_columns),
    'border_size': border_size
}
column_input_button = Button(position = (1100, 100), size = (60, 50), surface = screen, **column_input_kwargs)

undo_button_kwargs = {
    'text': "UNDO",
    'border_size': border_size
}
undo_button = Button(position = (800, 200), size = (100, 50), surface = screen, **undo_button_kwargs)

buttons = [row_input_button, column_input_button, reset_button, undo_button]

while running:
    # All event checking
    click = key_press = False # Reset flags
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            click = True
        if event.type == pygame.KEYDOWN:
            key_press = True
            key_press_event = event 

    # If a keyboard button was pressed, update values
    if key_press:
        if row_input_button.active == True:
            # Check for backspace 
            if key_press_event.key == pygame.K_BACKSPACE: 
                row_input_button.text = row_input_button.text[:-1] # get text input from 0 to -1 i.e. end. 
            elif key_press_event.unicode.isnumeric(): 
                row_input_button.text += key_press_event.unicode # Unicode standard is used for string formation
        if column_input_button.active == True:
            # Check for backspace 
            if key_press_event.key == pygame.K_BACKSPACE: 
                column_input_button.text = column_input_button.text[:-1] # get text input from 0 to -1 i.e. end. 
            elif key_press_event.unicode.isnumeric(): 
                column_input_button.text += key_press_event.unicode # Unicode standard is used for string formation

    # Identify if a board square was clicked
    mouse_position = pygame.mouse.get_pos()
    if click:
        # If the user clicked on either the row or column input, activate it to allow input, else they clicked outside of the input so deactivate
        row_input_button.active = column_input_button.active = False
        if row_input_button.clicked(mouse_position): row_input_button.active = True
        if column_input_button.clicked(mouse_position): column_input_button.active = True
            
        # If user clicked the reset button, reset board
        if reset_button.clicked(mouse_position):
            num_rows = num_columns = 0
            if row_input_button.text != '': num_rows = int(row_input_button.text)
            if column_input_button.text != '': num_columns = int(column_input_button.text)
            board, board_rects, square_size, player, color = reset_button.on_click(board_render_size, (num_rows, num_columns))

        # If user clicked a square on the board, chomp the board and switch to the next player's turn
        #TODO: ADD LOGIC TO ONLY ENTER THIS LOOP IF USER CLICKED IN THE BOARD
        for index, board_rect in enumerate(board_rects):
            if board_rect.collidepoint(mouse_position):
                move = board.moves[index]
                board = board.chomp(move)
                board_rects = generate_board_rects(board.board, square_size)
                player, color = switch_player(player)
                exit
        

    # RENDER GRAPHICS
    screen.fill("black")
    for button in buttons: button.draw()
    draw_board(screen, board_rects, border_size = 5)

    # Color the square the player is hovering over
    for square in board_rects:
        if square.collidepoint(mouse_position):
            pygame.draw.rect(screen, color, square, 5)
    for button in buttons:
        button.rect_color = (255, 255, 255)
        if button.hovered_over(mouse_position): button.rect_color = (0, 255, 0)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()