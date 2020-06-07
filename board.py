# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 16:57:33 2017

@author: RoySorce
"""

from copy import deepcopy 
import math
import random
import aihelper
import aiantagonist

class Board():
        
    def __init__(self):
        self.board = [[0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]]
        self.shifts_made = list()
        self.tiles_placed = list()
        self.shifters_turn = False
        self.previous_board_state = None
        self.human = True
        self.killSwitch = False
        
    def __str__(self):
        output = ""
        for x in range(len(self.board)):
            for y in range(len(self.board[x])):
                chars = len(str(self.board[x][y]))
                if(chars == 4):
                    output += " " + str(self.board[x][y])
                elif(chars == 3):
                    output += " " + str(self.board[x][y]) + " "
                elif(chars == 2):
                    output += "  " + str(self.board[x][y]) + "  "
                else: 
                    output += "   " + str(self.board[x][y]) + "  "
            output += "\n"
        
        return output
    
    #randomly select 2 tiles to start the game
    def startGame(self):
        
        self.previous_board_state = deepcopy(self.board)
                    
        tile1x = random.randint(0, 3)
        tile1y = random.randint(0, 3)
        val1 = random.randint(1, 10)
        if(val1 != 10):
            self.board[tile1x][tile1y] = 2
            self.tiles_placed.append(((tile1x, tile1y), 2))
        else:
            self.board[tile1x][tile1y] = 4
            self.tiles_placed.append(((tile1x, tile1y), 4))
        
        tile2x = random.randint(0, 3)
        tile2y = random.randint(0, 3)
        val2 = random.randint(1, 10)
        
        while(tile1x == tile2x and tile1y == tile2y):
            tile2x = random.randint(0, 3)
            tile2y = random.randint(0, 3)
            
        if(val2 != 10):
            self.board[tile2x][tile2y] = 2
            self.tiles_placed.append(((tile2x, tile2y), 2))
        else:
            self.board[tile2x][tile2y] = 4
            self.tiles_placed.append(((tile2x, tile2y), 4))
        
        self.shifters_turn = True
        
    def availableSpaces(self):
        openSpaces = list()
        for x in range(len(self.board)):
            for y in range(len(self.board[x])):
                if(self.board[x][y] == 0):
                    openSpaces.append((x,y))
        return openSpaces
        
    def generateMoves(self):
        if(self.shifters_turn):
            return self.generateMoves_ShiftTiles()
        else:
            return self.generateMoves_PlaceTiles()
        
    def generateMoves_ShiftTiles(self):
        moves = list()
        terminate = False
        #right shift available
        for x in range(len(self.board)):
            if(terminate):
                break
            for y in range(len(self.board[x]) - 1): 
                if(self.board[x][y] != 0):
                    if(self.board[x][y+1] == 0 or self.board[x][y+1] == self.board[x][y]):
                        moves.append("right")
                        terminate = True
                        break
        #left shift available
        terminate = False
        for x in range(len(self.board)):
            if(terminate):
                break
            for y in range(len(self.board[x]) - 1, 0, -1):
                if(self.board[x][y] != 0):
                    if(self.board[x][y-1] == 0 or self.board[x][y-1] == self.board[x][y]):
                        moves.append("left")
                        terminate = True
                        break
        #down shift available
        terminate = False
        for x in range(len(self.board) - 1):
            if(terminate):
                break
            for y in range(len(self.board[x])):
                if(self.board[x][y] != 0):
                    if(self.board[x+1][y] == 0 or self.board[x+1][y] == self.board[x][y]):
                        moves.append("down")
                        terminate = True
                        break
        #up shift available
        terminate = False
        for x in range(len(self.board) - 1, 0, -1):
            if(terminate):
                break
            for y in range(len(self.board[x])):
                if(self.board[x][y] != 0):
                    if(self.board[x-1][y] == 0 or self.board[x-1][y] == self.board[x][y]):
                        moves.append("up")
                        terminate = True
                        break
        return moves
        
    def generateMoves_PlaceTiles(self):
        moves = list()
        for x in self.availableSpaces():
            moves.append((x, 2))
            moves.append((x, 4))
        return moves
            
    def previewMove(self, move):
        copy_of_self = deepcopy(self)
        
        if(copy_of_self.shifters_turn): #shift tiles
            copy_of_self.makeMoves_ShiftTiles(move)
        else: #place tiles
            copy_of_self.makeMoves_PlaceTiles(move)
        copy_of_self.shifters_turn = not(copy_of_self.shifters_turn)
        return copy_of_self
    
    def humanPlay(self, code):
        if(code == "w"):
            move = "up"
        elif(code == "s"):
            move = "down"
        elif(code == "a"):
            move = "left"
        elif(code == "d"):
            move = "right"
        elif(code == "p"):
            move = "kill"
        else:
            move = self.humanPlay(input("Unrecognized key, try again: "))
            
        if(move not in self.generateMoves_ShiftTiles() and move != "kill"):
            print("cannot shift %s: it will do nothing to current board" % move)
            move = self.humanPlay(input("Input new key: "))
        return move
    
    def makeMoves(self, move = None):
        if(self.shifters_turn): #shift tiles
            if(self.human):
                keyCode = input("Your turn: ")
                move = self.humanPlay(keyCode)
                #print("you moved %s" % move)
            self.makeMoves_ShiftTiles(move)
        else: #place tiles
            self.makeMoves_PlaceTiles(move)
        self.shifters_turn = not(self.shifters_turn)
    
    def makeMoves_ShiftTiles(self, direction):
        
        self.previous_board_state = deepcopy(self.board)
        if(direction == None): #random move selection
            print("random move being made")
            direction = random.choice(self.generateMoves_ShiftTiles())    
        self.shifts_made.append(direction)
        
        if(direction == "up"):
            self.board = self.shift_up()
        elif(direction == "down"):
            self.board = self.shift_down()
        elif(direction == "left"):
            self.board = self.shift_left()
        elif(direction == "right"):
            self.board = self.shift_right() 
        elif(direction == "kill"):
            self.killSwitch = True
        else: # this should never be reached
            print("error, wrong argument: %s" % direction)
    
    def shift_up(self):
        #print("SHIFTING UP")
        board = deepcopy(self.board)
        zero_spaces = list()
        #shift and merge up
        for x in range(4):
            for y in range(4):
                if(board[y][x] == 0):
                    zero_spaces.append(y)
                elif(zero_spaces):
                    top_most_open = zero_spaces.pop(0)
                    board[top_most_open][x] = board[y][x]
                    board[y][x] = 0
                    zero_spaces.append(y)
                    if(top_most_open > 0):
                        if(board[top_most_open][x] == board[top_most_open - 1][x]):
                            #print("merging at column %d" % x)
                            board[top_most_open - 1][x] = board[top_most_open - 1][x]*2
                            board[top_most_open][x] = 0
                            zero_spaces.insert(0, top_most_open)
                elif(y > 0 and board[y-1][x] == board[y][x]):
                    #print("merging at column %d" % x)
                    board[y-1][x] = board[y-1][x]*2
                    board[y][x] = 0
                    zero_spaces.insert(0, y)
            zero_spaces.clear()
        return board
    
    def shift_down(self):
        #print("SHIFTING DOWN")
        board = deepcopy(self.board)
        zero_spaces = list()
        #shift and merge down
        for x in range(4):
            for y in range(3, -1, -1):
                if(board[y][x] == 0):
                    zero_spaces.append(y)
                elif(zero_spaces):
                    bottom_most_open = zero_spaces.pop(0)
                    board[bottom_most_open][x] = board[y][x]
                    board[y][x] = 0
                    zero_spaces.append(y)
                    if(bottom_most_open < 3):
                        if(board[bottom_most_open][x] == board[bottom_most_open + 1][x]):
                            #print("merging at column %d" % x)
                            board[bottom_most_open + 1][x] = board[bottom_most_open + 1][x]*2
                            board[bottom_most_open][x] = 0
                            zero_spaces.insert(0, bottom_most_open)
                elif(y < 3 and board[y + 1][x] == board[y][x]):
                    #print("merging at column %d" % x)
                    board[y + 1][x] = board[y + 1][x]*2
                    board[y][x] = 0
                    zero_spaces.insert(0, y)
            zero_spaces.clear()
        return board
    
    def shift_left(self):
        #print("SHIFTING LEFT")
        board = deepcopy(self.board)
        zero_spaces = list()
        #shift and merge left
        for x in range(4):
            for y in range(4):
                if(board[x][y] == 0):
                    zero_spaces.append(y)
                elif(zero_spaces):
                    left_most_open = zero_spaces.pop(0)
                    board[x][left_most_open] = board[x][y]
                    board[x][y] = 0
                    zero_spaces.append(y)
                    if(left_most_open > 0):
                        if(board[x][left_most_open - 1] == board[x][left_most_open]):
                            #print("merging at row %d" % x)
                            board[x][left_most_open - 1] = board[x][left_most_open - 1]*2
                            board[x][left_most_open] = 0
                            zero_spaces.insert(0, left_most_open)
                elif(y > 0 and board[x][y - 1] == board[x][y]):
                    #print("merging at row %d" % x)
                    board[x][y - 1] = board[x][y - 1]*2
                    board[x][y] = 0
                    zero_spaces.insert(0, y)
            zero_spaces.clear()
        return board
    
    def shift_right(self):
        #print("SHIFT RIGHT")
        board = deepcopy(self.board)
        zero_spaces = list()
        #shift and merge right
        for x in range(4):
            for y in range(3, -1, -1):
                if(board[x][y] == 0):
                    zero_spaces.append(y)
                elif(zero_spaces):
                    right_most_open = zero_spaces.pop(0)
                    board[x][right_most_open] = board[x][y]
                    board[x][y] = 0
                    zero_spaces.append(y)
                    if(right_most_open < 3):
                        if(board[x][right_most_open + 1] == board[x][right_most_open]):
                            #print("merging at row %d" % x)
                            board[x][right_most_open + 1] = board[x][right_most_open + 1]*2
                            board[x][right_most_open] = 0
                            zero_spaces.insert(0, right_most_open)
                elif(y < 3 and board[x][y + 1] == board[x][y]):
                    #print("merging at row %d" % x)
                    board[x][y + 1] = board[x][y + 1]*2
                    board[x][y] = 0
                    zero_spaces.insert(0, y)
            zero_spaces.clear()
        return board
    
    def makeMoves_PlaceTiles(self, move):
        
        self.previous_board_state = deepcopy(self.board)
        
        if(move != None):
            self.tiles_placed.append(move)
            self.board[move[0][0]][move[0][1]] = move[1]
        else:
            tile = random.choice(self.availableSpaces())
            value = random.randint(1, 10)
            if(value != 10):
                self.board[tile[0]][tile[1]] = 2
                self.tiles_placed.append(((tile[0], tile[1]), 2))
            else:
                self.board[tile[0]][tile[1]] = 4
                self.tiles_placed.append(((tile[0], tile[1]), 4))
                
    def adjacent(self, tuple1, tuple2):
        if(-1 < tuple1[0] < 4 
           and -1 < tuple2[0] < 4
           and -1 < tuple1[1] < 4
           and -1 < tuple2[1] < 4): #check bounds first
            if((abs(tuple2[0] - tuple1[0]) + abs(tuple2[1] - tuple1[1]) <= 1)):
                return True
        return False
            
        
    def gameOver(self):
        if(self.killSwitch):
            print("game was killed")
            return True
        elif(self.aiWon()):
            print("AI BOT WINS")
            return True
        elif(self.opponentWon()):
            return True
        else:
            return False
    
    #checks if there are no available shifts to make
    def opponentWon(self):
            return not self.generateMoves_ShiftTiles()
    
    def aiWon(self):
        for x in range(4):
            for y in range(4):
                if(self.board[x][y] == 2048):
                    return True   
        return False
    
    def maxValue(self):
        maxValue = 0
        for x in range(4):
            for y in range(4):
                if(self.board[x][y] > maxValue):
                    maxValue = self.board[x][y]
        return maxValue
    
def main():
    max_values = list()
    for x in range(1):
        b1 = Board()
        b1.startGame()
        if(b1.human):
            print("w: up, a: left, s: down, d: right\ninput one then hit enter")
        ai_good = aihelper.AIHelper(b1)
        ai_bad = aiantagonist.Antagonist(b1)
        print(b1)
        iterations = 1
        while(not b1.gameOver()):
            print(iterations)
            if(b1.shifters_turn):
                if(b1.human):
                    b1.makeMoves(None)
                else:
                    bestMove = ai_good.getMoves()
                    b1.makeMoves(bestMove)
            else:
                bestMove = ai_bad.getMoves()
                b1.makeMoves(bestMove)
            print(b1)
            iterations += 1
        max_values.append(b1.maxValue())
    print(max_values)
    #              0  1  2  3   4   5   6   7    8    9    10    11
    #              1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048
    occurrences = [0, 0, 0, 0,  0,  0,  0,  0,   0,   0,   0,    0]
    for x in max_values:
        occurrences[int(math.log(x, 2))] += 1
    print(occurrences)
    
if __name__== "__main__":
    main()