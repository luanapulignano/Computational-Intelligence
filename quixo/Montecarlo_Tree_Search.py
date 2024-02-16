from game import Game, Player, Move
import random
from copy import deepcopy
import math
import pickle

class RandomPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        from_pos = (random.randint(0, 4), random.randint(0, 4))
        move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        return from_pos, move

# tree node class definition
class TreeNode():
    # class constructor (create tree node class instance)
    def __init__(self, game, parent):
        # init associated board state
        self.game = game
        # init is node terminal flag
        if self.game.check_winner() != -1:
            # we have a terminal node
            self.is_terminal = True
        # otherwise
        else:
            # we have a non-terminal node
            self.is_terminal = False
        # init is fully expanded flag
        self.is_fully_expanded = self.is_terminal
        # init parent node if available
        self.parent = parent
        # init the number of node visits
        self.visits = 0
        # init the total score of the node
        self.score = 0
        # init current node's children
        self.children = {}
        self.move=None

# MCTS class definition
class MCTSPlayer(Player):

    def __init__(self) -> None:
        super().__init__()
        self.cache_file = "mcts_cache.pkl"
        self.cache = self.load_cache()
    
    def load_cache(self):
        try:
            with open(self.cache_file, "rb") as file:
                return pickle.load(file)
        except (FileNotFoundError, EOFError):
            return {}

    def save_cache(self):
        with open(self.cache_file, "wb") as file:
            pickle.dump(self.cache, file)

    # search for the best move in the current position
    def search(self, game):
        # create root node
        self.root = TreeNode(game, None)
        state_key = (tuple(map(tuple, game.get_board())), game.get_current_player())
        if state_key in self.cache:
            return self.cache[state_key]
        # walk through 100 iterations
        for iteration in range(100): 
            # select a node (selection phase)
            node = self.select(self.root)
            # scrore current node (simulation phase)
            score = self.rollout(node.game)
            # backpropagate results
            self.backpropagate(node, score)
        # pick up the best move in the current position
        best_node=self.get_best_node(self.root, 0)
        self.cache[state_key] = best_node.move
        self.save_cache()
        return best_node.move

    # select most promising node
    def select(self, node):
        # make sure that we're dealing with non-terminal nodes
        while not node.is_terminal:
            # case where the node is fully expanded
            if node.is_fully_expanded:
                node = self.get_best_node(node, 2)
            # case where the node is not fully expanded 
            else:
                # otherwise expand the node
                return self.expand(node)
        # return node
        return node

       # expand node
    def expand(self, node):
        # generate legal states (moves) for the given node
        moves = node.game.getPossibleMoves(node.game.get_current_player())
        # loop over generated states (moves)
        for move in moves:
            # make sure that current state (move) is not present in child nodes
            from_pos,slide = move
            state=node.game.get_new_state(from_pos,slide,node.game.get_current_player())
            state.current_player_idx=1-state.get_current_player()

            if str(move) not in node.children:
                # create a new node
                new_node = TreeNode(state, node)
                new_node.move=move
                # add child node to parent's node children list (dict)
                node.children[str(move)]=new_node
                
                # case when node is fully expanded
                if len(moves) == len(node.children):
                    #print("Fully expanded")
                    node.is_fully_expanded = True
                
                # return newly created node
                return new_node
        
    # simulate the game via making random moves until reach end of the game
    def rollout(self, game):
        # make random moves for both sides until terminal state of the game is reached
        while game.check_winner() == -1:
            move = random.choice(game.getPossibleMoves(game.get_current_player()))
            #print(game.get_board())
            if move is None:
                return 0
            else:
                from_pos,slide = move
                game=game.get_new_state(from_pos,slide,game.get_current_player())
                game.current_player_idx=1-game.get_current_player()

        # return score from the player "x" perspective
        if game.check_winner() == 0: 
            return 1
        elif game.check_winner() == 1: 
            return -1

    # backpropagate the number of visits and score up to the root node
    def backpropagate(self, node, score):
        # update nodes's up to root node
        while node is not None:
            # update node's visits
            node.visits += 1
            
            # update node's score
            node.score += score
            
            # set node to parent
            node = node.parent

    def get_best_node(self, node, exploration_constant):
        # define best score & best moves
        best_score = float('-inf')
        best_nodes = []
        
        # loop over child nodes
        for child_node in node.children.values():
            # get move score using UCT formula
            move_score =child_node.score / child_node.visits + exploration_constant * math.sqrt(math.log(node.visits / child_node.visits))                                        

            # better move has been found
            if move_score > best_score:
                best_score = move_score
                best_nodes = [child_node]
            
            # found as good move as already available
            elif move_score == best_score:
                best_nodes.append(child_node)
            
        # return one of the best moves randomly
        return random.choice(best_nodes)

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        return self.search(game)


def test_monte(total_games):
    total_wins=0
    mcts_player = MCTSPlayer()
    for i in range(total_games):
        game = Game()
        player1 = RandomPlayer()
        winner = game.play(mcts_player, player1)
        if winner == 0:
            total_wins += 1
    print(f"Wins: {total_wins}/{total_games}")

if __name__ == '__main__':
    for _  in range(10):
        test_monte(10)
        
