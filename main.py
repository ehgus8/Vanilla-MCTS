# this code is needed to refactor
from tictactoe import TicTacToe
from node import Node
from mcts import MCTS

def start():
    game = TicTacToe()
    mcts = MCTS(game=game)
    root = Node(None, to_player=1)
    root.state = game.reset()

    iterations = 100

    while True:
        for i in range(iterations):
            mcts.forward(root)
        root.print_children()
        root_state = root.state
        action = root.sample_action()
        root = Node(None, to_player=root.to_player*-1)
        state, _, done = game.step(root_state, action, to_player=root.to_player*-1)
        root.state = state

        game.display_board(root.state)

        if done:
            return
        
        y, x = list(map(int,input().split()))
        state, _, done = game.step(root.state, y * 3 + x, to_player=root.to_player)
        root = Node(None, to_player=root.to_player*-1)
        root.state = state
        if done:
            return

start()