import numpy as np
import math
import logging
import os

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

def get_game_logger(game_name):
    logger = logging.getLogger(game_name)
    logger.setLevel(logging.DEBUG)

    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(log_dir, exist_ok=True)

    file_path = os.path.join(log_dir, f'{game_name}.log')
    
    if not logger.handlers:
        file_handler = logging.FileHandler(file_path, mode='a') 
        file_handler.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
    
    return logger