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

    # Update and return self.moves set with all legal moves from current position
    def legal_moves(self):
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
                        self.calculate_bishop_moves(i,j)
                else:
                    if self.game_state[i][j] == "bp":
                        self.calculate_pawn_moves(i, j)
                    if self.game_state[i][j] == "br":
                        self.calculate_rook_moves(i, j)
                    if self.game_state[i][j] == "bk":
                        self.calculate_king_moves(i, j)
                    if self.game_state[i][j] == "bb":
                        self.calculate_bishop_moves(i,j)
        
        self.add_pawn_promotion()
        self.check_moves()

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

    # If any move results in opposing side having a king captures move, move is illegal, this function removes
    def check_moves(self):
        pass

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
                    self.moves[f"R{self.find_rook_ambig(i, j, new_i, j)}x{move_map[j]}{new_i + 1}"]
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

            self.prev_move = move
            return True
        else:
            return False
        
    def make_pawn_move(self, move):
        '''pawn move'''
        if move[1] != 'x':
            '''pawn advance'''
            new_j = rev_move_map[move[0]]
            new_i = int(move[1]) - 1
            if self.white_to_play:
                if move[-2] == "=":
                    self.game_state[new_i][new_j] = f"w{move[-1].lower()}"
                    self.game_state[new_i - 1][new_j] = ""
                else:
                    self.game_state[new_i][new_j] = "wp"
                    if self.game_state[new_i - 1][new_j] == "wp":
                        self.game_state[new_i - 1][new_j] = ""
                    else:
                        self.game_state[new_i - 2][new_j] = ""
            else:
                if move[-2] == "=":
                    self.game_state[new_i][new_j] = f"b{move[-1].lower()}"
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
                    if move[-2] == "=":
                        self.game_state[new_i][new_j] = f"w{move[-1].lower()}"
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
                    if move[-2] == "=":
                        self.game_state[new_i][new_j] = f"b{move[-1].lower()}"
                        self.game_state[new_i + 1][prev_j] = ""
                    else:
                        self.game_state[new_i][new_j] = "bp"
                        self.game_state[new_i + 1][prev_j] = ""
                else:
                    self.game_state[new_i][new_j] = "bp"
                    self.game_state[new_i + 1][new_j] = ""
                    self.game_state[new_i + 1][prev_j] = ""

    def make_rook_move(self, move):
        i, j = self.moves[move]
        new_i = int(move[-1]) - 1
        new_j = rev_move_map[move[-2]]
        self.game_state[i][j] = ""
        if self.white_to_play:
            self.game_state[new_i][new_j] = "wr"
        else:
            self.game_state[new_i][new_j] = "br"

    def make_king_move(self, move):
        i, j = self.moves[move]
        new_i = int(move[-1]) - 1
        new_j = rev_move_map[move[-2]]
        self.game_state[i][j] = ""
        if self.white_to_play:
            self.game_state[new_i][new_j] = "wk"
        else:
            self.game_state[new_i][new_j] = "bk"

    def make_bishop_move(self, move):
        i, j = self.moves[move]
        new_i = int(move[-1]) - 1
        new_j = rev_move_map[move[-2]]
        self.game_state[i][j] = ""
        if self.white_to_play:
            self.game_state[new_i][new_j] = "wb"
        else:
            self.game_state[new_i][new_j] = "bb"

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