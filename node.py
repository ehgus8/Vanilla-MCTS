import math

class Node:

    def __init__(self, parent, to_player) -> None:
        self.parent = parent # Node
        self.children = None # List
        self.state = None
        self.to_player = to_player # player to act in this state, to make next state.
        self.action = None # index or coordinate of actions to become this state.
        self.visit = 0
        self.score = 0
        self.is_game_ended = False
        self.winner = None

    def is_terminal(self):
        return self.is_game_ended or self.children == None

    def select(self):
        max_uct = -999
        max_idx = 0
        children = self.children
        for idx, child in enumerate(children):
            uct = self.to_player * child.score + math.sqrt(2)*math.sqrt(math.log(self.visit)/(child.visit+1))
            if uct > max_uct:
                max_uct = uct
                max_idx = idx
    

        return children[max_idx]

    def expand(self, actions):
        children = []
        for action in actions:
            child = Node(self, self.to_player * -1)
            child.action = action
            children.append(child)

        self.children = children

        return None
    
    def sample_action(self, method='visit'):
        max_visit = 0
        max_idx = 0
        children = self.children
        for idx, child in enumerate(children):
            if child.visit > max_visit:
                max_visit = child.visit
                max_idx = idx
        
        return children[max_idx].action

    def print_children(self):
        children = self.children
        for idx, child in enumerate(children):
            print(f'{idx+1}: visit: {child.visit}, score: {child.score}')

