import numpy as np
import time
from game import Game
from collections import deque
from mcts import MCTS
from node import Node
import utils


class Gomoku(Game):
    rows, cols = 15, 15
    action_dim = rows * cols
    state_dim = rows * cols

    logger = utils.get_game_logger('Gomoku')

    def __init__(self):
        self.board = np.zeros((3, Gomoku.rows, Gomoku.cols), dtype=np.float32) # the shape of the board is (3, rows, cols) to implement alpha zero in the future.

    @staticmethod
    def display_board(board):
        display = np.full((Gomoku.rows, Gomoku.cols), ' ')
        display[board[0] == 1] = 'O'
        display[board[1] == 1] = 'X'
        print("\n  ", end='')
        for c in range(Gomoku.cols):
            print(c, end=' ')
        print()
        for i, row in enumerate(display):
            print(i % 10, ' '.join(row))    
        print()

    @staticmethod
    def get_action_idx(action: tuple[int, int]):
        """
        Returns:
            action index (int): index of action flattened to 1D
        """
        return action[0] * Gomoku.rows + action[1]

    @staticmethod
    def make_move(board, current_player, action):
        row, col = action
        if board[0, row, col] == 0 and board[1, row, col] == 0:
            board[current_player, row, col] = 1
            board[2, :, :] = 1 - current_player
            return 1 - current_player
        else:
            print("Invalid move. Try again.")
            return current_player

    @staticmethod
    def undo_move(board, current_player, action):
        row, col = action
        board[1 - current_player, row, col] = 0
        # board[2, :, :] = 1 - current_player

    @staticmethod
    def check_winner(board, player, action):
        row, col = action
        def dfs(dr, dc):
            q = deque([(row, col)])
            visited = set()
            seq_count = 1
            while q:
                r, c = q.pop()
                visited.add((r, c))
                
                if 0 <= r + dr < Gomoku.rows and 0 <= c + dc < Gomoku.cols and (r + dr, c + dc) not in visited and board[player, r + dr, c + dc] == 1:
                    q.append((r + dr, c + dc))
                    seq_count += 1
                if 0 <= r - dr < Gomoku.rows and 0 <= c - dc < Gomoku.cols and (r - dr, c - dc) not in visited and board[player, r - dr, c - dc] == 1:
                    q.append((r - dr, c - dc))
                    seq_count += 1
                if seq_count >= 5:
                    return True
                
            return False
        
        for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:
            if dfs(dr, dc):
                return player
            
        return -1 # No winner
    
    @staticmethod
    def get_valid_moves(board):
        valid_moves = set()
        for r in range(Gomoku.rows):
            for c in range(Gomoku.cols):
                if board[0, r, c] == 1 or board[1, r, c] == 1:
                    for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:
                        if 0 <= r + dr < Gomoku.rows and 0 <= c + dc < Gomoku.cols and board[0, r + dr, c + dc] == 0 and board[1, r + dr, c + dc] == 0:
                            valid_moves.add((r + dr, c + dc))
                        if 0 <= r - dr < Gomoku.rows and 0 <= c - dc < Gomoku.cols and board[0, r - dr, c - dc] == 0 and board[1, r - dr, c - dc] == 0:
                            valid_moves.add((r - dr, c - dc))
        if len(valid_moves) == 0:
            valid_moves.add((Gomoku.rows//2, Gomoku.cols//2))
        return list(valid_moves)
        # return [(r, c) for r in range(Gomoku.rows) for c in range(Gomoku.cols) if board[0, r, c] == 0 and board[1, r, c] == 0]

    @staticmethod
    def mcts(board: np.array, root, mcts_iterations):
        """
        Call Monte Carlo Tree Search.
        Select -> Expand -> Simulate -> Backup
        """
        MCTS.mcts(board, root, Gomoku, mcts_iterations)

    @staticmethod
    def get_input(board):
        row, col = map(int, input("Enter row and column: ").split())
        if board[0, row, col] == 1 or board[1, row, col] == 1:
            return (None, None)
        return (row, col)
    
    def play_against_mcts(self, mcts_iterations):
        """
        Play a game of Tic-Tac-Toe against the MCTS agent.

        """
        current_player = 0
        move_count = 0

        while True:
            # Human player
            Gomoku.display_board(self.board)
            row, col = Gomoku.get_input(self.board)
            if row is None:
                print("Invalid move. Try again.")
                continue
            current_player = Gomoku.make_move(self.board, current_player, (row, col))
            move_count += 1
            winner = Gomoku.check_winner(self.board, 1 - current_player, (row, col))
            if winner != -1:
                Gomoku.display_board(self.board)
                print("Player", winner, "wins!")
                break
            elif move_count == 9:
                Gomoku.display_board(self.board)
                print("It's a draw!")
                break

            # MCTS agent
            root = Node(None, None, current_player, move_count)
            start_time = time.time()
            Gomoku.mcts(self.board, root, mcts_iterations)
            Gomoku.logger.debug(f'mcts_iteration: {mcts_iterations}, time: {time.time() - start_time}s')
            # row, col = root.sample_child().prevAction
            chosen_child = root.max_visit_child()
            for child in root.children:
                print(child.to_string(Gomoku))
            current_player = Gomoku.make_move(self.board, current_player, chosen_child.prevAction)
            move_count += 1
            winner = Gomoku.check_winner(self.board, root.currentPlayer, chosen_child.prevAction)
            if winner != -1:
                Gomoku.display_board(self.board)
                print("Player", winner, "wins!")
                break
            elif move_count == 9:
                Gomoku.display_board(self.board)
                print("It's a draw!")
                break