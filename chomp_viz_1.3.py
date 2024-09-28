import pygame
from chomp_logic import *
from ./chomp_testing_v2 import *

class Game():
    def __init__(self, board, render_size = None, square_size = None):
        self.board = board
        self.square_size = square_size
        if square_size is None:
            self.square_size = min(board_render_size[0] // max(max(self.board.board[0]) + 1, 1), board_render_size[1] // max(max(self.board.board[1]) + 1, 1))
        self.board_rects = self.generate_board_rects()
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
        if len(self.board_history) > 1:
            self.board = self.board_history[-2]
            self.board_history = self.board_history[:-1]
            self.generate_board_rects()
            self.move_history = self.move_history[:-1]
            self.switch_player()

    def generate_board_rects(self):
        board_rects = [pygame.Rect(self.square_size * self.board.board[0, i], self.square_size * self.board.board[1, i], self.square_size, self.square_size) for i in range(self.board.board.shape[1])]
        self.board_rects = board_rects
        return board_rects
    
    # Not as much of a "reset" than a 
    def reset_board(self, board_render_size, board_shape):
        self.square_size = min(board_render_size[0] // max(board_shape[0] + 1, 1), board_render_size[1] // max(board_shape[1] + 1, 1))
        self.board = BitBoard(size = board_shape)
        self.generate_board_rects()
        self.board_history = [self.board]
        self.move_history = []
        self.player = 1
        self.color = 'red'

    def make_move(self, move):
        self.board = self.board.chomp(move)
        self.generate_board_rects()
        self.switch_player()
        self.move_history.append(move)
        self.board_history.append(self.board)

    def draw_board(self, surface, color = "white", border_size = 0):
        for square in self.board_rects:
            pygame.draw.rect(surface, color, square, border_size)

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

pygame.init()
screen = pygame.display.set_mode((1280, 720))
font = pygame.font.SysFont('Arial', 25)
clock = pygame.time.Clock()
running = True

board_render_size = (700, 700) # Height and width of board on screen
board_shape = (10, 10) # Num rows and columns of board
num_rows, num_columns = board_shape

starting_board = BitBoard(size = board_shape).chomp((3, 1))
active_game = Game(starting_board, board_render_size)
win_flag, checked_boards = starting_board.is_winning()

for move in active_game.board.moves:
    if active_game.board.chomp(move).is_winning(checked_boards)[0] == False:
        print(move)

border_size = 5
reset_button_kwargs = {
    'text': "RESET",
    'border_size': border_size,
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

get_winning_boards_button_kwargs = {
    'text': "Get winning oards",
    'border_size': border_size
}
get_winning_boards_button = Button(position = (800, 300), size = (100, 50), surface = screen, **get_winning_boards_button_kwargs)

buttons = [row_input_button, column_input_button, reset_button, undo_button, get_winning_boards_button]

move_responses = {}

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
            active_game.reset_board(board_render_size, (num_rows, num_columns))

        # If user clicked a square on the board, chomp the board and switch to the next player's turn
        #TODO: ADD LOGIC TO ONLY ENTER THIS LOOP IF USER CLICKED IN THE BOARD
        for index, board_rect in enumerate(active_game.board_rects):
            if board_rect.collidepoint(mouse_position):
                move = active_game.board.moves[index]
                active_game.make_move(move)
                move_responses[move] = []
                for response in active_game.board.moves:
                    is_winning, checked_boards = active_game.board.chomp(response).is_winning(checked_boards)
                    if is_winning == False:
                        move_responses[move].append(response)
                        print(response)
                exit

        # If player clicked undo, reset board state to most recent board state
        if undo_button.clicked(mouse_position): active_game.undo()
        
        if get_winning_boards_button.active == True:
            win_flag, checked_boards = active_game.board.is_winning(checked_boards)

    # RENDER GRAPHICS
    screen.fill("black")
    for button in buttons: button.draw()
    active_game.draw_board(screen, border_size = 5)

    # Color the square the player is hovering over
    for square in active_game.board_rects:
        if square.collidepoint(mouse_position):
            pygame.draw.rect(screen, active_game.color, square, 5)
    for button in buttons:
        button.rect_color = (255, 255, 255)
        if button.hovered_over(mouse_position): button.rect_color = (0, 255, 0)

    pygame.display.flip()
    clock.tick(60)

    import pprint

pygame.quit()

pprint.pp(move_responses)

# for move in move_responses.keys():
#     print(f'{move}: {[response for response in move_responses[move]]}\n')