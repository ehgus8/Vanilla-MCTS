class MCTS:
    
    def __init__(self, game) -> None:
        self.game = game

    # forward : selection -> expansion -> simulation -> backpropagation
    def forward(self, root):
        trace = [root]
        node = root

        while not node.is_terminal():
            node = self.select(node)
            trace.append(node)
        
        if node.is_game_ended:
            self.backup(trace, node.winner)
            return

        self.expand(node)
        score = self.simulation(node) # score is the number of winning player or draw 0
        self.backup(trace, score)
    
    def select(self, node):
        node = node.select()
        game = self.game
        state, score, done = game.step(node.parent.state, node.action, to_player=node.parent.to_player)
        node.state = state

        if done:
            node.winner = score
            node.is_game_ended = True

        return node
    
    def expand(self, node):
        actions = self.game.get_valid_action_list(node.state.flatten(), shuffle=True)
        node.expand(actions)
    
    def simulation(self, node):
        return self.game.simulation(node)

    def backup(self, trace, score):
        for node in trace[::-1]:
            node.visit += 1
            node.score += score
            # score = score * -1