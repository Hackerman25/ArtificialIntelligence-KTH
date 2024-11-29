#!/usr/bin/env python3
import random

from fishing_game_core.game_tree import Node
from fishing_game_core.player_utils import PlayerController
from fishing_game_core.shared import ACTION_TO_STR
import time

class PlayerControllerHuman(PlayerController):
    def player_loop(self):
        """
        Function that generates the loop of the game. In each iteration
        the human plays through the keyboard and send
        this to the game through the sender. Then it receives an
        update of the game through receiver, with this it computes the
        next movement.
        :return:
        """

        while True:
            # send message to game that you are ready
            msg = self.receiver()
            if msg["game_over"]:
                return


class PlayerControllerMinimax(PlayerController):

    def __init__(self):
        super(PlayerControllerMinimax, self).__init__()

    def player_loop(self):
        """
        Main loop for the minimax next move search.
        :return:
        """

        # Generate first message (Do not remove this line!)
        first_msg = self.receiver()

        while True:
            msg = self.receiver()

            # Create the root node of the game tree
            node = Node(message=msg, player=0)

            # Possible next moves: "stay", "left", "right", "up", "down"
            best_move = self.search_best_next_move(initial_tree_node=node)

            # Execute next action
            self.sender({"action": best_move, "search_time": None})


    def calc_distancetoclosestfish(self, node):

        distancelist = []

        #print("YYY length of fish pos: ", len(node.state.fish_positions), "dict: ", node.state.fish_positions)
        for key in node.state.fish_positions:
            #print("fish", node.state.fish_positions[i][0])
            #print("hook", node.state.hook_positions[0])

            hookx = node.state.hook_positions[0][0]
            hooky = node.state.hook_positions[0][1]


            fishesx = node.state.fish_positions[key][0]
            fishesy = node.state.fish_positions[key][1]

            distancelist.append(  abs( min((hookx-fishesx),20-(hookx-fishesx))) + abs((hooky-fishesy)))

            #print("fishesCORD: ", node.state.fish_positions[key], "distance: ", ((hookx-fishesx)**2+(hooky-fishesy)**2)**0.5)

        if len(distancelist) > 0:
            mindistance = min(distancelist)
        else:
            mindistance = 0

        return mindistance

    def calc_heuristics(self, node):

        distance_score = - self.calc_distancetoclosestfish(node)


        #print("score: ", node.state.player_scores[0] , node.state.player_scores[1])

        player_score =   node.state.player_scores[0] - node.state.player_scores[1]
        #print("points:" , player_score)
        return 5* player_score + distance_score


    def minimax(self,node,depth_to_search,MaximizingPlayer):

        if depth_to_search == 0:

            Eval = self.calc_heuristics(node)
            return Eval

        if MaximizingPlayer:
            #print("MAXEVAL")
            MaxEval = float('-inf')


            node.compute_and_get_children()

            MaxIndex = 0
            for i in range(0,len(node.children)):
                eval = self.minimax(node.children[i], depth_to_search - 1, False)

                #print("eval: ", eval)#,"action: ", child.state.)
                if eval > MaxEval:
                    MaxEval = eval
                    Evaldict[eval] = i

            #print("MaxEval: ", MaxEval,"MaxIndex: ", MaxIndex)
            return MaxEval

        else:
            #print("MINEVAL")
            MinEval = float('inf')

            node.compute_and_get_children()

            for i in range(0, len(node.children)):
                eval = self.minimax(node.children[i], depth_to_search - 1, True)

                #print("eval: ", eval)  # ,"action: ", child.state.)
                if eval < MinEval:
                    MinEval = eval
                    Evaldict[eval] = i

            #print("MinEval: ", MinEval, "MinIndex: ", MinIndex)
            return MinEval


    def alphabeta(self,node,state,depth_to_search,alpha,beta,initial_time,nodes_seen,MaximizingPlayer):
        #s t a t e : the curren t s t a t e we are analyzing
        #α: the curren t be s t value ach ievab le by A
        #β: the curren t be s t value ach ievab le by B
        #p layer : the curren t p layer
        #re turn s the minimax value o f the s t a t e


        if time.time() - initial_time > 0.071:
            raise TimeoutError
        else:

            #check for repeated states
            hashkey  = self.hash_table(state)[0]
            if hashkey in nodes_seen and nodes_seen[hashkey] >= depth_to_search:
                print("REPEATED STATES")
                return nodes_seen[hashkey][0] , nodes_seen[hashkey][1]


            children = node.compute_and_get_children()



            #children.sort(key = self.calc_heuristics,reverse = True) # HERE WRONG BCUZ min max depending on player!!
            #print("children: ", children.state.player_scores[0], type(children))

            if depth_to_search == 0 or len(children) == 0:
                return self.calc_heuristics(node), 0

            best_index = 0


            if MaximizingPlayer == True:
                v = float('-inf')
                for i in range(0,len(node.children)):
                    eval, action = self.alphabeta(node.children[i],node.children[i].state, depth_to_search - 1,alpha,beta, initial_time,nodes_seen,False)

                    #print("eval: ", eval, "action: ", action)
                    if eval > v:
                        v = eval
                        best_index = i

                    alpha = max(alpha,v)
                    if beta <= alpha:
                        break

            else:
                v = float('inf')      #THIS One
                for i in range(0, len(node.children)):
                    eval, action = self.alphabeta(node.children[i], node.children[i].state, depth_to_search - 1, alpha, beta, initial_time,nodes_seen,True)

                    #print("eval: ", eval, "action: ", action)
                    if eval < v:
                        v = eval
                        best_index = i

                    beta = min(beta, v)
                    if beta >= alpha:
                        break

            hashkey = self.hash_table(state)
            nodes_seen.update({hashkey:[v,best_index]})
        return v, best_index

    def hash_table(self,state):


        fishpos = state.get_fish_positions().items()
        hookx = state.hook_positions[0][0]
        hooky = state.hook_positions[0][1]

        return str(fishpos) + str(hookx) + str(hooky)

    def iterative_deepening_search(self, node, nodes_seen,max_depth):
        initial_time = time.time()

        best_move = 0

        #value, best_move = self.alphabeta(node, 2, float('-inf'), float('inf'), initial_time, True)

        try:



            for depth in range(1, max_depth + 1):
                value, move = self.alphabeta(node, node.state, depth, -float('inf'), float('inf'), initial_time, nodes_seen, True)
                best_move = move
                #print(best_move, value)


        except TimeoutError:
            pass

        return best_move



    def search_best_next_move(self, initial_tree_node):
        """
        Use minimax (and extensions) to find best possible next move for player 0 (green boat)
        :param initial_tree_node: Initial game tree node
        :type initial_tree_node: game_tree.Node
            (see the Node class in game_tree.py for more information!)
        :return: either "stay", "left", "right", "up" or "down"
        :rtype: str
        """

        # EDIT THIS METHOD TO RETURN BEST NEXT POSSIBLE MODE USING MINIMAX ###

        # NOTE: Don't forget to initialize the children of the current node
        #       with its compute_and_get_children() method!


        #print(initial_tree_node.compute_and_get_children())
        #print(initial_tree_node.children)

        global Evaldict
        Evaldict = 0

        #bestscore = self.minimax(initial_tree_node,4,True)

        alpha = float('-inf')
        beta = float('inf')
        initial_time = time.time()
        nodes_seen = dict()

        #bestscore, best_index= self.alphabeta(initial_tree_node,initial_tree_node.state,3,alpha,beta,initial_time,nodes_seen,True)

        best_index = self.iterative_deepening_search(initial_tree_node, nodes_seen, 20)

        #print("bestscore ", bestscore,"action: ", best_index)


        #random_move = random.randrange(1)
        return ACTION_TO_STR[best_index]
