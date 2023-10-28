#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# PROGRAMMER: Ruth Dohrmann
# PROGRAM: a-star.py
# 
# Description: This program utilizes A* search to solve an 8-puzzle problem.
# The user can choose between 4 heuristics (h(n) = 0; h(n) = Number of tiles 
# displaced from the goal; h(n) = Sum of Manhattan (city-block) distances of 
# all tiles from the goal; h(n) = Sum of Manhattan (city-block) distances of 
# all tiles from the goal plus the sum of displaced tiles not located directly
# next to the blank tile).
import sys, numpy.random as random
import heapq
import copy

# Set for closed list
class Set():
    def __init__(self):
        self.thisSet = set()
    def add(self,entry):
        if entry is not None:
            self.thisSet.add(entry.__hash__())
    def length(self):
        return len(self.thisSet)
    # check whether or not 'query' is in the set
    def isMember(self,query):
        return query.__hash__() in self.thisSet

# Board state; keeps track of the tiles' order as well as the index of blank tile
class state():
    def __init__(self, xpos = 0, ypos = 0, tiles = [[0,1,2],[3,4,5],[6,7,8]]):
        self.xpos = xpos
        self.ypos = ypos
        self.tiles = tiles
    def board(self):
        return self.tiles
    def left(self):
        # check tile position
        if (self.ypos == 0):
            return None
        # create a deep copy
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos][s.ypos-1]
        s.ypos -= 1
        s.tiles[s.xpos][s.ypos] = 0
        return s
    def right(self):
        # check tile position
        if (self.ypos == 2):
            return None
        # create a deep copy
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos][s.ypos+1]
        s.ypos += 1
        s.tiles[s.xpos][s.ypos] = 0
        return s
    def up(self):
        # check tile position
        if (self.xpos == 0):
            return None
        # create a deep copy
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos-1][s.ypos]
        s.xpos -= 1
        s.tiles[s.xpos][s.ypos] = 0
        return s
    def down(self):
        # check tile position
        if (self.xpos == 2):
            return None
        # create a deep copy
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos+1][s.ypos]
        s.xpos += 1
        s.tiles[s.xpos][s.ypos] = 0
        return s
    def __hash__(self):
        return (tuple(self.tiles[0]),tuple(self.tiles[1]),tuple(self.tiles[2]))
    def __str__(self):
        # return formatted string of the board
        return '%d %d %d\n%d %d %d\n%d %d %d\n'%(
                self.tiles[0][0],self.tiles[0][1],self.tiles[0][2],
                self.tiles[1][0],self.tiles[1][1],self.tiles[1][2],
                self.tiles[2][0],self.tiles[2][1],self.tiles[2][2])
    def copy(self):
        s = copy.deepcopy(self)
        return s
    def __eq__(self, other):
        return self.tiles == other

# Priority Queue to store the frontier
class PriorityQueue():
    def __init__(self):
        self.thisQueue = []
    def push(self, thisNode):
        # add node to queue
        heapq.heappush(self.thisQueue, (thisNode.val, -thisNode.id, thisNode))
    def pop(self):
        # pop best node (lowest val [then greatest id]) off the queue
        return heapq.heappop(self.thisQueue)[2]
    def isEmpty(self):
        return len(self.thisQueue) == 0
    def length(self):
        return len(self.thisQueue)

nodeId = 0
class node():
    # node includes f value, g value, board state, and parent node
    def __init__(self, f_val, g_val, my_state, parent):
        global nodeId
        self.id = nodeId
        nodeId += 1
        self.val = f_val
        self.g_val = g_val
        self.my_state = my_state
        self.parent_node = parent
    def getState(self):
        return self.my_state
    def getGVal(self):
        return self.g_val
    def getParent(self):
        return self.parent_node
    def __str__(self):
        # return string of board
        return f'{self.my_state}'

# check command line arguments
if (len(sys.argv) != 2):
    print()
    print("Usage: %s [h-choice]" %(sys.argv[0]))
    print()
    sys.exit(1)

desired_board = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

# There is no error checking in this code
# Well formatted input is assumed
def main():

    board = []
    board_row = []
    # Read board from stdin
    for line in sys.stdin:
        board_row += line.split()
        board.append(board_row)
        board_row = []

    # convert board items from strings to ints
    board = [[int(board[y][x]) for x in range(3)] for y in range(3)]
    h_choice = int(sys.argv[1])

    result = treeSearch(board, h_choice)
    stack = []
    if result:
        # total number of nodes visited/expanded (V)
        V = result[0]
        # maximum number of nodes stored in memory (closed list + open list size)
        N = result[1]
        current_node = result[2]
        # depth of the optimal solution
        d = current_node.getGVal()
        # Reverse path
        while (current_node):
            stack.append(current_node)
            current_node = current_node.getParent()
        # calculate branching factor
        if d != 0:
            b = N**(1/d)
        else:
            b = 0
        # print statistics
        print(f"{V=}\n{N=}\n{d=}\n{b=}\n")
        # print path
        for tree_node in range(len(stack)):
            print(stack.pop())
    else:
        print("Invalid board")


