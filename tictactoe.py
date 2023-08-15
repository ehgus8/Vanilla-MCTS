# this code is needed to refactor
import numpy as np
import random

size = 3
class TicTacToe:
    def __init__(self):
        pass

    def size(self):
        return size
    
    def reset(self):
        board = np.zeros((size, size),dtype=np.float32)

        return board
    
    # it takes an action in the form of an integer index (0~8) not coordinate (y, x)
    def step(self, board, action, to_player, copy=True):
        y, x = action//size, action%size
        if copy:
            board = board.copy()

        done = self.make_move(board, y, x, to_player)
        next_player = to_player * -1
        score = 0
        if done == True:
            if self.winner == 0:
                score = 0
            else:
                score = to_player
                
        return board, score, done
    
    def get_valid_action_list(self, board, shuffle = False):
        indices = np.where(board == 0)
        action_list = indices[0].tolist()
        if shuffle:
            random.shuffle(action_list)
        if action_list == []:
            action_list = None

        return action_list

    def simulation(self, node):
        board = node.state.copy()
        to_player = node.to_player
        actions = self.get_valid_action_list(node.state, shuffle=True)

        for action in actions:
            _, score, done = self.step(board, action, to_player, copy=False)

            if done:
                return score
            
            to_player = to_player * -1
        
        return 0


    def get_action_mask(self, s):
        mask = s[0].clone().flatten()
        mask[mask == 0] = 2
        mask[(mask == 1) | (mask == -1)] = 0
        mask[mask == 2] = 1
    
        return mask
        
    # 플레이어 1은 -1 , 플레이어 2는 1로 변경 된 상태를 넘겨준다.
    def get_reversed_board(self, s):
        return s * -1


    def get_random_move(self):
        valid_indices = np.array(np.where(self.valid_moves == 1)).reshape(-1)
        random_move = np.random.choice(valid_indices,size=1)
        return random_move[0]
    
    
    def get_valid_moves(self, board):
        indices = np.where(board == 0)
        valid_moves = indices[0] * 5 + indices[1]
        return valid_moves

    def make_move(self, board, row, col, player):
        if board[row, col] != 0:
            return None

        board[row, col] = player
        
        is_win = self.check_win(board, player)
        if is_win:
            print(f'Player {player} wins!')
            self.winner = player
            return True
        #draw
        if is_win == None:
            print(f'Player draw!')
            self.winner = 0
            return True
        
        return False

    def check_win(self, board, player):
        # Check rows and columns
        for i in range(size):
            for j in range(size - 2):
                if (np.all(board[i, j:j+3] == player) or 
                    np.all(board[j:j+3, i] == player)):
                    return True

        diag1 = [1, 1] # vector (y, x)
        diag2 = [1, -1] # vector (y, x)
        # Check diagonals
        for i in range(size - 2):
            for j in range(size - 2):
                if (np.all(board[[i+k*diag1[0] for k in range(3)], [j+k*diag1[1] for k in range(3)]] == player) or
                    np.all(board[[i+k*diag2[0] for k in range(3)], [j+2+k*diag2[1] for k in range(3)]] == player)):
                    return True

        # Check draw
        if (np.where(board == 0)[0].shape[0] == 0):
            return None

        return False

    def display_board(self, board):
        print(board)
    
    def get_state(self):
        return self.board.copy()

    