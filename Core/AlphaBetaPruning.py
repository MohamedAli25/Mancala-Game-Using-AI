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
from enum import Enum
import Node
import Enums

print(sys.getrecursionlimit())



class pruning_alg:
      def __init__(self, node):

            self.root = node
            # run alpha beta pruning
            self.sol = _run_pruning(self.root)

      def _run_pruning(current):

            if current.children is not None:
                  for child in current.children:
                        _run_pruning(child)

            _update_node(current)
            _update_parent_node (current)    
            
            
            return

      def _update_parent_node (current) : 
                        
             #update node's parent
            if current.parentNode is not None : 
                  _update_node (current._update_parent_node)
      
      
      
      def _update_node (current) :
               
                # update current node
                 
            if current.maxMin == MaxMinPlayer.MAX_PLAYER:
                  # update alpha if node is maximizer
                  current.alpha = _update_alpha(current.score,current.alpha)
                  current.score = current.alpha

            else:  # its minimizer node
                  # update beta if node is minimizer
                  current.beta = _update_beta(current.score,current.beta)
                  current.score = current.beta

                  
      
      def _update_beta(betanew, betaold):
            # modify beta if betanew< betaold
            if betanew < betaold:
                  return betanew
            return betaold

      def _update_alpha(alphanew, alphaold):
             # modify alpha if alphanew> alpha old
            if alphanew > alphaold:
                  return alphanew
            return alphaold
