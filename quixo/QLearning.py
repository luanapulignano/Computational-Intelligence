from game import Game, Player, Move
import random
from collections import defaultdict
import numpy as np
import pickle
from itertools import zip_longest
import gzip
import os


class RandomPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        from_pos = (random.randint(0, 4), random.randint(0, 4))
        move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        return from_pos, move

class QLearningPlayer(Player):
    def __init__(self, alpha, epsilon,decay_rate, dis_factor):
        super().__init__()
        self.Q = defaultdict(float)
        self.alpha = alpha
        self.epsilon = epsilon
        self.decay_rate = decay_rate
        self.dis_factor = dis_factor
    #   self.load_q_dict()
    
    # def load_q_dict(self):
    #     part=0
    #     self.Q = defaultdict(float)

    #     while True:
    #         filename = f"q_dict_part_{part}.pkl.gz"

    #         if not os.path.exists(filename):
    #             print("file not opened",filename)
    #             break  

    #         with gzip.open(filename, 'rb') as file:
    #             episode_dict = pickle.load(file)
    #             for key, value in episode_dict.items():
    #                 self.Q[key] = value

    #         part += 1

    # def save_q_dict(self):
    #     part_size = 500
    #     num_parts = (len(self.Q) + part_size - 1) // part_size  # Calculates the number of parts

    #     for i in range(num_parts):
    #         start = i * part_size
    #         end = (i + 1) * part_size if i < num_parts - 1 else len(self.Q)
    #         part_dict = dict(list(self.Q.items())[start:end])

    #         filename = f"q_dict_part_{i}.pkl.gz"
    #         with gzip.open(filename, 'wb') as file:
    #             pickle.dump(part_dict, file)


    def get_Q(self, state, move,game):
        state_key = tuple(map(tuple, game.get_board()))
        return self.Q[(state_key, move)]


    def choose_move(self, state, available,game):
        if random.random() < self.epsilon:
            return random.choice(available)
        else:
            Q_vals= [self.get_Q(state, move,game) for move in available]
            max_Q = max(Q_vals)
            best_moves = [i for i in range(len(available)) if Q_vals[i] == max_Q]
            index = random.choice(best_moves)
            return available[index]

    def update_Q(self, state, move, reward, next_state, available,game):
        state_key = tuple(map(tuple, game.get_board()))
        next_Q_vals = [self.get_Q(next_state, next_move,game) for next_move in available]
        max_next_Q = max(next_Q_vals,default=0.0)
        self.Q[(state_key, move)] = (1 - self.alpha) * self.Q[(state_key, move)] + self.alpha * (reward + self.dis_factor * max_next_Q)
    
    def decay_epsilon(self, episode):
        self.epsilon = max(self.epsilon * (1 / (1 + self.decay_rate * episode)), 0.01)  # Assicurati che epsilon non scenda sotto 0.01

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        return self.choose_move(game.get_board(),game.getPossibleMoves(game.get_current_player()),game)
    

    def fitness(self,game,player):
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

def train_qlearning_agent(qlearning_player, num_episodes,agent_index):
    for episode in range(num_episodes):
        game = Game()  
        state = game.get_board()

        while True:
            available_moves = game.getPossibleMoves(game.get_current_player())
            if game.get_current_player() == agent_index:
                chosen_move = qlearning_player.choose_move(state, available_moves,game)
            else:
                chosen_move = random.choice(available_moves)

            # Execute the move
            from_pos, move = chosen_move
            game.move(from_pos, move, game.get_current_player())
    
            # Get the new state
            next_state = game.get_board()

            # Calculates the reward
            reward = qlearning_player.fitness(game,game.get_current_player())

            # Update the Q value
            qlearning_player.update_Q(state, chosen_move, reward, next_state, available_moves,game)

            # Check if the game is finished
            if game.check_winner() != -1:
                break
            
            game.current_player_idx += 1
            game.current_player_idx %= 2
            state = next_state
        qlearning_player.decay_epsilon(episode)
    #qlearning_player.save_q_dict()
    print("Training completed.")

def test_qlearning(agent,total_games):
    total_wins=0
    for _ in range(total_games):
        game = Game()
        player2=RandomPlayer()
        winner = game.play(agent, player2)
        if winner == 0:
            total_wins += 1
    print(f"Wins: {total_wins}/{total_games}")

if __name__ == '__main__':
    player1=QLearningPlayer(0.1,0.2,0.01,0.3)
    train_qlearning_agent(player1,10,0)
    test_qlearning(player1,100)