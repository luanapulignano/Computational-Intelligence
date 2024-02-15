import random
import numpy as np
from game import Game, Player, Move

class RandomPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        from_pos = (random.randint(0, 4), random.randint(0, 4))
        move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        return from_pos, move

class MinMaxPlayer(Player):
    def __init__(self,game:Game,depth) -> None:
        super().__init__()
        self.game = game
        self.depth=depth
        self.cache = {}

    def fitness(self, game,player):
        # Check for a winner
        winner = game.check_winner()
        if winner == 0:
            return float('inf')  # Current player wins
        elif winner == 1:
            return float('-inf')  # Opponent wins
    
        opponent=1-player

        max_occurrences_player_row = 0
        max_occurrences_opponent_row = 0
        max_occurrences_player_column = 0
        max_occurrences_opponent_column= 0
        max_occurrences_player_diag = 0
        max_occurrences_opponent_diag = 0

        # Count maximum occurrences for each column
        for col in range(game.get_board().shape[1]):
            occurrences_player = np.sum(game.get_board()[:, col] == player)
            occurrences_opponent = np.sum(game.get_board()[:, col] == opponent)
            max_occurrences_player_column = max(max_occurrences_player_column, occurrences_player)
            max_occurrences_opponent_column = max(max_occurrences_opponent_column, occurrences_opponent)

        # Count maximum occurrences for each row
        for row in range(game.get_board().shape[0]):
            occurrences_player = np.sum(game.get_board()[row, :] == player)
            occurrences_opponent = np.sum(game.get_board()[row, :] == opponent)
            max_occurrences_player_row = max(max_occurrences_player_row, occurrences_player)
            max_occurrences_opponent_row = max(max_occurrences_opponent_row, occurrences_opponent)

        # Count maximum occurrences for the major diagonal
        occurrences_player_major = np.sum(np.diag(game.get_board()) == player)
        occurrences_opponent_major = np.sum(np.diag(game.get_board()) == opponent)
        occurrences_player_minor = np.sum(np.diag(np.fliplr(game.get_board())) == player)
        occurrences_opponent_minor = np.sum(np.diag(np.fliplr(game.get_board())) == opponent)
        max_occurrences_player_diag = max(occurrences_player_major, occurrences_player_minor)
        max_occurrences_opponent_diag = max(occurrences_opponent_major, occurrences_opponent_minor)

        # Apply a penalty based on the maximum number of opponent's pieces
        value = max_occurrences_player_column+max_occurrences_player_row+max_occurrences_player_diag - max_occurrences_opponent_column -max_occurrences_opponent_diag - max_occurrences_opponent_row
        return value if player==0 else -value


    #we are implementing minmax with alpha beta pruning for better efficiency
    def minmax_with_cache(self, game: Game, depth: int, alpha: float, beta,player):
        state_key = (tuple(map(tuple, game.get_board())), player)
        if state_key in self.cache:
            return self.cache[state_key]
        
        best_movement=None
        possible = game.getPossibleMoves(player)
        if (depth == 0) or (game.check_winner() != -1) or not possible: #This is the terminal condition of the minmax
            value = self.fitness(game, player)
            result = value, best_movement, alpha, beta
            self.cache[state_key] = result
            return result

        if player==0:
            value = float('-inf')
            possible_moves = game.getPossibleMoves(player)
            for move in possible_moves:
                child = game.get_new_state(move[0], move[1], player)
                tmp,_,_,_ = self.minmax_with_cache(child, depth-1, alpha, beta,(1-player))
                if tmp > value:
                    value = tmp
                    best_movement = move
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
        else:
            value = float('inf')
            possible_moves = game.getPossibleMoves(player)
            for move in possible_moves:
                child = game.get_new_state(move[0], move[1], player)
                tmp,_, _,_ = self.minmax_with_cache(child, depth-1, alpha, beta,(1-player))
                if tmp < value:
                    value = tmp
                    best_movement = move
                beta = min(beta, value)
                if alpha >= beta:
                    break
        
        self.cache[state_key] = value, best_movement, alpha, beta
        return value, best_movement, alpha, beta

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
            value, best_movement, alpha, beta = self.minmax_with_cache(game, self.depth, float('-inf'), float('inf'),game.get_current_player())
            #If the move returned by minmax is not acceptable , it is returned None and in this case we will return a random play
            if best_movement is not None:
                return best_movement
            else:
                return random.choice(game.getPossibleMoves(game.get_current_player()))


def test_minmax(total_games,depths):
    for depth in depths:
        total_wins=0
        for _ in range(total_games):
            game = Game()
            player1 = MinMaxPlayer(game,depth)
            player2=RandomPlayer()
            winner = game.play(player1, player2)
            if winner == 0:
                total_wins += 1
        print(f"Wins: {total_wins}/{total_games} with depth: {depth}")

if __name__ == '__main__':
    test_minmax(100,[2])