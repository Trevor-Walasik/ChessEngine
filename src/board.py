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
        self.moves = set()

        for i in range(8):
            for j in range(8):
                if self.white_to_play:
                    if self.game_state[i][j] == "wp":
                        self.calculate_pawn_moves(i, j)
                else:
                    if self.game_state[i][j] == "bp":
                        self.calculate_pawn_moves(i, j)
        
        self.add_pawn_promotion()
        self.check_moves()

    def add_pawn_promotion(self):
        new_moves = set()
        moves_to_remove = set()
        for move in self.moves:
            if self.white_to_play:
                if move[0] in rev_move_map and move[-1] == "8":
                    new_moves.add(move + "=N")
                    new_moves.add(move + "=B")
                    new_moves.add(move + "=R")
                    new_moves.add(move + "=Q") 
                    moves_to_remove.add(move)
            else: 
                if move[0] in rev_move_map and move[-1] == "1":
                    new_moves.add(move + "=N")
                    new_moves.add(move + "=B")
                    new_moves.add(move + "=R")
                    new_moves.add(move + "=Q") 
                    moves_to_remove.add(move)

        self.moves = self.moves | new_moves
        self.moves = self.moves - moves_to_remove

    # If any move results in opposing side having a king captures move, move is illegal, this function removes
    def check_moves(self):
        pass

    def calculate_pawn_moves(self, i, j):
        if self.white_to_play:
            if i == 1:
                if not self.game_state[i + 1][j] and not self.game_state[i + 2][j]:
                    self.moves.add(f"{move_map[j]}{i + 2}")
                    self.moves.add(f"{move_map[j]}{i + 3}")
            else:
                if i + 1 < 8 and not self.game_state[i + 1][j]:
                    self.moves.add(f"{move_map[j]}{i + 2}")
            
            if i + 1 < 8 and j + 1 < 8 and \
               self.game_state[i + 1][j + 1] and self.game_state[i + 1][j + 1][0] == "b":
                self.moves.add(f"{move_map[j]}x{move_map[j + 1]}{i + 2}")

            if i + 1 < 8 and j - 1 > -1 and \
               self.game_state[i + 1][j - 1] and self.game_state[i + 1][j - 1][0] == "b":
                self.moves.add(f"{move_map[j]}x{move_map[j - 1]}{i + 2}")
            
            if i == 4:
                if self.prev_move[1] == "5" and j - 1 > -1 and \
                   rev_move_map[self.prev_move[0]] == j - 1:
                    self.moves.add(f"{move_map[j]}x{move_map[j - 1]}{i + 2}")

                if self.prev_move[1] == "5" and j + 1 < 8 and \
                   rev_move_map[self.prev_move[0]] == j + 1:
                    self.moves.add(f"{move_map[j]}x{move_map[j + 1]}{i + 2}")
                    
        else:
            if i == 6:
                if not self.game_state[i - 1][j] and not self.game_state[i - 2][j]:
                    self.moves.add(f"{move_map[j]}{i}")
                    self.moves.add(f"{move_map[j]}{i - 1}")
            else:
                if i - 1 > -1 and not self.game_state[i - 1][j]:
                    self.moves.add(f"{move_map[j]}{i}")

            if i - 1 > -1 and j + 1 < 8 and \
               self.game_state[i - 1][j + 1] and self.game_state[i - 1][j + 1][0] == "w":
                self.moves.add(f"{move_map[j]}x{move_map[j + 1]}{i}")

            if i - 1 > -1 and j - 1 > -1 and \
               self.game_state[i - 1][j - 1] and self.game_state[i - 1][j - 1][0] == "w":
                self.moves.add(f"{move_map[j]}x{move_map[j - 1]}{i}")

            if i == 3:
                if self.prev_move[1] == "4" and j - 1 > -1 and \
                   rev_move_map[self.prev_move[0]] == j - 1:
                    self.moves.add(f"{move_map[j]}x{move_map[j - 1]}{i}")

                if self.prev_move[1] == "4" and j + 1 < 8 and \
                   rev_move_map[self.prev_move[0]] == j + 1:
                    self.moves.add(f"{move_map[j]}x{move_map[j + 1]}{i}")

    def make_move(self, move):
        if move in self.moves:
            if move[0] in rev_move_map:
                self.make_pawn_move(move)
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

    def print_moves(self):
        print(self.moves)

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