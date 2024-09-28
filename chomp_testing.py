from chomp_logic import *
import numpy as np

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

board = BitBoard(size = (2, 2))
win_flag, checked_boards = board.is_winning()
board_keys = [*checked_boards.keys()]

board_index_hash = {}
i = 0
for key in board_keys:
    board_index_hash[key] = i
    i += 1

connections = {}
for board_key in board_keys:
    board = checked_boards[board_key]['board_state']
    connections[board_index_hash[board_key]] = [board_index_hash[board] for board in board.get_sub_boards(keys = True)]
#del(connections[''])

adjacency_matrix = np.zeros((len(board_keys), len(board_keys)))
for key in connections.keys():
    for connection in connections[key]:
        adjacency_matrix[key, connection] = 1

print_board(adjacency_matrix.astype(bool))