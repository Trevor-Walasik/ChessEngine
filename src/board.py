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
                else:
                    if self.game_state[i][j] == "bp":
                        self.calculate_pawn_moves(i, j)
                    if self.game_state[i][j] == "br":
                        self.calculate_rook_moves(i, j)
        
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
        new_move = ""
        for new_i in range(i + 1, 8):
            if self.game_state[new_i][j]:
                if self.game_state[new_i][j][0] == "b" and self.white_to_play or \
                    self.game_state[new_i][j][0] == "w" and not self.white_to_play:
                    new_move = f"Rx{move_map[j]}{new_i + 1}"
                else:
                    break

            else:
                new_move = f"R{move_map[j]}{new_i + 1}"

            if self.check_for_horz_ambig(new_i, j) and self.check_for_vert_ambig(new_i, j):
                new_move = "R" + f"{move_map[j]}{i + 1}" + new_move[1:]
            elif self.check_for_horz_ambig(new_i, j):
                new_move = "R" + f"{move_map[j]}" + new_move[1:]
            elif self.check_for_vert_ambig(new_i, j):
                new_move = "R" + f"{i + 1}" + new_move[1:]

            self.moves[new_move] = (i, j)

            if new_move[1] == "x":
                break

        for new_i in range(i - 1, -1, -1):
            if self.game_state[new_i][j]:
                if self.game_state[new_i][j][0] == "b" and self.white_to_play or \
                    self.game_state[new_i][j][0] == "w" and not self.white_to_play:
                    new_move = f"Rx{move_map[j]}{new_i + 1}"
                else:
                    break

            else:
                new_move = f"R{move_map[j]}{new_i + 1}"

            if self.check_for_horz_ambig(new_i, j) and self.check_for_vert_ambig(new_i, j):
                new_move = "R" + f"{move_map[j]}{i + 1}" + new_move[1:]
            elif self.check_for_horz_ambig(new_i, j):
                new_move = "R" + f"{move_map[j]}" + new_move[1:]
            elif self.check_for_vert_ambig(new_i, j):
                new_move = "R" + f"{i + 1}" + new_move[1:]

            self.moves[new_move] = (i, j)

            if new_move[1] == "x":
                break

        for new_j in range(j + 1, 8):
            if self.game_state[i][new_j]:
                if self.game_state[i][new_j][0] == "b" and self.white_to_play or \
                self.game_state[i][new_j][0] == "w" and not self.white_to_play:
                    new_move = f"Rx{move_map[new_j]}{i + 1}"
                else:
                    break
            else:
                new_move = f"R{move_map[new_j]}{i + 1}"

            if self.check_for_horz_ambig(i, new_j) and self.check_for_vert_ambig(i, new_j):
                new_move = "R" + f"{move_map[j]}{i + 1}" + new_move[1:]
            elif self.check_for_horz_ambig(i, new_j):
                new_move = "R" + f"{move_map[j]}" + new_move[1:]
            elif self.check_for_vert_ambig(i, new_j):
                new_move = "R" + f"{i + 1}" + new_move[1:]

            self.moves[new_move] = (i, j)

            if new_move[1] == "x":
                break

        for new_j in range(j - 1, -1, -1):
            if self.game_state[i][new_j]:
                if self.game_state[i][new_j][0] == "b" and self.white_to_play or \
                self.game_state[i][new_j][0] == "w" and not self.white_to_play:
                    new_move = f"Rx{move_map[new_j]}{i + 1}"
                else:
                    break
            else:
                new_move = f"R{move_map[new_j]}{i + 1}"

            if self.check_for_horz_ambig(i, new_j) and self.check_for_vert_ambig(i, new_j):
                new_move = "R" + f"{move_map[j]}{i + 1}" + new_move[1:]
            elif self.check_for_horz_ambig(i, new_j):
                new_move = "R" + f"{move_map[j]}" + new_move[1:]
            elif self.check_for_vert_ambig(i, new_j):
                new_move = "R" + f"{i + 1}" + new_move[1:]

            self.moves[new_move] = (i, j)

            if new_move[1] == "x":
                break

    def check_for_vert_ambig(self, i, j):
        a1 = ""
        a2 = ""
        for new_i in range(i + 1, 8):
            if self.game_state[new_i][j]:
                a1 = self.game_state[new_i][j]
                break

        for new_i in range(i - 1, -1, -1):
            if self.game_state[new_i][j]:
                a2 = self.game_state[new_i][j]
                break

        if a1 == a2 and (a1 == "wr" or a1 == "br"):
            return True
        else:
            return False

    def check_for_horz_ambig(self, i, j):
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

    def make_move(self, move):
        if move in self.moves:
            if move[0] in rev_move_map:
                self.make_pawn_move(move)
            
            elif move[0] == "R":
                self.make_rook_move(move)

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
        if self.white_to_play:
            new_i = int(move[-1]) - 1
            new_j = rev_move_map[(move[-2])]
            self.game_state[new_i][new_j] = "wr"
            prev_i, prev_j = self.moves[move]
            self.game_state[prev_i][prev_j] = ""
            
        else:
            new_i = int(move[-1]) - 1
            new_j = rev_move_map[(move[-2])]
            self.game_state[new_i][new_j] = "br"
            prev_i, prev_j = self.moves[move]
            self.game_state[prev_i][prev_j] = ""

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