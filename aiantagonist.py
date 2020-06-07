# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 17:01:07 2017

@author: RoySorce
"""

class Antagonist:
    
    def __init__(self, b):
        self.board = b
        self.name = "antagonist"
        
    def makeMove(self, move):
        self.board.makeMoves(move)
    
    def getMoves(self):
        move = self.alpha_beta(self.board, 2)
        return move
        
    def alpha_beta(self ,b, depth):
        if(depth == 0): #random tile selection
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
        occupied_spaces = 0
        for x in range(4):
            last_non_zero_value= -1
            for y in range(4):
                if(board[x][y] != 0):
                    if(last_non_zero_value != -1):
                        if(board[x][y] != last_non_zero_value):
                            total += 10
                    last_non_zero_value = board[x][y]
                    occupied_spaces += 1
        
        for x in range(4):
            last_non_zero_value= -1
            for y in range(4):
                if(board[y][x] != 0):
                    if(last_non_zero_value != -1):
                        if(board[y][x] != last_non_zero_value):
                            total += 10
                    last_non_zero_value = board[y][x]
                    
        total += occupied_spaces*2
        return total

                    
                        
            
        
    
        
    
     