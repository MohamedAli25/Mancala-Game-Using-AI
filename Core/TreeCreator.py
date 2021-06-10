from Enums import MaxMinPlayer, GameMode
from Node import Node
from Settings import Settings


class TreeCreator:
    def __init__(self):
        self.__treeDepth = Settings.GAME_DIFFICULTY.value
        self.__gameMode = Settings.GAME_MODE

    def create_tree(self, node: Node):
        self.__create_tree_of_depth(node, self.__treeDepth)

    def __create_tree_of_depth(self, node: Node, treeDepth: int):
        if treeDepth == 0:
            return
        node.children = {}
        if node.playerType == MaxMinPlayer.MAX_PLAYER:
            for i in range(6):
                if node.gameState[i] != 0:
                    newNode = Node()
                    numOfStones = node.gameState[i]
                    currentIndex = i
                    newGameState = node.gameState[:]
                    newGameState[i] = 0
                    while numOfStones != 0:
                        currentIndex = (currentIndex + 1) % 14
                        if currentIndex == 13:
                            continue
                        newGameState[currentIndex] += 1
                        numOfStones -= 1
                    newNode.playerType = MaxMinPlayer.MAX_PLAYER if currentIndex == 6 else MaxMinPlayer.MIN_PLAYER
                    if 0 <= currentIndex <= 5 and newGameState[currentIndex] == 1\
                            and self.__gameMode is GameMode.STEALING:
                        oppositeIndex = 12 - currentIndex
                        newGameState[6] += newGameState[currentIndex]
                        newGameState[6] += newGameState[oppositeIndex]
                        newGameState[currentIndex] = 0
                        newGameState[oppositeIndex] = 0
                    if self.__is_game_state_finished(newGameState):
                        self.__finish_game(newGameState)
                    newNode.gameState = newGameState
                    newNode.parentNode = self
                    node.children[i] = newNode
        else:
            for i in range(7, 13):
                if node.gameState[i] != 0:
                    newNode = Node()
                    numOfStones = node.gameState[i]
                    currentIndex = i
                    newGameState = node.gameState[:]
                    newGameState[i] = 0
                    while numOfStones != 0:
                        currentIndex = (currentIndex + 1) % 14
                        if currentIndex == 6:
                            continue
                        newGameState[currentIndex] += 1
                        numOfStones -= 1
                    newNode.playerType = MaxMinPlayer.MIN_PLAYER if currentIndex == 13 else MaxMinPlayer.MAX_PLAYER
                    if 7 <= currentIndex <= 12 and newGameState[currentIndex] == 1 \
                            and self.__gameMode is GameMode.STEALING:
                        oppositeIndex = 12 - currentIndex
                        newGameState[13] += newGameState[currentIndex]
                        newGameState[13] += newGameState[oppositeIndex]
                        newGameState[currentIndex] = 0
                        newGameState[oppositeIndex] = 0
                    if self.__is_game_state_finished(newGameState):
                        self.__finish_game(newGameState)
                    newNode.gameState = newGameState
                    newNode.parentNode = self
                    node.children[i] = newNode
        for moveIndex in node.children.keys():
            self.__create_tree_of_depth(node.children[moveIndex], treeDepth - 1)

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

    def __finish_game(self, gameState: list):
        for i in range(6):
            gameState[6] += gameState[i]
        for i in range(6):
            gameState[i] = 0
        for i in range(7, 13):
            gameState[13] += gameState[i]
        for i in range(7, 13):
            gameState[i] = 0
