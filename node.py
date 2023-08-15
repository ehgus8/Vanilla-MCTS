import math

class Node:

    def __init__(self, parent) -> None:
        self.parent = parent # Node
        self.children = None # List
        self.state = None
        self.to_player = None # player to act in this state, to make next state.
        self.action = None # index or coordinate of actions to become this state.
        self.visit = 0
        self.score = 0
        self.is_game_ended = False

    def is_terminal(self):
        return self.is_game_ended or self.children == None

    def select(self):
        max_uct = -999
        max_idx = 0
        children = self.children
        for idx, child in enumerate(children):
            uct = child.score + math.sqrt(2)*math.sqrt(math.log(self.visit)/child.visit)
            if uct > max_uct:
                max_uct = uct
                max_idx = idx
        
        return children[max_idx]

    def expand(self, actions):
        if actions == None:
            self.is_game_ended = True

        children = []
        for action in actions:
            child = Node(self)
            child.action = action

        self.children = children

        return None
    

