from tictactoe import TicTacToe
from connect4 import Connect4

# game = TicTacToe()
game = Connect4()

game.play_against_mcts(mcts_iterations = 500)
