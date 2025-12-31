from board import Board
import copy
import time
import random
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
    "": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "wp": [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    "wn": [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    "wb": [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    "wr": [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "wq": [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "wk": [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "bp": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    "bn": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    "bb": [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    "br": [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    "bq": [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    "bk": [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
}

def board_to_input_array(game_state):
    layer = []
    for i in range(8):
        for j in range(8):
            layer.extend(mapping[game_state[i][j]])
    return layer 

def simulate_game(model, sleep_time=None, extract_training=False, print_game=False, number_of_games=1):
    # Plan
    # Initialize return values for extract_training
    if extract_training:
        inputs = []
        outputs = []
        

    for i in range(number_of_games):
        score = []
        board = Board()
        while board.game_loop(print_game = print_game):
            if board.white_to_play:
                moves = []
                activations = []
                move_inputs = []

                for m in board.moves:
                    if m[-1] == "#":
                        activations.append(float(1000000))
                        move_input = board_to_input_array(board.game_state)
                    else:
                        temp = copy.deepcopy(board)
                        temp.make_move(m)
                        move_input = board_to_input_array(temp.game_state)
                        input_arr = np.array(move_input)
                        input_arr = np.expand_dims(input_arr, axis=0)
                        activation = model(input_arr, training=False)
                        activations.append(float(activation.numpy().flatten()[0]))
                    moves.append(m)
                    move_inputs.append(move_input)

                tensor_input = tf.convert_to_tensor(np.array(activations))
                softmax_output = tf.nn.softmax(tensor_input)
                probs = np.array(softmax_output).flatten()
                chosen_index = np.random.choice(len(moves), p=probs)

                board.make_move(moves[chosen_index])
                if extract_training:
                    inputs.append(move_inputs[chosen_index])
                    score.append(board.score)
                board.white_to_play = not board.white_to_play

            else:
                not_found = True
                for m in list(board.moves):
                    if m[-1] == "#":
                        board.make_move(m)
                        not_found = False
                if not_found:
                    board.make_move(random.choice(list(board.moves)))
                board.white_to_play = not board.white_to_play
        
        if board.white_wins:
            print("White Wins")
            game_outputs = [white_squish_function(s) for s in score]
            outputs.extend(game_outputs)
        elif board.black_wins:
            print("Black Wins")
            game_outputs = [-black_squish_function(s) for s in score]
            outputs.extend(game_outputs)
        else:
            print("Draw")
            game_outputs = [-black_squish_function(s) / 2 if s < 0 
                            else white_squish_function(s) / 2 
                            for s in score]
            outputs.extend(game_outputs)

    if extract_training:
        print(np.array(outputs))
        return (np.array(inputs), np.array(outputs))
        

def white_squish_function(x):
    if x >= 12:
        return 1
    if x <= -12:
        return 0
    return 1 / (1 + np.exp(-1.5 * (x - 4.5)))

def black_squish_function(x):
    if x >= 12:
        return 0
    if x <= -12:
        return 1
    return 1 / (1 + np.exp(1.5 * (x + 4.5)))

if __name__ == "__main__":
    '''
    model = models.Sequential([
        layers.Flatten(input_shape = (768,)),
        layers.Dense(768, activation = 'relu'),
        layers.Dense(2000, activation = 'relu'),
        layers.Dense(2000, activation = 'relu'),
        layers.Dense(2000, activation = 'relu'),
        layers.Dense(768, activation = 'relu'),
        layers.Dense(256, activation = 'relu'),
        layers.Dense(128, activation = 'relu'),
        layers.Dense(64, activation = 'relu'),
        layers.Dense(1)
    ])
    '''
    model = tf.keras.models.load_model('model.keras')
    for i in range(250):
        res = simulate_game(model, extract_training = True, print_game = False, number_of_games = 12)
        if res:
            x_train, y_train = res
            optimizer = tf.keras.optimizers.Adam(
                learning_rate=0.0001,
            )
            model.compile(
                optimizer=optimizer,
                loss='mean_absolute_error',
                metrics=['accuracy'],
            )
        
            model.fit(
                x_train, 
                y_train, 
                epochs=6,
                batch_size = (len(x_train) - 1)//6
            )   
        model.save('model.keras')

    model.save('model.keras')
