from Node import Node


class SearchTree:
    def __init__(self) -> None:
        self.root = Node()
        self.currentNode: Node = self.root
        self.root.gameState = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]

    def make_move(self, indx) -> None:
        self.currentNode = self.currentNode.children[indx]
    
    def get_game_state(self):
        return self.currentNode.gameState

# if __name__ == "__main__":
#     s = SearchTree()
#     print(s.currentNode.getScore_playerA)
#     # print('Current Node game state:', s.get_game_state())