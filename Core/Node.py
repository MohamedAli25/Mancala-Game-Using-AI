import math
from Enums import MaxMinPlayer

class Node:
    def __init__(self) -> None:
        self.parrentNode: Node = None
        self.children: dict = None
        self.playerType = MaxMinPlayer.MAX_PLAYER
        self.alpha = math.inf
        self.beta = -math.inf
        self.gameState: list = None 
    
    @property
    def getScore_playerA(self) -> int:
        return self.gameState[6]

    @property
    def getScore_playerB(self) -> int:
        return self.gameState[-1]

    def get_score(self) -> int:
        """
        returns the score difference between player A and player B (opponent)
        """
        return self.gameState[6] - self.gameState[-1]
