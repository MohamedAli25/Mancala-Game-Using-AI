from Enums import MaxMinPlayer
from Node import Node
from TreeCreator import TreeCreator


class SearchTree:
    def __init__(self) -> None:
        self.root = Node()
        self.currentNode: Node = self.root
        self.root.gameState = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
        self.root.playerType = MaxMinPlayer.MAX_PLAYER

    def make_move(self, index) -> None:
        if self.currentNode.playerType is MaxMinPlayer.MAX_PLAYER:
            assert 0 <= index <= 5
        else:
            assert 7 <= index <= 12
        self.currentNode = self.currentNode.children[index]

    def get_game_state(self):
        return self.currentNode.gameState


if __name__ == "__main__":
    searchTree = SearchTree()
    treeCreator = TreeCreator()
    treeCreator.create_tree(searchTree.currentNode)
    print(searchTree.currentNode.children)
    print(searchTree.get_game_state())
    print(searchTree.currentNode.playerType)
    searchTree.make_move(5)
    print(searchTree.currentNode.children)
    print(searchTree.get_game_state())
    print(searchTree.currentNode.playerType)
    searchTree.make_move(9)
    print(searchTree.currentNode.children)
    print(searchTree.get_game_state())
    print(searchTree.currentNode.playerType)
    searchTree.make_move(1)
    print(searchTree.currentNode.children)
    print(searchTree.get_game_state())
    print(searchTree.currentNode.playerType)
