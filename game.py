from players import *
import pygame as pg
from aux_funcs import valid_block, win_condition
import random as rnd

class Board:
        def __init__(self, rows, cols, screen):
                self.rows = rows
                self.cols = cols
                self.w, self.h = pg.display.get_surface().get_size()
                self.w /= cols
                self.h /= rows
                self.p1 = Player(False, cols, rows)
                self.p2 = Player(True, cols, rows)
                self.mouse_rect = pg.Rect(0, 0, 0, 0)
                self.turn = {True:-1,False:1}[rnd.randint(0,1) == 0]            
                self.mouse_index = [-1,-1]
                ####matrix#####
                self.backend = [[{True:['#',[]], False:[' ',[0,1,2,3]]}[x==0 or x ==cols+1] for x in range(cols+2)]]*int(rows+2)
                a = [('#',[])]*(rows+2)
                self.backend[0] = a; self.backend[-1] = a
        def mouse_shadow(self, screen, pos):
            p = 0.14

            if not (self.w*p < pos[0]%self.w and pos[0]%self.w < self.w*(1-p)):
                col, row = pos[0]//self.w, pos[1]//self.h
                if row == self.rows-1: row -= 1
                pg.display.set_caption("Vertical " + str((col,row)))
                if col*self.w+(self.w/2) < pos[0]: col += 1
                self.mouse_rect = pg.Rect((col*self.w)-(self.w*p), row*self.h, (self.w*p)*2, self.h*2)
                pg.draw.rect(screen, Cregshadow, self.mouse_rect)
                self.mouse_index = (int(row), int(col))
                return
            elif not (self.h*p < pos[1]%self.h and pos[1]%self.h < self.h*(1-p)):
                col, row = pos[0]//self.w, pos[1]//self.h
                if col == self.cols-1: col -= 1
                pg.display.set_caption("Horizontal "+str((col,row)))
                if row*self.h+(self.h/2) < pos[1]: row+=1 
                self.mouse_rect = pg.Rect(col*self.w,(row*self.h)-(self.h*p),self.w*2, (self.h*p)*2)
                pg.draw.rect(screen, Cregshadow, self.mouse_rect)
                self.mouse_index = (int(row), int(col))
                return
            else:
                pg.display.set_caption("None")
                self.mouse_index = (int(-1), int(-1))
                return
        
        def click(self, screen): ### click func missing
                if self.mouse_index == (-1,-1): return 
                if self.mouse_rect.size[0] > self.mouse_rect.size[1]:
                    print("Horizontal")
                    row, col = self.mouse_index
                    row+= 1; col+= 1
                    old = self.backend[row]
                    self.backend[row] = [[old[i][0], [0,1,2,3]] if i == col or i == col+1 else old[i] for i in range(len(old))]
                    return
                else:
                    print("Vertical")
                    row, col = self.mouse_index
                    row+=1; col+=1
                    old, bold  = self.backend[row], self.backend[row+1]
                    self.backend[row] = [[old[i][0], [0,1,2,3]] if i == col else old[i] for i in range(len(old))]
                    self.backend[row+1] = [[bold[i][0], [0,1,2,3]] if i == col else bold[i] for i in range(len(bold))]

                return

        def update_players(self, screen, w, h):
                # draw pawns
                pg.draw.circle(screen, Cpawn1, self.p1.get_coord(screen, w, h), abs(int(w/2) - 5))
                pg.draw.circle(screen, Cpawn2, self.p2.get_coord(screen, w, h), abs(int(w/2) - 5))
                pos1, pos2 = self.p1.get_col_row(), self.p2.get_col_row()
                self.backend[pos1[0]+1] = [('X',self.backend[pos1[0]+1][i][1]) if i == pos1[1]+1 else self.backend[pos1[0]+1][i] for i in range(len(self.backend[pos1[0]+1]))]
                self.backend[pos2[0]+1] = [('O',self.backend[pos2[0]+1][i][1]) if i == pos2[1]+1 else self.backend[pos2[0]+1][i] for i in range(len(self.backend[pos2[0]+1]))]
                return
        ####MOVS##### (DX,DY)
        # 
        # [(1,0), (-1,0), (0,1), (0,-1)]
        #
        #    R       L      D       U
        # 
        def draw_board(self, screen, w, h, p):
                # rectangles
                for i in range(self.rows):
                        for j in range(self.cols):
                                pg.draw.rect(screen, Cwhite, (i*w, j*h, w, h))
                                pg.draw.rect(screen, Cbrown, (i*w+p, j*h+p, w-p*2, h-p*2))
                                if len(self.backend[i+1][j+1][1]) < 4:
                                    for i in range(4):
                                        if i not in self.backend[i+1][j+1][1]:
                                            if i == 0:
                                                pg.draw.rect(screen, Cblack, (((i+1)*w)-(w*0.1), j*h, w*0.1, h))
                                            elif i == 1:
                                                pg.draw.rect(screen, Cblack, (i*w, j*h, w*0.1, h))
                                            elif i == 2:
                                                pg.draw.rect(screen, Cblack, (i*w,((j+1)*h)-(h*0.1), w, h*0.1))
                                            elif i == 3:
                                                pg.draw.rect(screen, Cblack, (i*w, j*h, w, h*0.1))

        def move_pawns(self):
                for i in self.backend: print(i)
                print("\n\n")
                self.moveflag = True
                #if self.turn == 1: self.p1.next_move(self.backend)
                #else: self.p2.next_move(self.backend)
                self.turn *= -1
        
        def update_board(self, screen):
                w, h, p = self.w, self.h, 1
                self.draw_board(screen, w, h, p)
                self.update_players(screen, w, h)
                winner = win_condition(self.backend)
                if winner != ' ':
                    print(winner)
                    return self.turn*10
                return self.turn


