from pprint import pprint

def get_boards(max_height: int, max_width: int, position: int = 0) -> list:
    checked_lists = []
    if position == max_width - 1:
        checked_lists = [[i] for i in range(0, max_height + 1)]
        return checked_lists
    for i in range(max_height + 1):
        sub_boards = get_boards(i, max_width, position + 1)
        for sub_board in sub_boards:
            checked_lists.append([i] + sub_board)
        
    return checked_lists

def print_board(board):
    board_rep = board.astype(str)
    board_rep[board_rep == 'True'] = '\u25A9' # Replace all "True" values with a filled square
    board_rep[board_rep == 'False'] = '\u25A1' # Replace all "False" values with a empty square

    hash_key_array = [] # Store string as an array to speed up operations
    for i in range(board_rep.shape[0]):
        for j in range(board_rep.shape[1]):
            hash_key_array.append(board_rep[i, j])
            hash_key_array.append(' ')
        hash_key_array = hash_key_array[:-1] # Remove the extra space
        hash_key_array.append('\n')

    hash_key_array = hash_key_array[:-1] # Remove the extra newline character
    hash_key = ''.join(hash_key_array)
    print(hash_key + '\n')


class Board(list):
    def __init__(self, board):
        super().__init__(board)

        self.board = [element for element in board if element != 0]
        self.string_rep = ''.join([str(element) + ',' for element in self.board])[:-1]
        self.moves = self.get_moves()

    def __repr__(self):
        return repr(self.board)

    def chomp(self, move: tuple, in_place: bool = False):
        column, height = move
        new_board = [element for element in self.board]
        for i in range(column, len(new_board)):
            new_board[i] = min(new_board[i], height)
        if in_place == True:
            self.__init__(new_board)
        return Board(new_board)
    
    def get_moves(self):
        moves = []
        for i in range(len(self.board)):
            for j in range(self.board[i]):
                if (i, j) != (0, 0):
                    moves.append((i, j))
        return moves

    def get_sub_boards(self):
        sub_boards = []
        for move in self.moves:
            sub_boards.append(self.chomp(move))
        return sub_boards
    
    def transpose(self):
        num_columns_transpose = max(self.board)
        transpose = [0] * num_columns_transpose
        for i in range(num_columns_transpose):
            transpose[i] = sum([element > i for element in self.board])
        return Board(transpose)
    
    # Returns two items, a bool which states if the board is player 1 winning, and a dict which takes the string representation of a board as a key and returns a dict which includes the board itself, and a bool which states if the board is player 1 winning
    def is_winning(self, checked_boards: dict = {}):
        # BASE CASE: The empty board is considered player 1 winning
        if sum(self) == 1:
            checked_boards[self.string_rep] = {'board': self, 'win_flag': False}
            return(False, checked_boards)
        # If board is in checked boards, return win_flag from that board
        elif checked_boards.get(self.string_rep) != None:
            winning_flag = checked_boards[self.string_rep]['win_flag']
            return winning_flag, checked_boards
        # If board is not in checked boards and is not empty, check if all sub-boards are losing and if so, this board is player 1 winning
        else:
            # Identify whether all sub-boards of a given board are player 1 winning/losing
            sub_board_results = [sub_board.is_winning(checked_boards)[0] for sub_board in self.get_sub_boards()]
            winning_flag = not (sum(sub_board_results) == len(sub_board_results)) # If all sub-boards of board are LOSING then the board is winning
            checked_boards[self.string_rep] = {'board': self, 'win_flag': winning_flag} # Add this board to the checked boards

            # If a board is player 1 winning/losing, then so is the transpose of that board, so add the transpose to the checked boards with the same winning_flag value
            board_transpose = self.transpose()
            if checked_boards.get(board_transpose.string_rep) == None:
                checked_boards[board_transpose.string_rep] = {'board': board_transpose, 'win_flag': winning_flag}
            return winning_flag, checked_boards
        
if __name__ == '__main__':
    size = 2
    board = Board([size] * size)
    win_flag, checked_boards = board.is_winning()

    # Generate a list containing all valid boards up to (size x size)
    all_boards = get_boards(size, size)
    for i in range(len(all_boards)):
        board = all_boards[i]
        if 0 in board:
            all_boards[i] = [element for element in board if element != 0]
    all_boards.remove([])

    # For each board in our list of boards, generate the string representation of the board for hashing later
    # output: ['1', '1,1', '2', '2,1', '2,2']
    board_keys = [''.join([str(element) + ',' for element in board])[:-1] for board in all_boards]

    # Enumerate the string representations of the boards and place them in a dict with the string representation as the key
    # output: {'1': 0, '1,1': 1, '2': 2, '2,1': 3, '2,2': 4}
    board_index_hash = {}
    for index, key in enumerate(board_keys):
        board_index_hash[key] = index

    # For each board generate the list of indices that represent all boards we can reach in one move
    # Output: [[], [0], [0], [1, 2], [1, 2, 3]]
    connections = [[board_index_hash[sub_board.string_rep] for sub_board in checked_boards[board_key]['board'].get_sub_boards()] for board_key in board_keys]

    import numpy as np
    adjacency_matrix = np.zeros((len(board_keys), len(board_keys)))
    for row_index in range(len(connections)):
        for connection in connections[row_index]:
            adjacency_matrix[row_index, connection] = 1

    print(adjacency_matrix)

    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize = (10, 10))
    # plt.imshow(adjacency_matrix)
    # plt.show()

    print_board(adjacency_matrix.astype(bool))