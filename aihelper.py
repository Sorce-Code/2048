# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 17:00:05 2017

@author: RoySorce
"""
import math

class AIHelper:
    
    def __init__(self, b):
        self.board = b
        self.name = "2048 Bot"
        
    def makeMove(self, move):
        self.board.makeMoves(move)
    
    def getMoves(self):
        move = self.alpha_beta(self.board, 0)
        return move
        
    def alpha_beta(self, b, depth):
        if(depth == 0):
            return None
        moves = b.generateMoves()
        bestMove = -1
        bestValue = float("-inf")
        p_inf = float("inf")
        n_inf = float("-inf")
        for x in moves:
            nextBoardState = b.previewMove(x)
            score = self.min_value_ab(nextBoardState, depth-1, p_inf, n_inf)
            if(score > bestValue):
                bestMove = x
                bestValue = score
        print("Best Value %d : Best Move %s" % (bestValue, bestMove))
        return bestMove
        
    def max_value_ab(self, b, depth, alpha, beta):
        if(depth == 0 or b.gameOver()):
            return self.evaluation(b)
        moves = b.generateMoves()
        bestValue = float("-inf")
        for x in moves:
            nextBoardState = b.previewMove(x)
            bestValue = max(bestValue, self.min_value_ab(nextBoardState, depth-1, alpha, beta))
            if(bestValue >= beta):
                return bestValue
            alpha = max(alpha, bestValue)
        return bestValue

    def min_value_ab(self, b, depth, alpha, beta):
        if(depth == 0 or b.gameOver()):
            return self.evaluation(b)
        moves = b.generateMoves()
        bestValue = float("inf")
        for x in moves:
            nextBoardState = b.previewMove(x)
            bestValue = min(bestValue, self.max_value_ab(nextBoardState, depth-1, alpha, beta))
            if(bestValue <= alpha):
                return bestValue
            beta = min(beta, bestValue)
        return bestValue
    
    def evaluation(self, b):
        board = b.board
        
        total = 0
        openSpots_total = 0
        maxValue_total = 0
        rowSmoothness_total = 0
        columnSmoothness_total = 0
        monotonic_total = 0
        cornerPack_total = 0
        
        #row smoothness AND total open spaces evaluation
        for x in range(4):
            last_non_zero_value = -1
            for y in range(4):
                if(board[x][y] != 0):
                    if(last_non_zero_value != -1): 
                        val1 = math.log(board[x][y]) / math.log(2)
                        val2 = math.log(last_non_zero_value) / math.log(2)
                        rowSmoothness_total -= abs(val1 - val2)
                    last_non_zero_value = board[x][y]
                else:
                    openSpots_total += 1
        
        #column smoothness AND max value evaluation
        biggestValue = ((-1,-1), 0)
        biggerValue = ((-1,-1), 0)
        bigValue = ((-1,-1), 0)
        for x in range(4):
            last_non_zero_value = -1
            for y in range(4):
                if(board[y][x] != 0): 
                    if(last_non_zero_value != -1):
                        val1 = math.log(board[y][x]) / math.log(2)
                        val2 = math.log(last_non_zero_value) / math.log(2)
                        columnSmoothness_total -= abs(val1 - val2)
                    last_non_zero_value = board[y][x]
                    
                if(board[y][x] > biggestValue[1]): #retrieving biggest values
                    bigValue = biggerValue
                    biggerValue = biggestValue
                    biggestValue = ((y, x), board[y][x])
                elif(board[y][x] > biggerValue[1]):
                    bigValue = biggerValue
                    biggerValue = ((y, x), board[y][x])
                elif(board[y][x] > bigValue[1]):
                    bigValue = ((y, x), board[y][x])
       
        #cornerPack evaluation        
        if((biggestValue[0][0] == 0 and biggestValue[0][1] == 0) or
           (biggestValue[0][0] == 0 and biggestValue[0][1] == 3) or
           (biggestValue[0][0] == 3 and biggestValue[0][1] == 0) or
           (biggestValue[0][0] == 3 and biggestValue[0][1] == 3)):
            cornerPack_total += math.log(biggestValue[1]) / math.log(2)
            if(b.adjacent(biggestValue[0], biggerValue[0])):
                cornerPack_total *= 2
                if(b.adjacent(biggestValue[0], bigValue[0])):
                    cornerPack_total *= 1.5
        
        #monotonicity evaluation
        temp_totals = [0, 0, 0, 0]
        #left and right
        for row in range(4): 
            currentCol = 0
            nextCol = 1
            while(nextCol < 4):
                while(board[row][nextCol] != 0 and nextCol < 3):
                    nextCol += 1
                if(board[row][currentCol] != 0):
                    currentValue = math.log(board[row][currentCol]) / math.log(2)
                else:
                    currentValue = 0
                if(board[row][nextCol] != 0):
                    nextValue = math.log(board[row][nextCol]) / math.log(2)
                else:
                    nextValue = 0
                if(currentValue > nextValue):
                    temp_totals[0] += nextValue - currentValue
                elif(nextValue > currentValue):
                    temp_totals[1] += currentValue - nextValue
                currentCol = nextCol
                nextCol += 1
        #up and down
        for col in range(4): 
            currentRow = 0
            nextRow = 1
            while(nextRow < 4):
                while(board[nextRow][col] != 0 and nextRow < 3):
                    nextRow += 1
                if(board[currentRow][col] != 0):
                    currentValue = math.log(board[currentRow][col]) / math.log(2)
                else:
                    currentValue = 0
                if(board[nextRow][col] != 0):
                    nextValue = math.log(board[nextRow][col]) / math.log(2)
                else:
                    nextValue = 0
                if(currentValue > nextValue):
                    temp_totals[2] += nextValue - currentValue
                elif(nextValue > currentValue):
                    temp_totals[3] += currentValue - nextValue
                currentRow = nextRow
                nextRow += 1
        
        #weight totals
        if(openSpots_total != 0):
            openSpots_total = math.log(openSpots_total) * 3
        rowSmoothness_total *= .1
        columnSmoothness_total *= .1
        maxValue_total = math.log(biggestValue[1]) / math.log(2)
        #monotonic_total = max(temp_totals[0], temp_totals[1]) + max(temp_totals[2], temp_totals[3])
        #print("Open space: " + str(openSpots_total) +"\nsmoothness: " + str(rowSmoothness_total + columnSmoothness_total) + "\ncornerPack: " + str(cornerPack_total))
        #print("Monotonic Total: " + str(monotonic_total))
        total = openSpots_total + maxValue_total + rowSmoothness_total + columnSmoothness_total + monotonic_total + cornerPack_total
        return total
        
