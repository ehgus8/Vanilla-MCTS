from tictactoe import TicTacToe
from connect4 import Connect4

if __name__ == '__main__':
    while True:
        print('1. TicTacToe')
        print('2. Connect4')
        num = int(input())
        if num == 1:
            game = TicTacToe()
        elif num == 2:
            game = Connect4()
        
        game.play_against_mcts(mcts_iterations = 500)