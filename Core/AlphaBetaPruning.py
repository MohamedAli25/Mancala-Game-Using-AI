'''
class pruning_alg :

   ~Attributes :
         Node

   ~Methods :

    # required output
    # should print the chosen next optimal state /node after runnning minmax w alphabeta pruning alg
    *get_next_node(node) -> node

    # for debugging
    # print alphas and betas for every node in the given tree
    *check_correctness ()

'''
import sys
from Node import Node
from Enums import *
import numpy as np


print(sys.getrecursionlimit())



class Pruner:
      def __init__(self, node : Node):

            self.root = node
            self.sol = self._run_pruning(self.root)

      def _run_pruning(self , current : Node):

            if current.children is not None:
                  print(current.children , type(current.children))
                  for child in current.children:
                        #look ahead for leaf nodes
                        if child.children is not None :
                              #found leaf nodes ; take the limits as they are @root                                    
                              child.alpha = current.alpha
                              child.beta = current.beta
                              #run recursively
                              self._run_pruning(child)
                        else : # children of this node are leaves 
                              for leaf in current.children :
                                    self._update_node(current,leaf)
                                    #cutoff handling 
                                    if current.alpha >= current.beta : break 
                              
                              #update alpha and beta for parent node 
                              self._update_parent_node (current)    
                              #cutoff handling 
                              if current.parrentNode.alpha >= current.parrentNode.beta : break 
                        #update alpha and beta for parent node 
                        self._update_parent_node (current)    
                        #cutoff handling 
                        if current.alpha >= current.beta : break 
            return

      def _update_parent_node (self , current) : 
                        
             #update node's parent
            try :              
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
            except : pass
      
      def _update_node (self ,current,child) :
               
                # update current node
                 
            if current.playerType == MaxMinPlayer.MAX_PLAYER:
                  # update alpha if node is maximizer
                  current.alpha = self._update_alpha(child.score,current.alpha)
                  current.score = current.alpha

            else:  # its minimizer node
                  # update beta if node is minimizer
                  current.beta = self._update_beta(child.score,current.beta)
                  current.score = current.beta

                  
      
      def _update_beta(self , betanew, betaold):
            # modify beta if betanew< betaold
            return min(betanew,betaold)

      def _update_alpha(self, alphanew, alphaold):
             # modify alpha if alphanew> alpha old
            return max(alphanew,alphaold)


#driver 
if __name__== '__main__' :
      root = Node()
      n=[]
      for i in range(39) : 
            n.append(Node())
      root.children = n[0:3]
      n[0].children = n[4:7]
      n[1].children = n[7:9]
      n[2].children = n[10:12]
      n[0].parrentNode = root
      n[1].parrentNode = root
      n[2].parrentNode = root
      for i in range(3,12) :
            n[i].children = n[(12+(i-3)*3):(15+(i-3)*3)]
            n[i].parrentNode = n[(i-3)//3]
      
      scores = [8,2,2,7,4,1,3,3,3,1,2,5,3,1,2,6,1,4,9,9,9,1,8,9,9,1,0]
      print (len(scores))
      for i in range (12,39):
            
            n[i].score =scores[i-12]
            n[i].parrentNode = n[((i-12)//3)+3 ]
      pruner = Pruner(root)
      
      print(root.alpha , root.beta)
      
      
