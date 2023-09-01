from pythello import Pythello
from game.enums import DiscEnum
from game.point import Point

from players.player import Player
from players.random_player import RandomPlayer
from players.minimax_player import MiniMaxPlayer
from players.late_minimax_player import LateMiniMaxPlayer
from players.mcts_player import MCTSPlayer

from collections import Counter
import copy

class Runner:

    def __init__(self):
        Runner.compare_players(MiniMaxPlayer, LateMiniMaxPlayer, 3, True)
        Runner.compare_players(MiniMaxPlayer, MCTSPlayer, 1, True)

    @staticmethod
    def compare_players(player1:Player, player2:Player, games=10, show_game=False) -> None:
        winners_dict = {}
        for i in range(games):
            print(f'Playing game {i}...')
            game = Pythello(players = [player1(DiscEnum.WHITE), player2(DiscEnum.BLACK)])
            game.play(show_game)
            winner = game.get_winner()
            if type(winner).__name__ not in winners_dict.keys():
                winners_dict[type(winner).__name__] = (winner.color, 0)
            winners_dict[type(winner).__name__] = (winner.color, winners_dict[type(winner).__name__][1] + 1)
            print({type(winner).__name__})

        winners_dict_switched = {}
        for i in range(games):
            print(f'Playing game {i}...')
            game = Pythello(players = [player2(DiscEnum.WHITE), player1(DiscEnum.BLACK)])
            game.play(show_game)
            winner = game.get_winner()
            if type(winner).__name__ not in winners_dict_switched.keys():
                winners_dict_switched[type(winner).__name__] = (winner.color, 0)
            winners_dict_switched[type(winner).__name__] = (winner.color, winners_dict_switched[type(winner).__name__][1] + 1)
            type(winner).__name__

        print('\n----------\nGames won by players...')
        [ print(f'\t{winner} as {tuple[0].name.title()} ({tuple[0].value}): {tuple[1]}/{i+1}') for winner, tuple in Counter(winners_dict).items() ]
        [ print(f'\t{winner} as {tuple[0].name.title()} ({tuple[0].value}): {tuple[1]}/{i+1}') for winner, tuple in Counter(winners_dict_switched).items() ]

Runner()

class Tester:

    def __init__(self):
        func_list = [func for func in dir(Tester) if callable(getattr(Tester, func)) and 'test' in func ]

        for func in func_list:
            print(f'{func}: {getattr(Tester, func)()}')

    def test_scale():
        game1 = Pythello(scale=2)
        # print(game1)
        return game1.board.scale == 2

    def test_place_disc():
        game1 = Pythello()
        res1 = game1.place_disc(Point(3, 2), DiscEnum.BLACK)
        res2 = game1.place_disc(Point(4, 2), DiscEnum.BLACK)
        return not res1 and res2

    def test_board_copy():
        game1 = Pythello()
        game2 = copy.deepcopy(game1)
        game1.place_disc(Point(1, 1), DiscEnum.BLACK)
        game2.place_disc(Point(6, 6), DiscEnum.BLACK)
        return game1 != game2
    
    def test_all_playable_spots():
        game1 = Pythello()
        points = game1.board.get_all_playable_points(DiscEnum.BLACK)
        game1.place_disc(points[0], DiscEnum.BLACK)
        points = game1.board.get_all_playable_points(DiscEnum.WHITE)
        return points == [Point(2,3), Point(2,5), Point(4,5)]

    def test_is_game_over():
        game1 = Pythello()
        game2 = Pythello()
        game2.board.grid = [[DiscEnum.BLACK.value] * len(game2.board.grid) for _ in range(len(game2.board.grid))]
        return not game1.is_game_over() and game2.is_game_over()
    

