from Core.AlphaBetaPruning import Pruner
from Core.Enums import MaxMinPlayer
from Core.Node import Node
from Core.TreeCreator import TreeCreator
import os
import pickle


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

    def make_optimal_move(self) -> int:
        if self.currentNode.children is None:
            t = TreeCreator()
            t.create_tree(self.currentNode)

        if self.currentNode.bestMoveIndex is None:
            # print('pruner goin to run')
            Pruner(self.currentNode)
        assert self.currentNode.bestMoveIndex is not None
        # print(self.currentNode.bestMoveIndex)
        # print(self.currentNode.children)
        best_move_index = self.currentNode.bestMoveIndex
        self.currentNode = self.currentNode.children[self.currentNode.bestMoveIndex]
        return best_move_index

    def is_game_finished(self):
        return self.__is_game_state_finished(self.currentNode.gameState)

    def get_game_state(self):
        return self.currentNode.gameState

    def get_current_player_number(self):
        return self.currentNode.playerType

    def __is_game_state_finished(self, gameState: list):
        allEmpty = True
        for i in range(6):
            if gameState[i] > 0:
                allEmpty = False
        if allEmpty:
            return True
        allEmpty = True
        for i in range(7, 13):
            if gameState[i] > 0:
                allEmpty = False
        return allEmpty

    def save(self) -> None:
        """
        save current game to a pickle file
        """
        path = os.path.join(os.getcwd(), 'mancalaGame.gg')
        with open(path, 'wb') as handle: pickle.dump({
            "state": self.currentNode.gameState,
            "playerType": 1 if self.currentNode.playerType is MaxMinPlayer.MAX_PLAYER else 0
        },
                                                     handle, protocol=pickle.HIGHEST_PROTOCOL)
        print("game saved")

    @staticmethod
    def load(path=os.path.join(os.getcwd(), 'mancalaGame.gg')) -> Node:
        """
        loads a game from a pickle file
        """
        # path = os.path.join(os.getcwd(), 'mancalaGame.pickle')
        searchTree = SearchTree()
        with open(path, 'rb') as handle:
            data = pickle.load(handle)
        
        searchTree.root = Node()
        searchTree.currentNode = searchTree.root
        searchTree.root.gameState = data["state"]
        searchTree.root.playerType = MaxMinPlayer.MAX_PLAYER if data["playerType"] == 1 else MaxMinPlayer.MIN_PLAYER
        treeCreator = TreeCreator()
        treeCreator.create_tree(searchTree.currentNode)
        return searchTree
