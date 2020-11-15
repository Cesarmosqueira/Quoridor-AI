import pygame as pg
from aux_funcs import get_next_move
Cwhite = (255, 255, 255)
Cbrown = (112, 72, 60)
Cblack = (0, 0, 0)
Cpawn1 = (3, 140, 252)
Cpawn2 = (112, 181, 0)
Cshadow1 = (148,192,209)
Cshadow2 = (156,173,128)
Cregshadow = (255, 255, 102)
class Player:
        def __init__(self, side, cols, rows): ## side == True = UP else DOWN 
                self.x = cols//2
                self.y = {True: 0, False: rows-1}[side == True]
                self.side = side
                # [[(1,0),'V'],[(3,2), 'H']] ##max = 20 ##(x,y),side H/V
                self.fences = []

        def get_coord(self, screen, col_w, row_h):
                X, Y = int(((self.x+1)*col_w)-col_w/2), int(((self.y+1)*row_h)-row_h/2)
                return (int(X), int(Y))
        def get_col_row(self):
                return (self.y, self.x)

        def place_item(self, item, f, rows, cols):
                if f == True:
                        side = {True: 'H', False: 'V'}[item.w > item.h]
                        pos = ((item.left//cols)+{True: 0, False: 1}
                                   [side == 'H'], (item.top//rows)+{True: 0, False: 1}[side == 'V'])
                        self.fences.append([pos, side])
                # f == false???
                return
        def next_move(self, board):  ###BFSBFS
                print(board[self.y+1][self.x+1])
                board[self.y+1][self.x+1][0] = ' '
                self.y , self.x = get_next_move(board, self.side, (self.y+1, self.x+1))
                return

                
        def get_adyacents(self):
                #### not diagonals
                return [(self.x-1,self.y),(self.x+1,self.y),(self.x,self.y-1),(self.x,self.y+1)]
                

