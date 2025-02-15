import game
import numpy as np

class MCTS:

    @staticmethod
    def mcts(board, root, Game: game.Game, mcts_iterations):
        """
        Perform Monte Carlo Tree Search.
        Select -> Expand -> Simulate -> Backup

        Args:
            board (np.ndarray): The current board state.
            current_player (int): The current player.
            model (nn.Module): The neural network model.
        """
        for _ in range(mcts_iterations):
            node = root
            trace = [root]
            is_terminal = False
            while node.children:
                node.select()
                node = node.children[0]
                trace.append(node)

                Game.make_move(board, 1 - node.currentPlayer, node.prevAction)
                winner = Game.check_winner(board, 1 - node.currentPlayer, node.prevAction)
                if winner != -1:
                    is_terminal = True
                    result = 1 if winner == 1 - node.currentPlayer else -1
                    node.backup(trace, result, board, Game)
                    break
                elif node.move_count == 9:
                    is_terminal = True
                    result = 0
                    node.backup(trace, result, board, Game)
                    break
            if is_terminal:
                continue
            node.expand(Game.get_valid_moves(board))
            result = MCTS.simulate(Game, board, node)
            node.backup(trace, result, board, Game)

    @staticmethod
    def simulate(Game: game.Game, board, node):
        """
        Simulation step of MCTS.
        """
        sim_board = board.copy()
        current_player = node.currentPlayer
        move_count = node.move_count
        while True:
            valid_moves = Game.get_valid_moves(sim_board)
            if not valid_moves:
                print('move_count:',move_count, node.move_count)
                Game.display_board(board)
                Game.display_board(sim_board)
                break
            action = valid_moves[np.random.randint(len(valid_moves))]
            current_player = Game.make_move(sim_board, current_player, action)
            move_count += 1
            winner = Game.check_winner(sim_board, 1 - current_player, action)
            if winner != -1:
                return 1 if winner == (1 - node.currentPlayer) else -1
            elif move_count == 9:
                return 0