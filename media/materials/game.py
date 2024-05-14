from collections import namedtuple
from ai import minimax_alpha_beta_search

GameState = namedtuple("GameState", "to_move, utility, board, moves")


class Game:
    def actions(self, state):
        pass

    def result(self, state, move):
        pass

    def utility(self, state, player):
        pass

    def terminal_test(self, state):
        pass
    
    def to_move(self, state):
        return state.to_move
    


class TicTacToe(Game):
    def __init__(self, h=3, v=3, k=3):
        self.h = h
        self.v = v
        self.k = k
        moves = [(x, y) for x in range(0, h) for y in range(0, v)]
        self.initial = GameState(to_move='X', utility=0, board={}, moves=moves)

    def actions(self, state):
        return state.moves
    
    def result(self, state, move):
        if move not in state.moves:
            return state
        
        board = state.board.copy()
        board[move] = state.to_move
        moves = list(state.moves)
        moves.remove(move)
        return GameState(to_move=('O' if state.to_move == 'X' else 'X'),
                         utility=self.compute_utility(board, move, state.to_move),
                         board=board, moves=moves)
    
    def utility(self, state, player):
        return state.utility if player == 'X' else -state.utility
    
    def terminal_test(self, state):
        return state.utility != 0 or len(state.moves) == 0
    
    def display(self, state):
        board = state.board
        for x in range(self.h):
            for y in range(self.v):
                print(board.get((x, y), '.'), end=' ')
            print()

    def compute_utility(self, board, move, player):
        if (self.k_in_row(board, move, player, (0, 1)) or 
            self.k_in_row(board, move, player, (1, 0)) or 
            self.k_in_row(board, move, player, (1, -1)) or
            self.k_in_row(board, move, player, (1, 1))):
            return 1 if player == 'X' else -1
        else:
            return 0

    def k_in_row(self, board, move, player, delta_x_y):
        (delta_x, delta_y) = delta_x_y
        x, y = move
        n = 0
        while board.get((x, y)) == player:
            n += 1
            x, y = x + delta_x, y + delta_y
        x, y = move
        while board.get((x ,y)) == player:
            n += 1
            x, y = x - delta_x, y - delta_y
        
        n -= 1
        return n >= self.k


