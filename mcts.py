class MCTS:
    
    def __init__(self, game) -> None:
        self.game = game

    def forward(self, root):
        trace = [root]
        node = root
        while not node.is_terminal():
            node = self.select(node)
            trace.append(node)
        
        self.expand(node)
        score = self.simulation(node)
        self.backup(trace, score)

        return root
    
    def select(self, node):
        return node.select()
    
    def expand(self, node):
        actions = None
        node.expand(actions)
    
    def simulation(self, node):
        return self.game.simulation(node)

    def backup(self, trace, score):
        for node in trace[::-1]:
            node.visit += 1
            node.score += score
            score = score * -1