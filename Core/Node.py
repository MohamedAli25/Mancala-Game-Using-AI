import numpy as np
from Enums import MaxMinPlayer

class Node:
    def __init__(self) -> None:
        self.parrentNode = None
        self.children: list = None
        self.maxMin = MaxMinPlayer.MAX_PLAYER
        self.alpha = np.inf
        self.beta = np.NINF
        self.gameState = []
        self.score = 0

    def evaluate_score(self):
        """
        to be implemented
        """
        return self.score