# This function searches for a path to the goal board state. It follows the general algorithm:
# Initialize a closed list as an empty set
# Initialize frontier as a priority queue containing the initial state as its first node
# while the frontier is not empty:
#   pop the front node off the frontier
#   if the node is the goal, return the node
#   else, if the node is not in the closed list:
#       add the node to the closed list
#       expand the node and add its children to the frontier
# else return false
def treeSearch(board, h_choice):
    # get the position of the blank (zero)
    for i,j  in enumerate(board):
        if 0 in j:
            initial_index=(i,j.index(0))
            break

    initial_state = state(initial_index[0], initial_index[1], board)

    frontier = PriorityQueue()
    closed_list = Set()
    h = heuristicFunction(board, h_choice)
    # root node includes: f value, g value, state, and parent (None)
    root_node = node(h, 0, initial_state, None)
    frontier.push(root_node)
    # to hold the number of nodes expanded
    V = 0
    # while the frontier is not empty, expand nodes from the frontier until the goal state is reached
    while (not frontier.isEmpty()):
        current_node = frontier.pop()
        current_state = current_node.getState()
        # check if the node's state is the desired state, return if true
        if current_state == desired_board:
            # total number of nodes in memory
            max_nodes = closed_list.length() + frontier.length()
            # return number of nodes expanded, total number of nodes in memory, and current node
            return_info = [V, max_nodes, current_node]
            return return_info
        # check if the node's state is in the closed list, expand if false
        if (not closed_list.isMember(current_state)):
            # add to closed list
            closed_list.add(current_state)
            V += 1
            node_g_val = current_node.getGVal()
            # move the upper tile down to the blank's current position
            su = current_state.up()
            if su is not None:
                h = heuristicFunction(su.board(), h_choice)
                g = node_g_val + 1
                f = g + h
                frontier.push(node(f, g, su, current_node))
            # move the lower tile up to the blank's current position
            sd = current_state.down()
            if sd is not None:
                h = heuristicFunction(sd.board(), h_choice)
                g = node_g_val + 1
                f = g + h
                frontier.push(node(f, g, sd, current_node))
            # move the left tile right to the blank's current position
            sl = current_state.left()
            if sl is not None:
                h = heuristicFunction(sl.board(), h_choice)
                g = node_g_val + 1
                f = g + h
                frontier.push(node(f, g, sl, current_node))
            # move the right tile left to the blank's current position
            sr = current_state.right()
            if sr is not None:
                h = heuristicFunction(sr.board(), h_choice)
                g = node_g_val + 1
                f = g + h
                frontier.push(node(f, g, sr, current_node))
    return False

# This function returns the value of the chosen heuristic given the current board
def heuristicFunction(board, choice):
    # choice 0: no additional information, heuristic equals zero
    if choice == 0:
        return 0
    # choice 1: add one to the heuristic for each misplaced tile
    elif choice == 1:
        # one for each misplaced tile
        heuristic_board = [[0 if (int(board[y][x]) == (x+(3*y))) else 1 for x in range(3)] for y in range(3)]
        # return the sum of the 2d list
        return sum(map(sum,heuristic_board))
    # choice 2: add the distance from its desired position to the heuristic for each misplaced tile
    elif choice == 2:
        size = 3
        distance2 = 0
        heuristic_board = []
        for y in range(size):
            for x in range(size):
                # check if the tile is in the correct position
                if board[y][x] != x+3*y:
                    # find the location of the tile in the desired board
                    for i,j  in enumerate(desired_board):
                        if int(board[y][x]) in j:
                            index=(i,j.index(int(board[y][x])))
                            break
                    # calculate the distance from the desired position
                    distance = abs(index[0] - y)
                    distance += abs(index[1] - x)
                    distance2 += distance
                    heuristic_board.append(distance)
                else:
                    heuristic_board.append(0)
        return sum(heuristic_board)
    # choice 3: heuristic value of choice 2 plus one for each misplaced title not directly next to
    # the blank tile (the zero) 
    elif choice == 3:
        size = 3
        heuristic_board = []
        distance = 0
        additional_sum = 0
        for y in range(size):
            for x in range(size):
                if board[y][x] != x+3*y:
                    # find the location of the tile in the desired board
                    for i,j  in enumerate(desired_board):
                        if board[y][x] in j:
                            index=(i,j.index(board[y][x]))
                            break
                    # find the location of the 0 on the current board
                    for i,j  in enumerate(board):
                        if 0 in j:
                            index_blank=(i,j.index(0))
                            break
                    distance += abs(index[0] - y)
                    distance += abs(index[1] - x)
                    distance2 = abs(index_blank[0] - y)
                    distance2 += abs(index_blank[1] - x)
                    # if the displaced tile is not directly next to the blank,
                    # add one to the additional sum
                    if distance2 > 1:
                        additional_sum += 1
        total_sum = distance+additional_sum
        return total_sum

      
main()