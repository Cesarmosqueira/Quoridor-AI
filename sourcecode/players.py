import pygame as pg
from copy import deepcopy
from aux_funcs import get_next_move, valid_fence, make_and_do_choice
from random import randint
Cwhite = (255, 255, 255)
Cbrown = (112, 72, 60)
Cblack = (0, 0, 0)
Cpawn1 = (3, 140, 252)
Cpawn2 = (112, 181, 0)
pawnsC = { 0: (227, 227, 14),
           1: (3, 140, 252),
           2: (181, 84, 0),
           3: (112, 181, 0)}
Cshadow1 = (148,192,209)
Cshadow2 = (156,173,128)
Cregshadow = (255, 255, 102)
representation = { 0: 'L',
                   1: 'T',
                   2: 'R',
                   3: 'B'}   
class Player:
    ## 0 = L
    ## 1 = T
    ## 2 = R
    ## 3 = B
    def __init__(self, side, cols, rows): ## side == True = UP else DOWN 
        self.x = 0
        self.y = 0
        if side == 0:
            self.x = 0
            self.y = rows//2
        if side == 1:
            self.x = cols//2
            self.y = 0
        if side == 2:
            self.x = cols - 1
            self.y = rows//2
        if side == 3:
            self.x = cols//2
            self.y = rows-1
        self.side = side
        # [[(1,0),'V'],[(3,2), 'H']] ##max = 20 ##(x,y),side H/V
        self.fences = []

    def get_coord(self, screen, col_w, row_h):
        X = self.x*col_w + col_w/2
        Y = self.y*row_h + row_h/2
        #X, Y = int(((self.x+1)*col_w)-col_w/2), int(((self.y+1)*row_h)-row_h/2)
        return (int(X), int(Y))

    def remove_bknd(self, n, pos):
        if n in pos[1]:
            pos[1].pop(pos[1].index(n))
            return True
        else: return False

    def next_move(self, board, players):  ###BFSBFS
        make_and_do_choice(board, players, self.side)
        return

    def place_fence(self, board, side, row, col):
        if side: #horizontal
            #horizontal
            #backup
            SLL = deepcopy(board[row][col]) 
            SLR = deepcopy(board[row][col+1]) 
            STL = deepcopy(board[row-1][col]) 
            STR = deepcopy(board[row-1][col+1]) 
            #remove
            self.remove_bknd(3,board[row][col])
            self.remove_bknd(3,board[row][col+1])
            self.remove_bknd(2,board[row-1][col])
            self.remove_bknd(2,board[row-1][col+1])
            if not valid_fence(board):
                #UNDO
                board[row][col] = SLL 
                board[row][col+1] = SLR
                board[row-1][col] = STL
                board[row-1][col+1] = STR
        else:
            #vertical
            col -= 1
            #backup
            STL = deepcopy(board[row][col])
            STR = deepcopy(board[row][col+1])
            SBL = deepcopy(board[row+1][col])
            SBR = deepcopy(board[row+1][col+1])
            #remove
            self.remove_bknd(0,board[row][col])
            self.remove_bknd(1,board[row][col+1])
            self.remove_bknd(0,board[row+1][col])
            self.remove_bknd(1,board[row+1][col+1])
            if not valid_fence(board):
                board[row][col]    = STL
                board[row][col+1]  = STR 
                board[row+1][col]  = SBL 
                board[row+1][col+1] = SBR

    def unplace_fence(self,board,side,row,col):
        if side:
            SLL = board[row][col][1] 
            SLR = board[row][col+1][1] 
            STL = board[row-1][col][1] 
            STR = board[row-1][col+1][1]
            if 3 not in SLL: SLL.append(3)
            if 3 not in SLR: SLR.append(3)
            if 2 not in STL: STL.append(2)
            if 2 not in STR: STR.append(2)            
        else:
            col -= 1
            STL = board[row][col][1]    
            STR = board[row][col+1][1]  
            SBL = board[row+1][col][1]  
            SBR = board[row+1][col+1][1]
            if 0 not in STL: STL.append(0)
            if 1 not in STR: STR.append(1)
            if 0 not in SBL: SBL.append(0)
            if 1 not in SBR: SBR.append(1)            
    def can_place(self, board, side, row, col):
        if side:
            SLL = board[row][col][1] 
            SLR = board[row][col+1][1] 
            STL = board[row-1][col][1] 
            STR = board[row-1][col+1][1]
            if 3 not in SLL: return False 
            if 3 not in SLR: return False
            if 2 not in STL: return False
            if 2 not in STR: return False            
        else:
            col -= 1
            STL = board[row][col][1]    
            STR = board[row][col+1][1]  
            SBL = board[row+1][col][1]  
            SBR = board[row+1][col+1][1]
            if 0 not in STL: return False
            if 1 not in STR: return False
            if 0 not in SBL: return False
            if 1 not in SBR: return False            
        return True

    def get_adyacents(self):
        #### not diagonals
        return [(self.x-1,self.y),(self.x+1,self.y),(self.x,self.y-1),(self.x,self.y+1)]
            

