import numpy as np
import math

def calcUcbOfChildrenFromParent(node: 'Node'):
    
    for child in node.children:
        if child.visit == 0:
            child.ucb = np.inf
            continue
        child.ucb = (child.value / child.visit) + math.sqrt(2 * math.log(node.visit) / child.visit)
    return

def get_probablity_distribution_of_children(node: 'Node', Game):
    """
    Get the probablity distribution of children by the number of visits.
    """
    visit_counts = np.zeros(Game.action_dim)
    for child in node.children:
        visit_counts[Game.get_action_idx(child.prevAction)] = child.visit

    probablity_distribution = visit_counts/np.sum(visit_counts)
    return probablity_distribution