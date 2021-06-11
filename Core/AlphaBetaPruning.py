from Core.Enums import *
from Core.Node import Node


# print(sys.getrecursionlimit())



class Pruner:
    def __init__(self, node: Node):
        self.root = node
        self._updateLeavesScore(self.root)
        self._run_pruning(self.root)
        self.update_bestMoveInd()

    def _run_pruning(self, current: Node):

        if current.children is not None:

            for child in list(current.children.values()):
                # look ahead for leaf nodes
                if child.children is not None:
                    child.alpha = current.alpha
                    child.beta = current.beta
                    # run recursively
                    self._run_pruning(child)
                else:
                    # children of this node are leaves
                    for leaf in list(current.children.values()):
                        self._update_node(current, leaf)
                        # cutoff handling
                        if current.alpha >= current.beta:
                            # print('cut1!')
                            break

                    # update alpha and beta for parent node
                    self._update_parent_node(current)
                    # cutoff handling
                    try :
                        if current.parrentNode.alpha >= current.parrentNode.beta:
                            # print('cut2!')
                            break
                    except: pass
            # update alpha and beta for parent node
            self._update_parent_node(current)
            # cutoff handling

        return

    def _update_parent_node(self, current):

        # update node's parent
        try:
            if current.parrentNode.playerType == MaxMinPlayer.MAX_PLAYER:
                # update alpha if node is maximizer
                current.parrentNode.alpha = self._update_alpha(current.score,
                                                               current.parrentNode.alpha)
                current.parrentNode.score = current.parrentNode.alpha

            else:  # its minimizer node
                # update beta if node is minimizer
                current.parrentNode.beta = self._update_beta(current.score,
                                                             current.parrentNode.beta)
                current.parrentNode.score = current.parrentNode.beta
        except:
            pass

    def _update_node(self, current, child):

        # update current node
        if current.playerType == MaxMinPlayer.MAX_PLAYER:
            # update alpha if node is maximizer
            current.alpha = self._update_alpha(child.score, current.alpha)
            current.score = current.alpha

        else:  # its minimizer node
            # update beta if node is minimizer
            current.beta = self._update_beta(child.score, current.beta)
            current.score = current.beta

    def _update_beta(self, betanew, betaold):
        # modify beta if betanew< betaold
        return min(betanew, betaold)

    def _update_alpha(self, alphanew, alphaold):
        # modify alpha if alphanew> alpha old
        return max(alphanew, alphaold)

    def update_bestMoveInd(self):
        self._update_bestMoveInd(self.root)

    def _update_bestMoveInd(self, current):

        try:
            for index, child in enumerate(list(current.children.values())):

                self._update_bestMoveInd(child)
                if current.playerType == MaxMinPlayer.MAX_PLAYER:
                    if current.bestMoveIndex is None or (child.score > list(current.children.values())[current.bestMoveIndex].score):
                        current.bestMoveIndex = list(current.children.keys())[index]
                else:
                    if current.bestMoveIndex is None or (child.score < list(current.children.values())[current.bestMoveIndex].score):
                        current.bestMoveIndex = list(current.children.keys())[index]

        except:
            pass
    
    def _updateLeavesScore (self , node):
        
        if node.children is None : 
            node.score = node.get_score()
            #print ("here",node.children)
            return
        for child in list(node.children.values()) : 
            self._updateLeavesScore(child)
            

# driver
if __name__ == '__main__':

    root = Node()
    n = []

    # ------TestCase1-----#
    for i in range(39):
        n.append(Node())
    n[0].playerType = MaxMinPlayer.MIN_PLAYER
    n[1].playerType = MaxMinPlayer.MIN_PLAYER
    n[2].playerType = MaxMinPlayer.MIN_PLAYER
    root.children = n[0:3]
    n[0].children = n[3:6]
    n[1].children = n[6:9]
    n[2].children = n[9:12]
    n[0].parrentNode = root
    n[1].parrentNode = root
    n[2].parrentNode = root
    for i in range(3, 12):
        n[i].children = n[(12 + (i - 3) * 3):(15 + (i - 3) * 3)]
        n[i].parrentNode = n[(i - 3) // 3]

    scores = [8, 2, 2, 7, 4, 1, 3, 3, 3, 1, 2, 5, 3, 1, 2, 6, 1, 4, 9, 9, 9, 1, 8, 9, 9, 1, 0]

    for i in range(12, 39):
        n[i].score = scores[i - 12]
        n[i].parrentNode = n[((i - 12) // 3) + 3]

    # ------------TestCase2-------------#
    # root.playerType = MaxMinPlayer.MIN_PLAYER
    # for i in range(30):
    #     n.append(Node())

    # n[2].playerType = MaxMinPlayer.MIN_PLAYER
    # n[3].playerType = MaxMinPlayer.MIN_PLAYER
    # n[4].playerType = MaxMinPlayer.MIN_PLAYER
    # n[5].playerType = MaxMinPlayer.MIN_PLAYER

    # root.children = n[0:2]
    # n[0].children = n[2:4]
    # n[1].children = n[4:6]

    # n[2].children = n[6:8]
    # n[3].children = n[8:10]
    # n[4].children = n[10:12]
    # n[5].children = n[12:14]

    # n[0].parrentNode = root
    # n[1].parrentNode = root
    # n[2].parrentNode = n[0]
    # n[3].parrentNode = n[0]
    # n[4].parrentNode = n[1]
    # n[5].parrentNode = n[1]

    # for i in range(6, 14):
    #     n[i].children = n[(6+(i-2)*2):(8+(i-2)*2)]
    #     n[i].parrentNode = n[((i-6)//2) + 2]

    # scores = [6, 4, 8, 6, 4, 0, 2, 2, 7, 4, 9, 3, 3, 3, 2, 0]

    # for i in range(14, 30):
    #     n[i].score = scores[i-14]
    #     n[i].parrentNode = n[((i-14)//2)+2]

    pruner = Pruner(root)

    pruner.update_bestMoveInd()
    print("root  ", ": [", root.alpha, " , ", root.beta, "]", " ,score : ", root.score, " , bestindex : ",
          root.bestMoveIndex)
    for i in range(39):
        print("node ", i, ": [", n[i].alpha, " , ", n[i].beta, "]", " ,score : ", n[i].score, " , bestindex : ",
              n[i].bestMoveIndex)
