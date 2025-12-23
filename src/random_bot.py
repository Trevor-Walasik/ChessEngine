from board import Board
import copy
import time
import tensorflow as tf
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt
import numpy as np

'''
input layer is one-hot encoded with the following representations
0000 = no piece
0001 = white pawn
0010 = white knight
0011 = white bishop
0100 = white rook
0101 = white queen
0110 = white king

'''

mapping = {
    "": [0, 0, 0, 0],
    "wp": [0, 0, 0, 1],
    "wn": [0, 0, 1, 0],
    "wb": [0, 0, 1, 1],
    "wr": [0, 1, 0, 0],
    "wq": [0, 1, 0, 1],
    "wk": [0, 1, 1, 0],
    "bp": [1, 0, 0, 1],
    "bn": [1, 0, 1, 0],
    "bb": [1, 0, 1, 1],
    "br": [1, 1, 0, 0],
    "bq": [1, 1, 0, 1],
    "bk": [1, 1, 1, 0],
}

def tensor_to_hueristic(tens, white):
    tens = tens.numpy()
    if white:
        return tens[0][0] - tens[0][2]
    else:
        return tens[0][2] - tens[0][0]


def board_to_input_array(game_state):
    layer = []
    for i in range(8):
        for j in range(8):
            layer.extend(mapping[game_state[i][j]])
    return layer

def simulate_game(model, sleep_time = None):
    board = Board()

    while board.game_loop():
        best_move = None
        best_move_val = -1
        for move in board.moves:
            if move[-1] == "#":
                best_move = move
                break

            temp_board = copy.deepcopy(board)

            temp_board.make_move(move)
            input = board_to_input_array(temp_board.game_state)
            input = tf.expand_dims(input, axis=0)

            huer = tensor_to_hueristic(model(np.array(input), training = False), board.white_to_play)
            if huer > best_move_val:    
                best_move_val = huer
                best_move = move

        board.make_move(best_move)
        board.white_to_play = not board.white_to_play
        if sleep_time:
            time.sleep(sleep_time)

    if board.white_wins:
        print("White Wins")
    elif board.black_wins:
        print("Black Wins")
    else:
        print("Draw")

if __name__ == "__main__":
    model = models.Sequential([
        layers.Flatten(input_shape = (256,)),
        layers.Dense(128, activation = 'relu'),
        layers.Dense(64, activation = 'relu'),
        layers.Dense(3, activation = 'softmax')
    ])
    simulate_game(model, .5)