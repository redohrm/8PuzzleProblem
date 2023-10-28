#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# PROGRAMMER: Ruth Dohrmann
# PROGRAM: random-board.py
# 
# Description: This program reads the input configuration from standard
# input and accept two command-line arguments (the random number 
# generator seed and the number of random moves to make) and prints a
# final board configuration to standard output in the same format as 
# the input file format.
import sys, numpy.random as random

if (len(sys.argv) != 3):
    print()
    print("Usage: %s [seed] [number of random moves]" %(sys.argv[0]))
    print()
    sys.exit(1)

# There is no error checking in this code;
# well formatted input is assumed
def main():
    board = []
    # read the board from standard input
    for line in sys.stdin:
        board += line.split()
    
    # Set up random number generator
    rng = random.default_rng(int(sys.argv[1]))
    number_of_moves = int(sys.argv[2])
    blank_index = 0
    
    # Called as many times as needed to generate moves
    for x in range(number_of_moves):
        # The moves are 0,1,2,3 which are each
        # associated with a particular movement direction
        # (0=up, 1=down, 2=left, 3=right).
        move = rng.integers(4)
        # Bounds checking
        while (move==0 and blank_index<3) or (move==1 and blank_index>5) or (move==2 and blank_index%3==0)\
        or (move==3 and blank_index%3==2):
            move = rng.integers(4)
        if move==0:
            new_index = blank_index - 3
        elif move==1:
            new_index = blank_index + 3
        elif move==2:
            new_index = blank_index - 1
        else:
            new_index = blank_index + 1
        # swap board tiles
        board = swap(blank_index, new_index, board)
        blank_index = new_index

    # output board
    for x in range(9):
        print(f"{board[x]}", end=" ")
        if x%3==2:
            print()

# swap function: swap list items at indices blank_index and new_index
def swap(blank_index, new_index, board):
    temp = board[blank_index]
    board[blank_index] = board[new_index]
    board[new_index] = temp
    return board
        
main()