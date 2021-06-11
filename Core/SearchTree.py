from Core.AlphaBetaPruning import Pruner
from Core.Enums import MaxMinPlayer
from Core.Node import Node
from Core.TreeCreator import TreeCreator


class SearchTree:
    def __init__(self, playerType=MaxMinPlayer.MAX_PLAYER) -> None:
        self.root = Node()
        self.currentNode: Node = self.root
        self.root.gameState = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
        self.root.playerType = playerType

    def make_move(self, index) -> None:
        if self.currentNode.playerType is MaxMinPlayer.MAX_PLAYER:
            assert 0 <= index <= 5
        else:
            assert 7 <= index <= 12
        if self.currentNode.children is None:
          t = TreeCreator()
          t.create_tree(self.currentNode)
        if index in self.currentNode.children:
            self.currentNode = self.currentNode.children[index]

    def make_optimal_move(self) -> None:
        if self.currentNode.children is None:
          t = TreeCreator()
          t.create_tree(self.currentNode)

        if self.currentNode.bestMoveIndex is None:
            #print('pruner goin to run')
            Pruner(self.currentNode)
        assert self.currentNode.bestMoveIndex is not None
        #print(self.currentNode.bestMoveIndex)
        #print(self.currentNode.children)
        best_move_index = self.currentNode.bestMoveIndex
        self.currentNode = self.currentNode.children[self.currentNode.bestMoveIndex]
        return best_move_index

    def is_game_finished(self):
        return len(list(self.currentNode.children.keys())) == 0

    def get_game_state(self):
        return self.currentNode.gameState
    
    def get_current_player_number(self):
        return self.currentNode.playerType


