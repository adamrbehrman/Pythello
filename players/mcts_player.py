from __future__ import annotations  # Import this line

from game.board import Board
from game.enums import Color
from game.point import Point
from players.player import Player

import copy
import random
from time import perf_counter
from typing import List
class MCTSPlayer(Player):

    def __init__(self, color:Color, iterations: int = 1000):
        super().__init__(color)
        self.iterations = iterations

    def mcts(self, root_node: MCTSNode):
        for _ in range(self.iterations):
            # Selection Phase (skipped)
            
            # Randomly choose a precomputed child node for exploration
            selected_child = random.choice(root_node.children)
            
            # Expansion Phase (skipped)

            # Simulation Phase
            score = self.simulate(selected_child)

            # Backpropagation Phase
            self.backpropagate(selected_child, score)

    def simulate(self, node: MCTSNode) -> int:
        # Simulate a full game from the selected child node (board state)
        board_copy = copy.deepcopy(node.state)
        while not board_copy.is_game_over():
            legal_moves = board_copy.get_legal_moves(node.color)

            if legal_moves:
                random_move = random.choice(legal_moves)
                board_copy.place_and_flip_discs(random_move, node.color)
            
            node.color = Color.BLACK if node.color == Color.WHITE else Color.WHITE

        # Game is over, determine the winner
        return board_copy.winner_heuristic(node.color)

    def backpropagate(self, node: MCTSNode, score: int):
        # Update the score for the selected child node (move at a board state) and its ancestors (earlier moves)
        while node is not None:
            node.visits += 1
            node.value += score
            node = None if node.parent is None else node.parent

    def select_best_move(self, root_node: MCTSNode):
        if not root_node.children: # No moves
            return None  
        
        best_child = max(root_node.children, key=lambda child: child.value)
        return best_child.move

    def play(self, board: Board) -> Point:
        # Initialize the root node with the current game state
        root_node = MCTSNode(board, self.color)

        for move in root_node.state.get_legal_moves(root_node.color):
            board_copy = copy.deepcopy(root_node.state)
            board_copy.place_and_flip_discs(move, root_node.color)
            root_node.children.append(MCTSNode(board_copy, Color.BLACK if root_node.color == Color.WHITE else Color.WHITE, move))

        # Run MCTS for a specified number of iterations
        self.mcts(root_node)

        # Select the best move based on child node visits
        best_move = self.select_best_move(root_node)

        # Return the move associated with the best child node
        return best_move
class MCTSNode:

    def __init__(self, state: Board, color: Color, move: Point = None):
        self.state = state
        self.color = color
        self.move = move
        self.children: List[MCTSNode] = []
        self.visits: int = 0
        self.value: int = 0
        self.parent: MCTSNode = None

    def __str__(self):
        return self.state.__str__()

