import numpy as np

class BitBoard():
    def __init__(self, board_state: np.ndarray = None, size: tuple = None):
        self.board = board_state
        if size != None:
            self.init_board(size)

        self.num_squares = self.board.shape[1]
        self.moves = list(zip(self.board[0, :], self.board[1, :]))

    def __repr__(self):
        return repr(self.board)
    
    def __eq__(self, comparison_board):
        return np.array_equal(self.board, comparison_board.board)

    # Tuple(int) -> np.array(int)
    # Create a size = (int, int) numpy array containing values of "True"
    def init_board(self, size: tuple) -> np.ndarray:
        self.board = np.array(np.where(np.ones(size, bool) == True))
        return self.board

    # size(int) -> np.array(bool)
    # Creates a martix representation of the board with values "True" if the board contains the point and "False" otherwise
    def board_representation(self, size: int = None) -> np.ndarray:
        if size == None:
            if self != BitBoard(size = (0, 0)):
                size = self.board.max() + 1
            else:
                size = 0
        board_rep = np.zeros((size, size), bool)
        for move in self.moves:
            board_rep[move] = True
        return board_rep
    
    # np.array -> str
    # Return a unique string which identifies the contents of the bit board for dict table lookups
    def hash_key(self):
        board_rep = self.board_representation().astype(str)
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
        return(hash_key)

    # np.array(int) -> BitBoard
    # Creates a BitBoard for the transpose of a given BitBoard
    def get_transpose(self) -> np.ndarray:
        transpose = np.array(np.where(self.board_representation().transpose() == True))
        return BitBoard(board_state = transpose)

    # tuple(int, int), opt in_place(bool) -> BitBoard
    # "Chomps" the board and removes all squares down and to the right of position
    def chomp(self, position: tuple, in_place: bool = False) -> np.ndarray:
        chomp_mask = (self.board[0] < position[0]) | (self.board[1] < position[1])
        sub_board = self.board[:, chomp_mask]
        if in_place == True:
            self.board = sub_board
        return BitBoard(board_state = sub_board)
    
    def get_sub_boards(self, keys = False, remove_empty_board = False):
        moves = self.moves
        if remove_empty_board == True and (0,0) in moves: moves.remove((0,0))

        if keys == True:
            return [self.chomp(move).hash_key() for move in moves]
        else:
            return [self.chomp(move) for move in moves]

    # BitBoard, dict(BitBoard, bool) -> bool, dict(BitBoard, bool)
    # Recursive function to identify if a given board is player 1 winning. Returns whether a board is winning and a dict containing all checked boards in the recursion.
    def is_winning(self, checked_boards: dict = {}):
        # BASE CASE: The empty board is considered player 1 winning
        if self == BitBoard(size = (0, 0)):
            checked_boards[self.hash_key()] = {'board_state': self, 'win_flag': True}
            return(True, checked_boards)
        # If board is in checked boards, return win_flag from that board
        elif checked_boards.get(self.hash_key()) != None:
            winning_flag = checked_boards[self.hash_key()]['win_flag']
            return winning_flag, checked_boards
        # If board is not in checked boards and is not empty, check if all sub-boards are losing and if so, this board is player 1 winning
        else:
            # Identify whether all sub-boards of a given board are player 1 winning/losing
            sub_board_results = [sub_board.is_winning(checked_boards)[0] for sub_board in self.get_sub_boards()]
            winning_flag = ~np.array(sub_board_results).all() # If all sub-boards of board are LOSING then the board is winning
            checked_boards[self.hash_key()] = {'board_state': self, 'win_flag': winning_flag} # Add this board to the checked boards

            # If a board is player 1 winning/losing, then so is the transpose of that board, so add the transpose to the checked boards with the same winning_flag value
            board_transpose = self.get_transpose()
            if checked_boards.get(board_transpose.hash_key()) == None:
                checked_boards[board_transpose.hash_key()] = {'board_state': board_transpose, 'win_flag': winning_flag}
            return winning_flag, checked_boards
        
    # I'm SO bad at trees, gonna need to do some LeetCode for this one
    def find_winning_path(self, checked_boards = {}):
        winning_path = None
        return winning_path


if __name__ == '__main__':
    max_rows = 30
    max_columns = 30
    column_indices = list(range(max_columns)) * max_rows
    row_indices = []
    for i in range(max_rows):
        row_indices += [i] * max_columns

    checked_boards = {}
    for h, w in zip(row_indices, column_indices):
        board = BitBoard(size = (h, w)).chomp((2, 2)).chomp((1, 2))
        win_flag, checked_boards = board.is_winning(checked_boards)
        if win_flag == False:
            print(h, w, win_flag)
            # print(board.hash_key())
            # print('\n')
    print(board)
    # board = BitBoard(size = (5,5)).chomp((2, 2))
    # print(board.is_winning()[0])
    # pass