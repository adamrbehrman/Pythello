from game.board import Board
from game.enums import Color
from game.point import Point
from players.player import Player
import copy
import math
import random
from time import perf_counter

class MCTSPlayer(Player):

    def __init__(self, color:Color, iterations: int = 1000):
        super().__init__(color)
        self.iterations = iterations

    def mcts(self, root_node):
        for _ in range(self.iterations):
            # Selection Phase (skipped)
            
            # Randomly choose a precomputed child node for exploration
            selected_child = random.choice(root_node.children)
            
            # Expansion Phase (skipped)

            # Simulation Phase
            result = self.simulate(selected_child)

            # Backpropagation Phase
            self.backpropagate(selected_child, result)

    def simulate(self, node):
        # Simulate a game rollout from the selected child node
        current_state = copy.deepcopy(node.state)
        while not current_state.is_game_over():
            legal_moves = current_state.get_all_playable_points(node.color)
            if legal_moves:
                random_move = random.choice(legal_moves)
                current_state.can_place_disc_and_flip(random_move, node.color)
                node.color = Color.BLACK if node.color == Color.WHITE else Color.WHITE 
            else:
                node.color = Color.BLACK if node.color == Color.WHITE else Color.WHITE

        # Game is over, determine the winner
        return current_state.winner_heuristic(node.color)

    def backpropagate(self, node, result):
        # Update statistics for the selected child node and its ancestors
        while node is not None:
            node.visits += 1
            node.value += result
            node = None if node.parent is None else node.parent

    def select_best_move(self, root_node):
        if not root_node.children:
            return None  # No legal moves available
        else:
            best_child = max(root_node.children, key=lambda child: child.value)
            return best_child.move

    def play(self, board: Board) -> Point:
        # Initialize the root node with the current game state
        root_node = Node(board, self.color)

        for point in root_node.state.get_legal_moves(root_node.color):
            board_copy = copy.deepcopy(root_node.state)
            board_copy.place_and_flip_discs(point, root_node.color)
            root_node.children.append(Node(board_copy, Color.BLACK if root_node.color == Color.WHITE else Color.WHITE ))

        # Run MCTS for a specified number of iterations
        self.mcts(root_node)

        # Select the best move based on child node visits
        best_move = self.select_best_move(root_node)

        # Return the move associated with the best child node
        return best_move
    
class Node:
    def __init__(self, state, color, move=None):
        self.state = state
        self.color = color
        self.move = move
        self.children = []
        self.visits = 0
        self.value = 0
        self.parent = None

    def __str__(self):
        return self.state.__str__()

