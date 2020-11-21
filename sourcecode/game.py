from copy import deepcopy
from players import *
import pygame as pg
from aux_funcs import valid_fence, win_condition
import random as rnd

class Board:
    def __init__(self, rows, cols, screen):
        pg.font.init()
        self.font = pg.font.SysFont('Comic Sans MS', 21)
        self.rows = rows
        self.cols = cols
        self.w, self.h = pg.display.get_surface().get_size()
        self.w /= cols
        self.h /= rows
        self.pawns = [Player(0, cols, rows), Player(1, cols, rows), Player(2, cols, rows), Player(3, cols, rows)] 
        self.mouse_rect = pg.Rect(0, 0, 0, 0)
        self.turn = rnd.randint(0,3)            
        self.mouse_index = [-1,-1]
        ####matrix#####
        self.backend = [[{True:['#',[]], False:[' ',[0,1,2,3]]}[x==0 or x ==cols+1] for x in range(cols+2)] for _ in range(rows+2)]
        a = [['#',[]] for _ in range(rows+2)]
        self.backend[0] = deepcopy(a); self.backend[-1] = deepcopy(a)
    def mouse_shadow(self, screen, pos):
        p = 0.14
        if not (self.w*p < pos[0]%self.w and pos[0]%self.w < self.w*(1-p)):
            col, row = pos[0]//self.w, pos[1]//self.h
            if col == 0 or col == self.cols -1: return
            if row == self.rows-1: row -= 1
            if col*self.w+(self.w/2) < pos[0]: col += 1
            self.mouse_rect = pg.Rect((col*self.w)-(self.w*p), row*self.h, (self.w*p)*2, self.h*2)
            pg.draw.rect(screen, Cregshadow, self.mouse_rect)
            self.mouse_index = (int(row), int(col))
            return
        elif not (self.h*p < pos[1]%self.h and pos[1]%self.h < self.h*(1-p)):
            col, row = pos[0]//self.w, pos[1]//self.h
            if row == 0 or row == self.rows -1: return
            if col == self.cols-1: col -= 1
            if row*self.h+(self.h/2) < pos[1]: row+=1 
            self.mouse_rect = pg.Rect(col*self.w,(row*self.h)-(self.h*p),self.w*2, (self.h*p)*2)
            pg.draw.rect(screen, Cregshadow, self.mouse_rect)
            self.mouse_index = (int(row), int(col))
            return
        else:
            self.mouse_index = (int(-1), int(-1))
            return
    
    def remove_bknd(self, n, pos):
        if n in pos[1]:
            pos[1].pop(pos[1].index(n))
            return True
        else: return False

    def click(self, screen): ### click func missing
        ####MOVS##### (DX,DY)
        #
        # [(1,0), (-1,0), (0,1), (0,-1)]
        #
        #    R       L      D       U
        #
        if self.mouse_index == (-1,-1): return 
        if self.mouse_rect.size[0] > self.mouse_rect.size[1]:
            #horizontal
            row, col = self.mouse_index
            row +=1 
            col += 1
            print("Recieved: ", (self.mouse_index))
            print(f"Modifying row = {row}; col = {col}")
            #backup
            SLL = deepcopy(self.backend[row][col]) 
            SLR = deepcopy(self.backend[row][col+1]) 
            STL = deepcopy(self.backend[row-1][col]) 
            STR = deepcopy(self.backend[row-1][col+1]) 
            #remove
            self.remove_bknd(3,self.backend[row][col])
            self.remove_bknd(3,self.backend[row][col+1])
            self.remove_bknd(2,self.backend[row-1][col])
            self.remove_bknd(2,self.backend[row-1][col+1])
            if not valid_fence(self.backend):
                #UNDO
                self.backend[row][col] = SLL 
                self.backend[row][col+1] = SLR
                self.backend[row-1][col] = STL
                self.backend[row-1][col+1] = STR

        else:
            #vertical
            row, col = self.mouse_index
            row += 1
            print("Recieved: ", (self.mouse_index))
            print(f"Modifying row = {row}; col = {col}")
            #backup
            STL = deepcopy(self.backend[row][col])
            STR = deepcopy(self.backend[row][col+1])
            SBL = deepcopy(self.backend[row+1][col])
            SBR = deepcopy(self.backend[row+1][col+1])
            #remove
            self.remove_bknd(0,self.backend[row][col])
            self.remove_bknd(1,self.backend[row][col+1])
            self.remove_bknd(0,self.backend[row+1][col])
            self.remove_bknd(1,self.backend[row+1][col+1])
            if not valid_fence(self.backend):
                self.backend[row][col]    = STL
                self.backend[row][col+1]  = STR 
                self.backend[row+1][col]  = SBL 
                self.backend[row+1][col+1] = SBR

        self.mouse_index = (-1,-1) 
        return
    def draw_backend(self):
        for i in self.backend: print(i)
        return 
    def update_players(self, screen, w, h):
        # draw pawns
        for pawn in self.pawns: 
            pg.draw.circle(screen, pawnsC[pawn.side], pawn.get_coord(screen, w, h), abs(int(w/2) - 5))
            self.backend[pawn.y+1][pawn.x+1][0] = representation[pawn.side]
        return
    ####MOVS##### (DX,DY)
    # 
    # [(1,0), (-1,0), (0,1), (0,-1)]
    #
    #    R       L      D       U
    # 
    def draw_board(self, screen, w, h, p, info):
        # rectangles
        fences = []
        for i in range(self.rows):
            for j in range(self.cols):
                x, y = j*w, i*h
                pg.draw.rect(screen, Cwhite, (j*w,  i*h, w, h))
                pg.draw.rect(screen, Cbrown, (j*w+p, i*h+p, w-p*2, h-p*2))
                if info:
                    screen.blit(self.font.render(str(self.backend[i+1][j+1][1]), False, Cwhite), (p+(j*w),p+(i*h)))    
                    screen.blit(self.font.render(str((j+1, i+1)), False, Cwhite), (p+(j*w),p+(i*h)+h/2))    
                if len(self.backend[i+1][j+1][1]) < 4:
                    fences.append([(i+1,j+1), self.backend[i+1][j+1][1]])
        #RECT(X,Y,W,H)
        for pos, restr in fences:
            y,x=pos
            x -= 1; y-= 1
            #block = (pos[1]-1)*w, (pos[0]-1)*h, w, h)
            
            #top = (x,y,w*2,h*p) 
            #R
            if   0 not in restr:
                pg.draw.rect(screen, Cblack, (((x+1)*w)-w*0.1,(y*h),w*0.15,h))
            #L
            if 1 not in restr:
                pg.draw.rect(screen, Cblack, ((x*w),(y*h),w*0.1,h))
            #D
            if 2 not in restr:
                pg.draw.rect(screen, Cblack, ((x*w),((y+1)*h)-w*0.1,w,h*0.15))
            #U
            if 3 not in restr: 
                pg.draw.rect(screen, Cblack, ((x*w),(y*h),w,h*0.1))
            

    def move_pawns(self):
        print("\n")
        self.moveflag = True
        self.pawns[self.turn].next_move(self.backend)
        self.turn = (self.turn+1)%4
        print(self.turn)
    
    def update_board(self, screen, info):
        pg.display.set_caption(f"Mouse at {self.mouse_index}\tTurn of player {self.turn}")
        w, h, p = self.w, self.h, 1
        self.draw_board(screen, w, h, p, info)
        self.update_players(screen, w, h)
        winner = win_condition(self.backend)
        if winner != ' ':
            print(winner)
            return self.turn*10
        return self.turn


