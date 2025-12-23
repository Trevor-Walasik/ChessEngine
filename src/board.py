import copy

move_map = {
    0:"a",
    1:"b",
    2:"c",
    3:"d",
    4:"e",
    5:"f",
    6:"g",
    7:"h"
}

rev_move_map = {
    "a":0,
    "b":1,
    "c":2,
    "d":3,
    "e":4,
    "f":5,
    "g":6,
    "h":7
}

class Board:
    # Initialize Board object with fresh game state
    def __init__(self):
        self.prev_move = ""
        self.white_castle_long_rights = True
        self.white_castle_short_rights = True
        self.black_castle_long_rights = True
        self.black_castle_short_rights = True
        self.white_to_play = True
        self.score = 0

        self.game_state = [
            ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
        ]

    def legal_moves(self):
        self.potential_moves()
        self.check_legality()
        self.add_checks()

    # Update and return self.moves set with all legal moves from current position
    def potential_moves(self):
        self.moves = dict()

        for i in range(8):
            for j in range(8):
                if self.white_to_play:
                    if self.game_state[i][j] == "wp":
                        self.calculate_pawn_moves(i, j)
                    if self.game_state[i][j] == "wr":
                        self.calculate_rook_moves(i, j)
                    if self.game_state[i][j] == "wk":
                        self.calculate_king_moves(i, j)
                    if self.game_state[i][j] == "wb":
                        self.calculate_bishop_moves(i, j)
                    if self.game_state[i][j] == "wn":
                        self.calculate_knight_moves(i, j)
                    if self.game_state[i][j] == "wq":
                        self.calculate_queen_moves(i, j)
                    
                    self.calculate_castles(0, 4)
                else:
                    if self.game_state[i][j] == "bp":
                        self.calculate_pawn_moves(i, j)
                    if self.game_state[i][j] == "br":
                        self.calculate_rook_moves(i, j)
                    if self.game_state[i][j] == "bk":
                        self.calculate_king_moves(i, j)
                    if self.game_state[i][j] == "bb":
                        self.calculate_bishop_moves(i, j)
                    if self.game_state[i][j] == "bn":
                        self.calculate_knight_moves(i, j)
                    if self.game_state[i][j] == "bq":
                        self.calculate_queen_moves(i, j)

                    self.calculate_castles(7, 4)
        
        self.add_pawn_promotion()

    def add_pawn_promotion(self):
        new_moves = dict()
        moves_to_remove = set()
        for move in self.moves:
            i, j = self.moves[move]
            if self.white_to_play:
                if move[0] in rev_move_map and move[-1] == "8":
                    new_moves[move + "=N"] = (i, j)
                    new_moves[move + "=B"] = (i, j)
                    new_moves[move + "=R"] = (i, j)
                    new_moves[move + "=Q"] = (i, j) 
                    moves_to_remove.add(move)
            else: 
                if move[0] in rev_move_map and move[-1] == "1":
                    new_moves[move + "=N"] = (i, j)
                    new_moves[move + "=B"] = (i, j)
                    new_moves[move + "=R"] = (i, j)
                    new_moves[move + "=Q"] = (i, j) 
                    moves_to_remove.add(move)

        for key, value in new_moves.items():
            self.moves[key] = value
            
        for move in moves_to_remove:
            del self.moves[move]

    # Check which moves result in a poition in which opposing side could capture king and remove 
    def check_legality(self):
        moves_to_del = set()

        for move in self.moves:
            temp_board = copy.deepcopy(self)
            temp_board.make_move(move)
            temp_board.white_to_play = not temp_board.white_to_play

            for i in range(8):
                for j in range(8):
                    if self.white_to_play and temp_board.game_state[i][j] == "wk":
                        king_i, king_j = i, j
                    if not self.white_to_play and temp_board.game_state[i][j] == "bk":
                        king_i, king_j = i, j

            temp_board.potential_moves()

            for pot_move in temp_board.moves:
                if len(pot_move) > 2 and pot_move[-3:] == f"x{move_map[king_j]}{king_i + 1}":
                    moves_to_del.add(move)
                    break

        for move in moves_to_del:
            del self.moves[move]

        self.remove_bad_castles()

    def remove_bad_castles(self):
        if self.prev_move and self.prev_move[-1] == "+":
            if "O-O" in self.moves:
                del self.moves["O-O"]
            if "O-O+" in self.moves:
                del self.moves["O-O"]
            if "O-O-O" in self.moves:
                del self.moves["O-O-O"]
            if "O-O-O+" in self.moves:
                del self.moves["O-O"]

        temp_board = copy.deepcopy(self)
        
        if self.white_to_play:
            temp_board.white_to_play = False
            temp_board.potential_moves()
            for move in temp_board.moves:
                if move[-2:] == "f1":
                    if "O-O" in self.moves:
                        del self.moves["O-O"]
                    if "O-O+" in self.moves:
                        del self.moves["O-O"]

                if move[-2:] == "c1" or move[-2:] == "d1":
                    if "O-O-O" in self.moves:
                        del self.moves["O-O-O"]
                    if "O-O-O+" in self.moves:
                        del self.moves["O-O"]

        else:
            temp_board.white_to_play = True
            temp_board.potential_moves()
            for move in temp_board.moves:
                if move[-2:] == "f8":
                    if "O-O" in self.moves:
                        del self.moves["O-O"]
                    if "O-O+" in self.moves:
                        del self.moves["O-O"]

                if move[-2:] == "c8" or move[-2:] == "d8":
                    if "O-O-O" in self.moves:
                        del self.moves["O-O-O"]
                    if "O-O-O+" in self.moves:
                        del self.moves["O-O"]

    # See which moves result in checks and add + if they do
    def add_checks(self):
        changes = {}
        for i in range(8):
            for j in range(8):
                if self.white_to_play and self.game_state[i][j] == "bk":
                    king_i, king_j = i, j
                if not self.white_to_play and self.game_state[i][j] == "wk":
                    king_i, king_j = i, j

        for move in self.moves:
            temp_board = copy.deepcopy(self)
            temp_board.make_move(move)
            temp_board.potential_moves()
            for pot_move in temp_board.moves:
                if len(pot_move) > 2 and pot_move[-3:] == f"x{move_map[king_j]}{king_i + 1}":
                    temp_board.white_to_play = not temp_board.white_to_play
                    temp_board.potential_moves()
                    temp_board.legal_moves()
                    
                    if temp_board.moves:
                        changes[move] = move + "+"
                    else:
                        changes[move] = move + "#" 

                    break

        for key, value in changes.items():
            self.moves[value] = self.moves[key]
            del self.moves[key]    

    def calculate_pawn_moves(self, i, j):
        if self.white_to_play:
            if i == 1:
                if not self.game_state[i + 1][j] and not self.game_state[i + 2][j]:
                    self.moves[f"{move_map[j]}{i + 2}"] = (i, j)
                    self.moves[f"{move_map[j]}{i + 3}"] = (i, j)
            else:
                if i + 1 < 8 and not self.game_state[i + 1][j]:
                    self.moves[f"{move_map[j]}{i + 2}"] = (i, j)
            
            if i + 1 < 8 and j + 1 < 8 and \
               self.game_state[i + 1][j + 1] and self.game_state[i + 1][j + 1][0] == "b":
                self.moves[f"{move_map[j]}x{move_map[j + 1]}{i + 2}"] = (i, j)

            if i + 1 < 8 and j - 1 > -1 and \
               self.game_state[i + 1][j - 1] and self.game_state[i + 1][j - 1][0] == "b":
                self.moves[f"{move_map[j]}x{move_map[j - 1]}{i + 2}"] = (i, j)
            
            if i == 4:
                if self.prev_move[1] == "5" and j - 1 > -1 and \
                   rev_move_map[self.prev_move[0]] == j - 1:
                    self.moves[f"{move_map[j]}x{move_map[j - 1]}{i + 2}"] = (i, j)

                if self.prev_move[1] == "5" and j + 1 < 8 and \
                   rev_move_map[self.prev_move[0]] == j + 1:
                    self.moves[f"{move_map[j]}x{move_map[j + 1]}{i + 2}"] = (i, j)
                    
        else:
            if i == 6:
                if not self.game_state[i - 1][j] and not self.game_state[i - 2][j]:
                    self.moves[f"{move_map[j]}{i}"] = (i, j)
                    self.moves[f"{move_map[j]}{i - 1}"] = (i, j)
            else:
                if i - 1 > -1 and not self.game_state[i - 1][j]:
                    self.moves[f"{move_map[j]}{i}"] = (i, j)

            if i - 1 > -1 and j + 1 < 8 and \
               self.game_state[i - 1][j + 1] and self.game_state[i - 1][j + 1][0] == "w":
                self.moves[f"{move_map[j]}x{move_map[j + 1]}{i}"] = (i, j)

            if i - 1 > -1 and j - 1 > -1 and \
               self.game_state[i - 1][j - 1] and self.game_state[i - 1][j - 1][0] == "w":
                self.moves[f"{move_map[j]}x{move_map[j - 1]}{i}"] = (i, j)

            if i == 3:
                if self.prev_move[1] == "4" and j - 1 > -1 and \
                   rev_move_map[self.prev_move[0]] == j - 1:
                    self.moves[f"{move_map[j]}x{move_map[j - 1]}{i}"] = (i, j)

                if self.prev_move[1] == "4" and j + 1 < 8 and \
                   rev_move_map[self.prev_move[0]] == j + 1:
                    self.moves[f"{move_map[j]}x{move_map[j + 1]}{i}"] = (i, j)
   
    def calculate_rook_moves(self, i, j):
        for new_i in range(i + 1, 8):
            if self.game_state[new_i][j]:
                if self.game_state[new_i][j][0] == "b" and self.white_to_play or \
                    self.game_state[new_i][j][0] == "w" and not self.white_to_play:
                    self.moves[f"R{self.find_rook_ambig(i, j, new_i, j)}x{move_map[j]}{new_i + 1}"] = (i, j)
                break
            else:
                self.moves[f"R{self.find_rook_ambig(i, j, new_i, j)}{move_map[j]}{new_i + 1}"] = (i, j)

        for new_i in range(i - 1, -1, -1):
            if self.game_state[new_i][j]:
                if self.game_state[new_i][j][0] == "b" and self.white_to_play or \
                    self.game_state[new_i][j][0] == "w" and not self.white_to_play:
                    self.moves[f"R{self.find_rook_ambig(i, j, new_i, j)}x{move_map[j]}{new_i + 1}"] = (i, j)
                break
            else:
                self.moves[f"R{self.find_rook_ambig(i, j, new_i, j)}{move_map[j]}{new_i + 1}"] = (i, j)

        for new_j in range(j + 1, 8):
            if self.game_state[i][new_j]:
                if self.game_state[i][new_j][0] == "b" and self.white_to_play or \
                self.game_state[i][new_j][0] == "w" and not self.white_to_play:
                    self.moves[f"R{self.find_rook_ambig(i, j, i, new_j)}x{move_map[new_j]}{i + 1}"] = (i, j)  
                break
            else:
                self.moves[f"R{self.find_rook_ambig(i, j, i, new_j)}{move_map[new_j]}{i + 1}"] = (i, j)

        for new_j in range(j - 1, -1, -1):
            if self.game_state[i][new_j]:
                if self.game_state[i][new_j][0] == "b" and self.white_to_play or \
                self.game_state[i][new_j][0] == "w" and not self.white_to_play:
                    self.moves[f"R{self.find_rook_ambig(i, j, i, new_j)}x{move_map[new_j]}{i + 1}"] = (i, j)
                break
            else:
                self.moves[f"R{self.find_rook_ambig(i, j, i, new_j)}{move_map[new_j]}{i + 1}"] = (i, j)


        a1 = ""
        a2 = ""
        for new_j in range(j + 1, 8):
            if self.game_state[i][new_j]:
                a1 = self.game_state[i][new_j]
                break

        for new_j in range(j - 1, -1, -1):
            if self.game_state[i][new_j]:
                a2 = self.game_state[i][new_j]
                break

        if a1 == a2 and (a1 == "wr" or a1 == "br"):
            return True        
        else:
            return False

    def calculate_king_moves(self, i, j):
        if i + 1 < 8 and j - 1 > -1:
            if self.game_state[i + 1][j - 1]:
                if (self.game_state[i + 1][j - 1][0] == "b" and self.white_to_play) or \
                   (self.game_state[i + 1][j - 1][0] == "w" and not self.white_to_play):
                    self.moves[f"Kx{move_map[j - 1]}{i + 2}"] = (i, j)
            else:
                self.moves[f"K{move_map[j - 1]}{i + 2}"] = (i, j)

        if i + 1 < 8:
            if self.game_state[i + 1][j]:
                if (self.game_state[i + 1][j][0] == "b" and self.white_to_play) or \
                   (self.game_state[i + 1][j][0] == "w" and not self.white_to_play):
                    self.moves[f"Kx{move_map[j]}{i + 2}"] = (i, j)
            else:
                self.moves[f"K{move_map[j]}{i + 2}"] = (i, j)

        if i + 1 < 8 and j + 1 < 8:
            if self.game_state[i + 1][j + 1]:
                if (self.game_state[i + 1][j + 1][0] == "b" and self.white_to_play) or \
                   (self.game_state[i + 1][j + 1][0] == "w" and not self.white_to_play):
                    self.moves[f"Kx{move_map[j + 1]}{i + 2}"] = (i, j)
            else:
                self.moves[f"K{move_map[j + 1]}{i + 2}"] = (i, j)

        if j - 1 > - 1:
            if self.game_state[i][j - 1]:
                if (self.game_state[i][j - 1][0] == "b" and self.white_to_play) or \
                   (self.game_state[i][j - 1][0] == "w" and not self.white_to_play):
                    self.moves[f"Kx{move_map[j - 1]}{i + 1}"] = (i, j)
            else:
                self.moves[f"K{move_map[j - 1]}{i + 1}"] = (i, j)

        if j + 1 < 8:
            if self.game_state[i][j + 1]:
                if (self.game_state[i][j + 1][0] == "b" and self.white_to_play) or \
                   (self.game_state[i][j + 1][0] == "w" and not self.white_to_play):
                    self.moves[f"Kx{move_map[j + 1]}{i + 1}"] = (i, j)
            else:
                self.moves[f"K{move_map[j + 1]}{i + 1}"] = (i, j)

        if i - 1 > -1 and j - 1 > -1:
            if self.game_state[i - 1][j - 1]:
                if (self.game_state[i - 1][j - 1][0] == "b" and self.white_to_play) or \
                   (self.game_state[i - 1][j - 1][0] == "w" and not self.white_to_play):
                    self.moves[f"Kx{move_map[j - 1]}{i}"] = (i, j)
            else:
                self.moves[f"K{move_map[j - 1]}{i}"] = (i, j)

        if i - 1 > -1:
            if self.game_state[i - 1][j]:
                if (self.game_state[i - 1][j][0] == "b" and self.white_to_play) or \
                   (self.game_state[i - 1][j][0] == "w" and not self.white_to_play):
                    self.moves[f"Kx{move_map[j]}{i}"] = (i, j)
            else:
                self.moves[f"K{move_map[j]}{i}"] = (i, j)

        if i - 1 > -1 and j + 1 < 8:
            if self.game_state[i - 1][j + 1]:
                if (self.game_state[i - 1][j + 1][0] == "b" and self.white_to_play) or \
                   (self.game_state[i - 1][j + 1][0] == "w" and not self.white_to_play):
                    self.moves[f"Kx{move_map[j + 1]}{i}"] = (i, j)
            else:
                self.moves[f"K{move_map[j + 1]}{i}"] = (i, j)

    def calculate_bishop_moves(self, i, j):
        new_i = i + 1
        new_j = j + 1
        while new_i < 8 and new_j < 8:
            if self.game_state[new_i][new_j]:
                if (self.game_state[new_i][new_j][0] == "b" and self.white_to_play) \
                   or (self.game_state[new_i][new_j][0] == "w" and not self.white_to_play):
                    self.moves[f"B{self.find_bishop_ambig(i, j, new_i, new_j)}x{move_map[new_j]}{new_i + 1}"] = (i, j)
                break
            else:
                self.moves[f"B{self.find_bishop_ambig(i, j, new_i, new_j)}{move_map[new_j]}{new_i + 1}"] = (i, j)
                new_i += 1
                new_j += 1

        new_i = i + 1
        new_j = j - 1
        while new_i < 8 and new_j > -1:
            if self.game_state[new_i][new_j]:
                if (self.game_state[new_i][new_j][0] == "b" and self.white_to_play) \
                   or (self.game_state[new_i][new_j][0] == "w" and not self.white_to_play):
                    self.moves[f"B{self.find_bishop_ambig(i, j, new_i, new_j)}x{move_map[new_j]}{new_i + 1}"] = (i, j)
                break
            else:
                self.moves[f"B{self.find_bishop_ambig(i, j, new_i, new_j)}{move_map[new_j]}{new_i + 1}"] = (i, j)
                new_i += 1
                new_j -= 1

        new_i = i - 1
        new_j = j + 1
        while new_i > -1 and new_j < 8:
            if self.game_state[new_i][new_j]:
                if (self.game_state[new_i][new_j][0] == "b" and self.white_to_play) \
                   or (self.game_state[new_i][new_j][0] == "w" and not self.white_to_play):
                    self.moves[f"B{self.find_bishop_ambig(i, j, new_i, new_j)}x{move_map[new_j]}{new_i + 1}"] = (i, j)
                break
            else:
                self.moves[f"B{self.find_bishop_ambig(i, j, new_i, new_j)}{move_map[new_j]}{new_i + 1}"] = (i, j)
                new_i -= 1
                new_j += 1

        new_i = i - 1
        new_j = j - 1
        while new_i > -1 and new_j > -1:
            if self.game_state[new_i][new_j]:
                if (self.game_state[new_i][new_j][0] == "b" and self.white_to_play) \
                   or (self.game_state[new_i][new_j][0] == "w" and not self.white_to_play):
                    self.moves[f"B{self.find_bishop_ambig(i, j, new_i, new_j)}x{move_map[new_j]}{new_i + 1}"] = (i, j)
                break
            else:
                self.moves[f"B{self.find_bishop_ambig(i, j, new_i, new_j)}{move_map[new_j]}{new_i + 1}"] = (i, j)
                new_i -= 1
                new_j -= 1

    def calculate_knight_moves(self, i, j):
        new_i = i + 2
        new_j = j + 1
        if new_i < 8 and new_j < 8:
            if self.game_state[new_i][new_j]:
                if (self.game_state[new_i][new_j][0] == "b" and self.white_to_play) or \
                   (self.game_state[new_i][new_j][0] == "w" and not self.white_to_play):
                    self.moves[f"N{self.find_knight_ambig(i, j, new_i, new_j)}x{move_map[new_j]}{new_i + 1}"] = (i, j)
            else:
                self.moves[f"N{self.find_knight_ambig(i, j, new_i, new_j)}{move_map[new_j]}{new_i + 1}"] = (i, j)

        new_i = i + 2
        new_j = j - 1
        if new_i < 8 and new_j > -1:
            if self.game_state[new_i][new_j]:
                if (self.game_state[new_i][new_j][0] == "b" and self.white_to_play) or \
                   (self.game_state[new_i][new_j][0] == "w" and not self.white_to_play):
                    self.moves[f"N{self.find_knight_ambig(i, j, new_i, new_j)}x{move_map[new_j]}{new_i + 1}"] = (i, j)
            else:
                self.moves[f"N{self.find_knight_ambig(i, j, new_i, new_j)}{move_map[new_j]}{new_i + 1}"] = (i, j)
            

        new_i = i + 1
        new_j = j - 2
        if new_i < 8 and new_j > -1:
            if self.game_state[new_i][new_j]:
                if (self.game_state[new_i][new_j][0] == "b" and self.white_to_play) or \
                   (self.game_state[new_i][new_j][0] == "w" and not self.white_to_play):
                    self.moves[f"N{self.find_knight_ambig(i, j, new_i, new_j)}x{move_map[new_j]}{new_i + 1}"] = (i, j)
            else:
                self.moves[f"N{self.find_knight_ambig(i, j, new_i, new_j)}{move_map[new_j]}{new_i + 1}"] = (i, j)

        new_i = i - 1
        new_j = j - 2
        if new_i > -1 and new_j > -1:
            if self.game_state[new_i][new_j]:
                if (self.game_state[new_i][new_j][0] == "b" and self.white_to_play) or \
                   (self.game_state[new_i][new_j][0] == "w" and not self.white_to_play):
                    self.moves[f"N{self.find_knight_ambig(i, j, new_i, new_j)}x{move_map[new_j]}{new_i + 1}"] = (i, j)
            else:
                self.moves[f"N{self.find_knight_ambig(i, j, new_i, new_j)}{move_map[new_j]}{new_i + 1}"] = (i, j)

        new_i = i + 1
        new_j = j + 2
        if new_i < 8 and new_j < 8:
            if self.game_state[new_i][new_j]:
                if (self.game_state[new_i][new_j][0] == "b" and self.white_to_play) or \
                   (self.game_state[new_i][new_j][0] == "w" and not self.white_to_play):
                    self.moves[f"N{self.find_knight_ambig(i, j, new_i, new_j)}x{move_map[new_j]}{new_i + 1}"] = (i, j)
            else:
                self.moves[f"N{self.find_knight_ambig(i, j, new_i, new_j)}{move_map[new_j]}{new_i + 1}"] = (i, j)

        new_i = i - 1
        new_j = j + 2
        if new_i > -1 and new_j < 8:
            if self.game_state[new_i][new_j]:
                if (self.game_state[new_i][new_j][0] == "b" and self.white_to_play) or \
                   (self.game_state[new_i][new_j][0] == "w" and not self.white_to_play):
                    self.moves[f"N{self.find_knight_ambig(i, j, new_i, new_j)}x{move_map[new_j]}{new_i + 1}"] = (i, j)
            else:
                self.moves[f"N{self.find_knight_ambig(i, j, new_i, new_j)}{move_map[new_j]}{new_i + 1}"] = (i, j)

        new_i = i - 2
        new_j = j + 1
        if new_i > -1 and new_j < 8:
            if self.game_state[new_i][new_j]:
                if (self.game_state[new_i][new_j][0] == "b" and self.white_to_play) or \
                   (self.game_state[new_i][new_j][0] == "w" and not self.white_to_play):
                    self.moves[f"N{self.find_knight_ambig(i, j, new_i, new_j)}x{move_map[new_j]}{new_i + 1}"] = (i, j)
            else:
                self.moves[f"N{self.find_knight_ambig(i, j, new_i, new_j)}{move_map[new_j]}{new_i + 1}"] = (i, j)

        new_i = i - 2
        new_j = j - 1
        if new_i > -1 and new_j > -1:
            if self.game_state[new_i][new_j]:
                if (self.game_state[new_i][new_j][0] == "b" and self.white_to_play) or \
                   (self.game_state[new_i][new_j][0] == "w" and not self.white_to_play):
                    self.moves[f"N{self.find_knight_ambig(i, j, new_i, new_j)}x{move_map[new_j]}{new_i + 1}"] = (i, j)
            else:
                self.moves[f"N{self.find_knight_ambig(i, j, new_i, new_j)}{move_map[new_j]}{new_i + 1}"] = (i, j)

    def calculate_queen_moves(self, i, j):
        for new_i in range(i + 1, 8):
            if self.game_state[new_i][j]:
                if self.game_state[new_i][j][0] == "b" and self.white_to_play or \
                    self.game_state[new_i][j][0] == "w" and not self.white_to_play:
                    self.moves[f"Q{self.find_rook_ambig(i, j, new_i, j)}x{move_map[j]}{new_i + 1}"] = (i, j)
                break
            else:
                self.moves[f"Q{self.find_rook_ambig(i, j, new_i, j)}{move_map[j]}{new_i + 1}"] = (i, j)

        for new_i in range(i - 1, -1, -1):
            if self.game_state[new_i][j]:
                if self.game_state[new_i][j][0] == "b" and self.white_to_play or \
                    self.game_state[new_i][j][0] == "w" and not self.white_to_play:
                    self.moves[f"Q{self.find_rook_ambig(i, j, new_i, j)}x{move_map[j]}{new_i + 1}"] = (i, j)
                break
            else:
                self.moves[f"Q{self.find_rook_ambig(i, j, new_i, j)}{move_map[j]}{new_i + 1}"] = (i, j)

        for new_j in range(j + 1, 8):
            if self.game_state[i][new_j]:
                if self.game_state[i][new_j][0] == "b" and self.white_to_play or \
                self.game_state[i][new_j][0] == "w" and not self.white_to_play:
                    self.moves[f"Q{self.find_rook_ambig(i, j, i, new_j)}x{move_map[new_j]}{i + 1}"] = (i, j)  
                break
            else:
                self.moves[f"Q{self.find_rook_ambig(i, j, i, new_j)}{move_map[new_j]}{i + 1}"] = (i, j)

        for new_j in range(j - 1, -1, -1):
            if self.game_state[i][new_j]:
                if self.game_state[i][new_j][0] == "b" and self.white_to_play or \
                self.game_state[i][new_j][0] == "w" and not self.white_to_play:
                    self.moves[f"Q{self.find_rook_ambig(i, j, i, new_j)}x{move_map[new_j]}{i + 1}"] = (i, j)
                break
            else:
                self.moves[f"Q{self.find_rook_ambig(i, j, i, new_j)}{move_map[new_j]}{i + 1}"] = (i, j)

        new_i = i + 1
        new_j = j + 1
        while new_i < 8 and new_j < 8:
            if self.game_state[new_i][new_j]:
                if (self.game_state[new_i][new_j][0] == "b" and self.white_to_play) \
                   or (self.game_state[new_i][new_j][0] == "w" and not self.white_to_play):
                    self.moves[f"Q{self.find_bishop_ambig(i, j, new_i, new_j)}x{move_map[new_j]}{new_i + 1}"] = (i, j)
                break
            else:
                self.moves[f"Q{self.find_bishop_ambig(i, j, new_i, new_j)}{move_map[new_j]}{new_i + 1}"] = (i, j)
                new_i += 1
                new_j += 1

        new_i = i + 1
        new_j = j - 1
        while new_i < 8 and new_j > -1:
            if self.game_state[new_i][new_j]:
                if (self.game_state[new_i][new_j][0] == "b" and self.white_to_play) \
                   or (self.game_state[new_i][new_j][0] == "w" and not self.white_to_play):
                    self.moves[f"Q{self.find_bishop_ambig(i, j, new_i, new_j)}x{move_map[new_j]}{new_i + 1}"] = (i, j)
                break
            else:
                self.moves[f"Q{self.find_bishop_ambig(i, j, new_i, new_j)}{move_map[new_j]}{new_i + 1}"] = (i, j)
                new_i += 1
                new_j -= 1

        new_i = i - 1
        new_j = j + 1
        while new_i > -1 and new_j < 8:
            if self.game_state[new_i][new_j]:
                if (self.game_state[new_i][new_j][0] == "b" and self.white_to_play) \
                   or (self.game_state[new_i][new_j][0] == "w" and not self.white_to_play):
                    self.moves[f"Q{self.find_bishop_ambig(i, j, new_i, new_j)}x{move_map[new_j]}{new_i + 1}"] = (i, j)
                break
            else:
                self.moves[f"Q{self.find_bishop_ambig(i, j, new_i, new_j)}{move_map[new_j]}{new_i + 1}"] = (i, j)
                new_i -= 1
                new_j += 1

        new_i = i - 1
        new_j = j - 1
        while new_i > -1 and new_j > -1:
            if self.game_state[new_i][new_j]:
                if (self.game_state[new_i][new_j][0] == "b" and self.white_to_play) \
                   or (self.game_state[new_i][new_j][0] == "w" and not self.white_to_play):
                    self.moves[f"Q{self.find_bishop_ambig(i, j, new_i, new_j)}x{move_map[new_j]}{new_i + 1}"] = (i, j)
                break
            else:
                self.moves[f"Q{self.find_bishop_ambig(i, j, new_i, new_j)}{move_map[new_j]}{new_i + 1}"] = (i, j)
                new_i -= 1
                new_j -= 1

    def calculate_castles(self, i, j):
        if self.white_castle_short_rights and self.white_to_play:
            if not self.game_state[0][5] and not self.game_state[0][6]:
                self.moves["O-O"] = (i, j)
        if self.white_castle_long_rights and self.white_to_play:
            if not self.game_state[0][1] and not self.game_state[0][2] and not self.game_state[0][3]:
                self.moves["O-O-O"] = (i, j)
        if self.black_castle_short_rights and not self.white_to_play:
            if not self.game_state[7][5] and not self.game_state[7][6]:
                self.moves["O-O"] = (i, j)
        if self.black_castle_long_rights and not self.white_to_play:
            if not self.game_state[7][1] and not self.game_state[7][2] and not self.game_state[7][3]:
                self.moves["O-O-O"] = (i, j)

    def find_rook_ambig(self, orig_i, orig_j, new_i, new_j):
        pieces_attacking_new = set()
        for i in range(new_i + 1, 8):
            if self.game_state[i][new_j]:
                pieces_attacking_new.add((i, new_j))
                break

        for i in range(new_i - 1, -1, -1):
            if self.game_state[i][new_j]:
                pieces_attacking_new.add((i, new_j))
                break

        for j in range(new_j + 1, 8):
            if self.game_state[new_i][j]:
                pieces_attacking_new.add((new_i, j))
                break

        for j in range(new_j - 1, -1, -1):
            if self.game_state[new_i][j]:
                pieces_attacking_new.add((new_i, j))
                break

        pieces_attacking_new.remove((orig_i, orig_j))

        general_ambig = False
        vert_ambig = False
        horz_ambig = False

        for temp_i, temp_j in pieces_attacking_new:
            if self.game_state[temp_i][temp_j] == self.game_state[orig_i][orig_j]:
                general_ambig = True
                if temp_j == orig_j:
                    vert_ambig = True
                if temp_i == orig_i:
                    horz_ambig = True

        if vert_ambig and horz_ambig:
            return f"{move_map[orig_j]}{orig_i + 1}"
        elif horz_ambig:
            return f"{move_map[orig_j]}"
        elif vert_ambig:
            return f"{orig_i + 1}"
        elif general_ambig:
            return f"{move_map[orig_j]}"
        else:
            return ""

    def find_bishop_ambig(self, orig_i, orig_j, new_i, new_j):
        pieces_attacking_new = set()

        i = new_i + 1
        j = new_j + 1
        while i < 8 and j < 8:
            if self.game_state[i][j]:
                pieces_attacking_new.add((i, j))
                break
            i += 1    
            j += 1

        i = new_i + 1
        j = new_j - 1
        while i < 8 and j > -1:
            if self.game_state[i][j]:
                pieces_attacking_new.add((i, j))
                break
            i += 1
            j -= 1

        i = new_i - 1
        j = new_j + 1
        while i > -1 and j < 8:
            if self.game_state[i][j]:
                pieces_attacking_new.add((i, j))
                break
            i -= 1
            j += 1

        i = new_i - 1
        j = new_j - 1
        while i > -1 and j > -1:
            if self.game_state[i][j]:
                pieces_attacking_new.add((i, j))
                break
            i -= 1
            j -= 1

        pieces_attacking_new.remove((orig_i, orig_j))

        general_ambig = False
        vert_ambig = False
        horz_ambig = False

        for temp_i, temp_j in pieces_attacking_new:
            if self.game_state[temp_i][temp_j] == self.game_state[orig_i][orig_j]:
                general_ambig = True
                if temp_j == orig_j:
                    vert_ambig = True
                if temp_i == orig_i:
                    horz_ambig = True

        if vert_ambig and horz_ambig:
            return f"{move_map[orig_j]}{orig_i + 1}"
        elif horz_ambig:
            return f"{move_map[orig_j]}"
        elif vert_ambig:
            return f"{orig_i + 1}"
        elif general_ambig:
            return f"{move_map[orig_j]}"
        else:
            return ""

    def find_knight_ambig(self, orig_i, orig_j, new_i, new_j):
        pieces_attacking_new = set()

        i = new_i + 2
        j = new_j + 1
        if i < 8 and j < 8:
            if self.game_state[i][j]:
                pieces_attacking_new.add((i, j))

        i = new_i + 2
        j = new_j - 1
        if i < 8 and j > -1:
            if self.game_state[i][j]:
                pieces_attacking_new.add((i, j))    
            
        i = new_i + 1
        j = new_j - 2
        if i < 8 and j > -1:
            if self.game_state[i][j]:
                pieces_attacking_new.add((i, j))        

        i = new_i - 1
        j = new_j - 2
        if i > -1 and j > -1:
            if self.game_state[i][j]:
                pieces_attacking_new.add((i, j))
                
        i = new_i + 1
        j = new_j + 2
        if i < 8 and j < 8:
            if self.game_state[i][j]:
                pieces_attacking_new.add((i, j))

        i = new_i - 1
        j = new_j + 2
        if i > -1 and j < 8:
            if self.game_state[i][j]:
                pieces_attacking_new.add((i, j))

        i = new_i - 2
        j = new_j + 1
        if i > -1 and j < 8:
            if self.game_state[i][j]:
                pieces_attacking_new.add((i, j))        

        i = new_i - 2
        j = new_j - 1
        if i > -1 and j > -1:
            if self.game_state[i][j]:
                pieces_attacking_new.add((i, j))

        pieces_attacking_new.remove((orig_i, orig_j))

        general_ambig = False
        vert_ambig = False
        horz_ambig = False

        for temp_i, temp_j in pieces_attacking_new:
            if self.game_state[temp_i][temp_j] == self.game_state[orig_i][orig_j]:
                general_ambig = True
                if temp_j == orig_j:
                    vert_ambig = True
                if temp_i == orig_i:
                    horz_ambig = True

        if vert_ambig and horz_ambig:
            return f"{move_map[orig_j]}{orig_i + 1}"
        elif horz_ambig:
            return f"{move_map[orig_j]}"
        elif vert_ambig:
            return f"{orig_i + 1}"
        elif general_ambig:
            return f"{move_map[orig_j]}"
        else:
            return ""

    def find_queen_ambig(self, orig_i, orig_j, new_i, new_j):
        diag = self.find_bishop_ambig(orig_i, orig_j, new_i, new_j)
        lat = self.find_rook_ambig(orig_i, orig_j, new_i, new_j)
        if len(diag) == 2:
            return diag
        elif len(lat) == 2:
            return lat
        elif len(diag) == 1 and not lat:
            return diag
        elif len(lat) == 1 and not diag:
            return lat
        elif len(lat) == 1 and len(diag) == 1:
            if lat.isalpha() and diag.isalpha():
                return lat
            elif lat.isnumeric() and diag.isnumeric():
                return lat
            else:
                if lat.isalpha():
                    return lat + diag
                else:
                    return diag + lat
        else:
            return ""

    def make_move(self, move):
        if move in self.moves:

            if move[0] in rev_move_map:
                self.make_pawn_move(move)
            elif move[0] == "R":
                self.make_rook_move(move)
            elif move[0] == "K":
                self.make_king_move(move)
            elif move[0] == "B":
                self.make_bishop_move(move)
            elif move[0] == "N":
                self.make_knight_move(move)
            elif move[0] == "Q":
                self.make_queen_move(move)
            elif move[0] == "O":
                self.make_castle(move)

            self.prev_move = move
            return True
        else:
            return False
        
    def make_pawn_move(self, move):
        if move[-1] in "+#":
            move_copy = move[:-1]
        else:
            move_copy = move
        '''pawn move'''
        if move[1] != 'x':
            '''pawn advance'''
            new_j = rev_move_map[move[0]]
            new_i = int(move[1]) - 1
            if self.white_to_play:
                if move[-2] == "=":
                    self.game_state[new_i][new_j] = f"w{move_copy[-1].lower()}"
                    self.game_state[new_i - 1][new_j] = ""
                else:
                    self.game_state[new_i][new_j] = "wp"
                    if self.game_state[new_i - 1][new_j] == "wp":
                        self.game_state[new_i - 1][new_j] = ""
                    else:
                        self.game_state[new_i - 2][new_j] = ""
            else:
                if move[-2] == "=":
                    self.game_state[new_i][new_j] = f"b{move_copy[-1].lower()}"
                    self.game_state[new_i + 1][new_j] = ""
                else:
                    self.game_state[new_i][new_j] = "bp"
                    if self.game_state[new_i + 1][new_j] == "bp":
                        self.game_state[new_i + 1][new_j] = ""
                    else:
                        self.game_state[new_i + 2][new_j] = ""
        else:
            '''pawn capture'''
            new_j = rev_move_map[move[2]]
            prev_j = rev_move_map[move[0]]
            new_i = int(move[3]) - 1
            if self.white_to_play:
                if self.game_state[new_i][new_j]:
                    if move_copy[-2] == "=":
                        self.game_state[new_i][new_j] = f"w{move_copy[-1].lower()}"
                        self.game_state[new_i - 1][prev_j] = ""
                    else:
                        self.game_state[new_i][new_j] = "wp"
                        self.game_state[new_i - 1][prev_j] = ""
                else:
                    self.game_state[new_i][new_j] = "wp"
                    self.game_state[new_i - 1][new_j] = ""
                    self.game_state[new_i - 1][prev_j] = ""
            else:
                if self.game_state[new_i][new_j]:
                    if move_copy[-2] == "=":
                        self.game_state[new_i][new_j] = f"b{move_copy[-1].lower()}"
                        self.game_state[new_i + 1][prev_j] = ""
                    else:
                        self.game_state[new_i][new_j] = "bp"
                        self.game_state[new_i + 1][prev_j] = ""
                else:
                    self.game_state[new_i][new_j] = "bp"
                    self.game_state[new_i + 1][new_j] = ""
                    self.game_state[new_i + 1][prev_j] = ""

    def make_rook_move(self, move):
        if move[-1] in "+#":
            move = move[:-1]
        else:
            move_copy = move
        i, j = self.moves[move]
        new_i = int(move[-1]) - 1
        new_j = rev_move_map[move[-2]]
        self.game_state[i][j] = ""
        if self.white_to_play:
            self.game_state[new_i][new_j] = "wr"
        else:
            self.game_state[new_i][new_j] = "br"

        if i == 0 and j == 0:
            self.white_castle_long_rights = False
        if i == 0 and j == 7:
            self.white_castle_short_rights = False
        if i == 7 and j == 0:
            self.black_castle_long_rights = False
        if i == 7 and j == 7:
            self.black_castle_short_rights = False

    def make_king_move(self, move):
        if move[-1] in "+#":
            move_copy = move[:-1]
        else:
            move_copy = move
        i, j = self.moves[move]
        new_i = int(move_copy[-1]) - 1
        new_j = rev_move_map[move_copy[-2]]
        self.game_state[i][j] = ""
        if self.white_to_play:
            self.game_state[new_i][new_j] = "wk"
            self.white_castle_long_rights = False
            self.white_castle_short_rights = False
        else:
            self.game_state[new_i][new_j] = "bk"
            self.black_castle_long_rights = False
            self.black_castle_short_rights = False

    def make_bishop_move(self, move):
        if move[-1] in "+#":
            move_copy = move[:-1]
        else:
            move_copy = move
        i, j = self.moves[move]
        new_i = int(move_copy[-1]) - 1
        new_j = rev_move_map[move_copy[-2]]
        self.game_state[i][j] = ""
        if self.white_to_play:
            self.game_state[new_i][new_j] = "wb"
        else:
            self.game_state[new_i][new_j] = "bb"

    def make_knight_move(self, move):
        if move[-1] in "+#":
            move_copy = move[:-1]
        else:
            move_copy = move
        i, j = self.moves[move]
        new_i = int(move_copy[-1]) - 1
        new_j = rev_move_map[move_copy[-2]]
        self.game_state[i][j] = ""
        if self.white_to_play:
            self.game_state[new_i][new_j] = "wn"
        else:
            self.game_state[new_i][new_j] = "bn"

    def make_queen_move(self, move):
        if move[-1] in "+#":
            move_copy = move[:-1]
        else:
            move_copy = move
        i, j = self.moves[move]
        new_i = int(move_copy[-1]) - 1
        new_j = rev_move_map[move_copy[-2]]
        self.game_state[i][j] = ""
        if self.white_to_play:
            self.game_state[new_i][new_j] = "wq"
        else:
            self.game_state[new_i][new_j] = "bq"

    def make_castle(self, move):
        if move[-1] in "+#":
            move = move[:-1]
        if len(move) == 3:
            if self.white_to_play:
                self.game_state[0][6] = "wk"
                self.game_state[0][5] = "wr"
                self.game_state[0][4] = ""
                self.game_state[0][7] = ""
            else:
                self.game_state[7][6] = "bk"
                self.game_state[7][5] = "br"
                self.game_state[7][4] = ""
                self.game_state[7][7] = ""
        else:
            if self.white_to_play:
                self.game_state[0][2] = "wk"
                self.game_state[0][3] = "wr"
                self.game_state[0][4] = ""
                self.game_state[0][0] = ""
            else:
                self.game_state[7][2] = "bk"
                self.game_state[7][3] = "br"
                self.game_state[7][4] = ""
                self.game_state[7][0] = ""

    def print_moves(self):
        print(self.moves.keys())

    def __str__(self):
        ret = ""
        for i in range(8):
            if self.white_to_play:
                ret += " " + "-"*41 + f"\n{8-i}|"
            else:
                ret += " " + "-"*41 + f"\n{i+1}|"
            for j in range(8):
                if self.white_to_play:
                    if self.game_state[7-i][j]:
                        ret += f" {self.game_state[7-i][j]} |"
                    else:
                        ret += "    |"
                else:
                    if self.game_state[i][j]:
                        ret += f" {self.game_state[i][j]} |"
                    else:
                        ret += "    |"
            ret += "\n"
        ret += " " + "-"*41 + "\n "
        for i in range(8):
            ret += f"  {move_map[i].upper()}  "
        return ret

if __name__ == "__main__":
    board = Board()
    while True:
        print(board)
        board.legal_moves()
        board.print_moves()
        while True:
            move = input("Enter move: ")
            if board.make_move(move):
                break
        board.white_to_play = not board.white_to_play