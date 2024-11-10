#!/usr/bin/env python3
import random

from fishing_game_core.game_tree import Node
from fishing_game_core.player_utils import PlayerController
from fishing_game_core.shared import ACTION_TO_STR


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

            distancelist.append(  ((hookx-fishesx)**2+(hooky-fishesy)**2)**0.5  )

            #print("fishesCORD: ", node.state.fish_positions[key], "distance: ", ((hookx-fishesx)**2+(hooky-fishesy)**2)**0.5)

        if len(distancelist) > 0:
            mindistance = min(distancelist)
        else:
            mindistance = 0

        return mindistance

    def calc_heuristics(self, node):

        #print("@@@@@@@@",node.state.hook_positions[0][0], node.state.fish_positions)

        #total_score = node.state.player_scores[0] - node.state.player_scores[1]

        total_score = - self.calc_distancetoclosestfish(node)

        return total_score


    def minimax(self,node,depth_to_search,MaximizingPlayer):


        #MaxEval = -999999
        #print("depth to searcg: ", depth_to_search)



        if depth_to_search == 0:

            Eval = self.calc_heuristics(node)
            return Eval

        if MaximizingPlayer:
            print("MAXEVAL")
            MaxEval = -999999


            node.compute_and_get_children()

            MaxIndex = 0
            for i in range(0,len(node.children)):
                eval = self.minimax(node.children[i], depth_to_search - 1, False)

                #print("eval: ", eval)#,"action: ", child.state.)
                if eval > MaxEval:
                    MaxEval = eval
                    Evaldict[eval] = i

            print("MaxEval: ", MaxEval,"MaxIndex: ", MaxIndex)
            return MaxEval

        else:
            print("MINEVAL")
            MinEval = 999999

            node.compute_and_get_children()

            MinIndex = 0
            for i in range(0, len(node.children)):
                eval = self.minimax(node.children[i], depth_to_search - 1, True)

                #print("eval: ", eval)  # ,"action: ", child.state.)
                if eval < MinEval:
                    MinEval = eval
                    Evaldict[eval] = i

            print("MinEval: ", MinEval, "MinIndex: ", MinIndex)
            return MinEval


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
        Evaldict = {}

        bestscore = self.minimax(initial_tree_node,4,True)
        index = Evaldict[bestscore]
        print("bestscore ", bestscore)


        #random_move = random.randrange(1)
        return ACTION_TO_STR[index]
