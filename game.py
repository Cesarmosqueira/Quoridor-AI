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
		self.valid_rect = pg.Rect(0, 0, 0, 0)
		self.placing_fence = False
		self.turn = {True:-1,False:1}[rnd.randint(0,1) == 0]            
		self.mouse_index = [-1,-1]
		####matrix#####
		self.backend = [[{True:'#', False:' '}[x==0 or x ==cols+1] for x in range(cols+2)]]*int(rows+2)
		a = ['#']*(rows+2)
		self.backend[0] = a; self.backend[-1] = a


	def mouse_shadow(self, screen, pos):
		col, row = pos[0]//self.w, pos[1]//self.h
		p = 2
		self.mouse_rect = pg.Rect(col*self.w+p, row*self.h+p, self.w-p*2, self.h-p*2)
		self.valid_rect = None
		if (row, col) != self.p1.get_col_row() and (row, col) != self.p2.get_col_row():
			pg.draw.rect(screen, Cregshadow, self.mouse_rect)
			self.valid_rect = self.mouse_rect
			self.mouse_index = (int(row),int(col))
	
	def click(self, screen):
		# turn
		if self.valid_rect and self.mouse_index != self.p1.get_col_row() and self.mouse_index != self.p2.get_col_row():
			pg.draw.rect(screen,Cblack,(self.valid_rect))
			prev = self.backend[self.mouse_index[0]+1] 
			if valid_block(self.backend,self.mouse_index[0]+1, self.mouse_index[1]+1):
				self.backend[self.mouse_index[0]+1] = [' ' if x != self.mouse_index[1]+1 and prev[x] != '#' else '#' for x in range(int(self.cols+2))]
				self.backend[self.mouse_index[0]+1][0] = '#'; self.backend[self.mouse_index[0]+1][-1] = '#'
			
			#for i in self.backend: print(i)

	def update_players(self, screen, w, h):
		# draw pawns
		pg.draw.circle(screen, Cpawn1, self.p1.get_coord(screen, w, h), abs(int(w/2) - 5))
		pg.draw.circle(screen, Cpawn2, self.p2.get_coord(screen, w, h), abs(int(w/2) - 5))
		pos1, pos2 = self.p1.get_col_row(), self.p2.get_col_row()
		self.backend[pos1[0]+1] = ['X' if x == pos1[1]+1 else str(self.backend[pos1[0]+1][x]) for x in range(int(self.cols+2))]
		self.backend[pos2[0]+1] = ['O' if x == pos2[1]+1 else str(self.backend[pos2[0]+1][x]) for x in range(int(self.cols+2))]

	def draw_board(self, screen, w, h, p):
		# rectangles
		for i in range(self.rows):
			for j in range(self.cols):
				pg.draw.rect(screen, Cwhite, (i*w, j*h, w, h))
				pg.draw.rect(screen, Cbrown, (i*w+p, j*h+p, w-p*2, h-p*2))
				if self.backend[j+1][i+1] == '#':
					pg.draw.rect(screen, Cblack, (i*w, j*h, w, h))

	def move_pawns(self):
		if self.turn == 1: self.p1.next_move(self.backend)
		else: self.p2.next_move(self.backend)
		self.turn *= -1


	def update_board(self, screen):
		w, h, p = self.w, self.h, 1
		self.draw_board(screen, w, h, p)
		self.update_players(screen, w, h)
		if win_condition(self.backend) != ' ':
			print('HA GANADO ALGUIEN y es ', 'El verde' if win_condition(self.backend) == 'O' else 'El azul')
			input()
			quit()
		return self.turn


